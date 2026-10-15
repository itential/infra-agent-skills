# Endpoint Wiring — Docker Engine Container Workload Deployment

Literal API calls behind each capability named in `docker-engine/procedure.md`. All calls are against
the Docker Engine REST API, version `v1.51` (source: docs.docker.com/reference/api/engine/version/
v1.51, retrieved 2026-09-29), JSON request/response bodies unless noted.

## Authentication for registry-facing calls

Any call that pulls from or pushes to a registry carries an `X-Registry-Auth` header: a base64url
([RFC 4648 §5](https://tools.ietf.org/html/rfc4648#section-5))-encoded JSON string, either:

```json
{"username": "string", "password": "string", "serveraddress": "string"}
```

or, if an identity token was already obtained elsewhere (e.g. via Docker Hub's own auth flow — see
`docker-hub/endpoints.md`):

```json
{"identitytoken": "9cbaf023786cd7..."}
```

`serveraddress` is a bare domain/IP, no protocol prefix.

## Create a container

`POST /containers/create`

Query params: `name` (must match `^/?[a-zA-Z0-9][a-zA-Z0-9_.-]+$`), `platform` (`os[/arch[/variant]]`
— if set, the daemon 404s rather than using a mismatched cached image; if unset, a mismatched cached
image is used with a warning instead of a hard failure).

Body (`ContainerConfig` + `HostConfig` + `NetworkingConfig`), key fields:

| Field | Location | Notes |
|---|---|---|
| `Image` | top-level | Required — the image reference to run |
| `Cmd` / `Entrypoint` | top-level | Override the image's defaults |
| `Env` | top-level | Array of `"KEY=value"` strings |
| `ExposedPorts` | top-level | Object keyed `"port/proto": {}` |
| `Labels` | top-level | Free-form key/value metadata |
| `HostConfig.PortBindings` | HostConfig | `{"22/tcp": [{"HostPort": "11022"}]}` — host port must be free |
| `HostConfig.Binds` | HostConfig | `["/host/path:/container/path"]` |
| `HostConfig.RestartPolicy.Name` | HostConfig | `no` \| `on-failure` \| `always` \| `unless-stopped` |
| `HostConfig.RestartPolicy.MaximumRetryCount` | HostConfig | Used with `on-failure` |
| `HostConfig.Memory` / `NanoCpus` / `CpuShares` / etc. | HostConfig | Resource limits |
| `HostConfig.AutoRemove` | HostConfig | Remove the container automatically on exit |
| `HostConfig.NetworkMode` | HostConfig | e.g. `"bridge"` |
| `NetworkingConfig.EndpointsConfig` | top-level | Per-network IPAM/aliases config |

Response `201`: `{"Id": "...", "Warnings": [...]}`. Errors: `400` bad parameter, `404` no such image
(example message: `"No such image: c2ada9df5af8"`), `409` conflict, `500` server error.

## Inspect a container

`GET /containers/{id}/json`

Query param: `size` (boolean, default `false`) — adds `SizeRw`/`SizeRootFs` to the response.

Response `200` key fields under `State`: `Status` (enum `created`|`running`|`paused`|`restarting`|
`removing`|`exited`|`dead` — authoritative field), `Running` (bool — can be `true` simultaneously with
`Paused: true`), `Paused`, `Restarting`, `OOMKilled`, `Dead`, `Pid`, `ExitCode`. Errors: `404` no such
container, `500` server error.

## Start a container

`POST /containers/{id}/start`

Query param: `detachKeys` (override the detach key sequence). Responses: `204` no error, `304`
container already started, `400` bad parameter (including an invalid checkpoint ID), `404` no such
container, `500` server error.

## Stop / Restart / Kill a container

- `POST /containers/{id}/stop` — query params `signal` (default per-container, typically `SIGTERM`),
  `t` (seconds to wait before killing). `204` no error, `304` already stopped, `404` no such container,
  `500` server error.
- `POST /containers/{id}/restart` — same `signal`/`t` params. `204` no error, `404` no such container,
  `500` server error.
- `POST /containers/{id}/kill` — query param `signal` (default `SIGKILL`). `204` no error, `404` no
  such container, `409` conflict (container not running — example message: `"Container <id> is not
  running"`), `500` server error.

## Update a container's resources

`POST /containers/{id}/update`

Body: `Resources` fields (`BlkioWeight`, `CpuShares`, `CpuPeriod`, `CpuQuota`,
`CpuRealtimePeriod`/`CpuRealtimeRuntime`, `CpusetCpus`/`CpusetMems`, `Memory`, etc.) plus
`RestartPolicy`. Response `200`: `ContainerUpdateResponse` with a `Warnings` array. Errors: `404` no
such container, `500` server error.

## Remove a container

`DELETE /containers/{id}`

Query params: `v` (bool, default `false` — also remove anonymous volumes), `force` (bool, default
`false` — kill first if running), `link` (bool, default `false` — remove only the named link).
Responses: `204` no error, `400` bad parameter, `404` no such container, `409` conflict (documented
example: `"You cannot remove a running container: <id>. Stop the container before attempting removal
or force remove"`), `500` server error.

## Pull (create) an image

`POST /images/create`

Query params: `fromImage` (image name to pull — tag/digest may be embedded), `fromSrc` (URL or `-` to
import from the request body instead of pulling), `repo`/`tag` (used when importing), `message`
(commit message for an import), `platform` (`os[/arch[/variant]]`), `changes` (array of Dockerfile
instructions applied to the imported image — supported: `CMD`|`ENTRYPOINT`|`ENV`|`EXPOSE`|`ONBUILD`|
`USER`|`VOLUME`|`WORKDIR`). Header: `X-Registry-Auth` (see above). If neither a tag nor digest is given
in `fromImage`, every tag for that image name is pulled. Response `200` (streamed JSON progress
events). Errors: `404` repository does not exist or no read access, `500` server error.

## Push an image

`POST /images/{name}/push`

`{name}` should be given without a tag (a tag suffix is ignored) — it must already reference the
target registry host, e.g. `registry.example.com/myimage`; Docker Hub is the implicit registry when no
host prefix is present. Query params: `tag` (which tag to push — if omitted, every locally-present tag
for that image is pushed), `platform` (`os[/arch[/variant]]` variant to push, JSON-encoded). Header:
`X-Registry-Auth` (required). Push is documented as cancelled if the client's HTTP connection to the
daemon closes mid-transfer. Response `200` no error. Errors: `404` no such image, `500` server error.

## Tag an image

`POST /images/{name}/tag`

Query params: `repo` (target repository, e.g. `someuser/someimage`), `tag` (new tag name). Creates an
additional reference to the source image; overwrites the target repo/tag if it already exists.
Response `201` no error. Errors: `400` bad parameter, `404` no such image, `409` conflict, `500` server
error.
