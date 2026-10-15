# Docker Engine — Container Workload Deployment Procedure

Create, start, stop, update, or remove a container against a Docker Engine daemon, and pull/tag/push
the image it runs from. Covers the plain Container and Image endpoints of the Docker Engine API only
— Swarm services, networks/volumes beyond what a container directly references, and Compose's own
multi-container orchestration model are out of scope. Assumes an authenticated Docker Engine API
client is already available (local Unix socket with no additional auth, or a TLS client for a remote
daemon per the vendor's own guidance) and, for any call that touches a registry (pulling or pushing an
image), an `X-Registry-Auth` credential is available to attach. Source: Docker Engine API v1.51
reference (docs.docker.com/reference/api/engine), retrieved 2026-09-29.

## Operational procedure

### 1. Make sure the image is present, or pull it

If the image isn't already in the local image store, pull it first. This is a registry-facing call and
carries an `X-Registry-Auth` header — a base64url-encoded JSON object of either
`{"username","password","serveraddress"}` or `{"identitytoken"}` (the latter if one was already
obtained, e.g. from Docker Hub's own auth flow — see `docker-hub/procedure.md`). Without a tag or
digest specified, the pull retrieves every tag for that image name, which is rarely what's wanted for
a deploy — always pin a tag or digest.

### 2. Confirm before creating a container whose name is already in use

Container names must be unique on the daemon. If a container with the intended name already exists
(running or stopped), decide explicitly whether to remove it first (step 6, with that step's
confirmation gate) or pick a different name — don't let the create call fail into an ambiguous state.

### 3. Build the container create request

Assemble the body around the target `Image` plus, as needed: `Cmd`/`Entrypoint` (override the image's
defaults), `Env` (list of `KEY=value` strings), `ExposedPorts`, `Labels`, `WorkingDir`, and a
`HostConfig` block for anything host-facing — `PortBindings` (maps a container port to a specific host
port; each host port can only be claimed by one container at a time, which matters for step 8's
scaling pattern), `Binds`/mount definitions, `RestartPolicy` (`Name` one of `no`/`on-failure`/
`always`/`unless-stopped`, plus `MaximumRetryCount` for `on-failure`), resource limits (`Memory`,
`NanoCpus`, etc.), and `AutoRemove` (delete the container automatically once it exits, if that's the
desired lifecycle). Pass the intended container name as the `name` query parameter, not in the body.

### 4. Submit the create and read the response

A successful create returns `201` with the new container's `Id` and a `Warnings` array — always
surface `Warnings` even on success, since the daemon uses it for non-fatal notices (for example, a
platform mismatch between the requested and locally cached image). Documented failure modes: `400`
bad parameter, `404` no such image (the pull in step 1 didn't actually land, or the name is wrong),
`409` conflict (most often the name-in-use case from step 2), `500` server error.

### 5. Start the container

Call start against the new container's `Id`. `204` means it's now starting; `304` means it was already
started (not an error condition to retry against); `404` no such container; `400` bad parameter
(including an invalid checkpoint ID, if checkpoint/restore is in use); `500` server error.

### 6. Confirm the container is actually running

A `204` from start only means the daemon accepted the start request — inspect the container afterward
to confirm it's actually up. Read `State.Status`, which is the authoritative field: one of `created`,
`running`, `paused`, `restarting`, `removing`, `exited`, or `dead`. Don't rely on `State.Running` alone
to mean "healthy and running" — a paused container is documented as both `Running: true` and `Paused:
true` simultaneously, so `Status` is the field that actually distinguishes the states. If `Status` is
`exited`, also check `State.ExitCode` and `State.OOMKilled` to understand why.

### 7. Update a running container's resources without recreating it

For a resource-limit or restart-policy change that doesn't require touching the image or command,
update the existing container in place rather than removing and recreating it — the same resource
fields available at create time (`Memory`, `NanoCpus`, `CpuShares`, etc.) plus `RestartPolicy` can be
changed on a live container. Response `200` includes its own `Warnings` array (surface it the same way
as step 4); `404` no such container; `500` server error.

### 8. Scale — no native primitive; documented workaround pattern only

The Docker Engine API has no "scale" or replica-count call for a plain container — this is a real gap
relative to Kubernetes' scale subresource, not an oversight in this procedure. The only
documented-behavior-consistent way to run N copies of the same workload is to repeat steps 2–6 with N
distinct `name` values. If the workload binds a host port via `PortBindings`, each of the N containers
needs a distinct host port (the daemon's own port-binding behavior means a second container claiming
an already-bound host port fails at create/start) — so a fixed host-port binding caps how many copies
can run side-by-side on one host. If the caller actually needs declarative, autoscaler-driven
replica-count scaling, that's a Swarm service or a Kubernetes Deployment, both out of scope for this
file.

### 9. Stop, restart, or kill

- **Stop** (graceful): sends a documented default of `SIGTERM`, or an overridden `signal`, then kills
  after a `t`-second grace period. `204` no error, `304` already stopped, `404` no such container,
  `500` server error.
- **Restart**: stop-then-start in one call, same `signal`/`t` query params as stop. `204` no error,
  `404` no such container, `500` server error.
- **Kill**: sends a signal immediately without the stop grace period (defaults to `SIGKILL`). `204` no
  error, `404` no such container, `409` conflict if the container isn't running, `500` server error.

### 10. Remove the container

**Stop and confirm with the operator before removing a container, and especially before force-removing
a running one** — state the container name/Id and whether `force` will be used. Query params: `v`
(also remove anonymous volumes associated with it), `force` (kill it first if running, rather than
requiring a prior stop), `link` (remove a specific link instead of the container itself). `204` no
error; `400` bad parameter; `404` no such container; `409` conflict — the documented case is attempting
to remove a running container without `force`; `500` server error.

### 11. Tag or push the image afterward, if publishing is part of the workflow

- **Tag**: create an additional reference (`repo`/`tag` query params) to an existing local image;
  overwrites the target repo/tag combination if it already exists. `201` no error, `400` bad parameter,
  `404` no such image, `409` conflict, `500` server error.
- **Push**: the image `name` path parameter must already carry (or be given, via tagging first) the
  registry hostname it's being pushed to (e.g. `registry.example.com/myimage`) — Docker Hub itself is
  the implicit registry when no hostname prefix is present. Requires the same `X-Registry-Auth` header
  as pulling. If the HTTP connection to the daemon is closed mid-push, the push is documented as
  cancelled — don't assume partial success. `200` no error, `404` no such image, `500` server error.

## Patterns

- **`Warnings` arrays on create/update responses are easy to miss because the call still returns a
  success status** — always check them, not just the status code.
- **`State.Status` is authoritative over the individual booleans** (`Running`/`Paused`/`Restarting`)
  for determining what state a container is actually in.
- **Registry-facing calls (pulling or pushing an image) need `X-Registry-Auth`; plain container
  lifecycle calls (create/start/stop/remove) don't** — don't attach registry credentials where they
  aren't needed, and don't skip them where they are.

## Known limitations

- No native scale/replica-count primitive — see step 8.
- Covers the plain Container and Image endpoints only; Swarm services, Compose-level orchestration, and
  networks/volumes beyond what a container directly attaches to are out of scope.
- A host-port-bound container caps how many same-workload copies can coexist on one daemon (step 8) —
  this procedure documents the constraint, it doesn't work around it.

## Tools

Every operation maps to the Docker Engine REST API — see `endpoints.md` for literal routes, query
parameters, and status codes.

| Operation | Description | Category |
|---|---|---|
| Create/Start/Stop/Restart/Kill/Update/Remove Container | Full container lifecycle | Container Management |
| Inspect Container | Read current state (`State.Status` and related fields) | Container Management |
| Create (pull) / Push / Tag Image | Registry-facing image operations plus local re-tagging | Image Management |

## Verification checklist

- [ ] Image presence was confirmed or pulled (with a pinned tag/digest) before create
- [ ] A name collision was resolved deliberately (remove-first or different name), not left to fail
      into the `409` case
- [ ] `Warnings` on create/update responses were checked, not just the status code
- [ ] Running state was confirmed via `State.Status`, not just a `204` from the start call
- [ ] Any remove (especially a forced remove of a running container) was confirmed with the operator
      first
- [ ] Registry credentials were attached only on pull/push, matching what the source documents as
      requiring `X-Registry-Auth`
