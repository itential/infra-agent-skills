# HAProxy — Frontend/Backend/Server Configuration and Runtime State Procedure

Defines a frontend (the VIP equivalent) and a backend with server lines (pool/pool-member
equivalent) in HAProxy's configuration file, and manages a server's live state (drain, maintenance,
weight) at runtime via HAProxy's Runtime API (the stats socket) without requiring a config reload.
Assumes shell/file access to edit and reload the target HAProxy instance's configuration, and a way
to reach its Runtime API socket (commonly via `socat`, or an equivalent client), are already
available. Does not cover HAProxy's Data Plane API (a separate REST management layer) — see Known
limitations — ACL/routing-rule authoring, or TLS certificate provisioning (see
`certificate-management`).

Source: HAProxy configuration-basics documentation
(https://www.haproxy.com/blog/haproxy-configuration-basics-load-balance-your-servers) for the
config-file block shape, and the HAProxy Runtime API reference
(https://www.haproxy.com/documentation/haproxy-runtime-api/reference/ and its `set-server` page) for
the live state-management commands, both retrieved 2026-09-17. Some general `server`-line parameter
semantics (exact behavior of `check`, `weight`, `disabled`) could not be retrieved verbatim from a
primary source in this research pass despite repeated attempts (the full configuration manual page
truncated before reaching that section on every attempt) — those are flagged below as commonly-known
HAProxy convention rather than presented as directly page-sourced.

This is a CLI/config-driven procedure per this repository's own convention: the literal
configuration-file syntax and Runtime API commands are the payload passed to a generic "edit this
config file" / "run this command against the target's management interface" capability — there is
no separate `endpoints.md` wiring layer for this vendor.

## Operational procedure

### Define a backend with initial servers (pool equivalent)

1. **Choose a unique backend name** — HAProxy's configuration is a flat namespace of named
   `frontend`/`backend`/`listen` sections; confirm the intended name doesn't already exist in the
   target configuration before adding a new section under it.
2. **Write the backend block** with one `server` line per pool member, in the confirmed minimal
   form: `server <member-name> <address>:<port>`. This bare form was the only shape independently
   confirmed as a verbatim worked example in this research pass; commonly-documented additional
   per-server keywords include `weight` (relative load-balancing weight) and `check` (enables active
   health checking for that server) — both are real, widely-documented HAProxy keywords, but their
   exact parameter ranges/defaults were not independently confirmed verbatim from a primary source
   in this pass. State any specific weight/check value the caller wants explicitly rather than
   assuming a default if precision matters, and confirm the exact accepted syntax against the target
   HAProxy version's own current documentation before relying on anything beyond the bare
   `server <name> <address>:<port>` form.
3. **Apply the change** — HAProxy's configuration file is declarative; a new/changed backend or
   server line takes effect only once the running process reloads its configuration (the exact
   reload mechanism — an init-system reload command, a container replacement, or HAProxy's own
   `-sf`/seamless-reload behavior — depends on how the target instance is deployed and was not
   itself confirmed from a primary source in this pass; use whatever reload mechanism the target
   environment's own operational runbook specifies).
4. **Confirm the reload succeeded** — HAProxy validates its configuration on reload and will refuse
   to apply a broken config; check the process's own reload outcome (exit status / log output)
   before considering the backend live, rather than assuming a submitted config change is already
   in effect.

### Define a frontend (VIP equivalent)

5. **Write the frontend block** binding to the intended VIP address and port, with a
   `default_backend` pointing at the backend created above. Confirmed minimal verbatim form:
   ```
   frontend <name>
   bind <address>:<port>
   default_backend <backend-name>
   ```
6. **Apply and confirm the reload**, as in steps 3-4.

### Add a pool member to an existing backend

7. **Prefer the Runtime API's dynamic-server commands over a config-file edit** when the target
   HAProxy instance supports dynamic servers, since this avoids a full reload: this platform
   documents `add server` ("add a dynamic server to a backend") and the corresponding
   `del server` ("remove a dynamic server from a backend") as Runtime API commands. If dynamic
   servers aren't available/supported on the target instance, add a `server` line to the backend's
   config-file block instead and follow steps 3-4.
8. **Confirm the member is visible** in the backend's live server list (via the Runtime API's own
   `show servers state` command, which dumps the current state of servers in backends) before
   reporting the member added.

### Change a member's live state without a config reload (drain / maintenance / weight)

9. **Distinguish the specific state-change commands documented for this platform** — do not treat
   them as interchangeable:
   - `disable server <backend>/<server>` — puts the server into maintenance mode (a top-level
     Runtime API command, separate from the `set server ... state ...` sub-form below).
   - `enable server <backend>/<server>` — takes the server back out of maintenance mode.
   - `set server <backend>/<server> state drain` — a distinct documented sub-form of `set server`
     for placing a server in a draining state.
   - `set server <backend>/<server> health down` — forces the server's reported health to down.
   - `set weight` / `set server <backend>/<server> weight <value>` — changes the server's relative
     load-balancing weight (a percentage form, e.g. `weight 50%`, was shown in the source).
   This source did not provide a single reconciling state-machine explanation of how `disable
   server`'s maintenance mode, `state drain`, and `health down` relate to or override each other —
   treat each as its own documented mechanism and report the outcome using the specific command
   actually issued, rather than normalizing all three into one generic "disabled" status.
10. **Stop and confirm with the operator before forcing a live-traffic-serving member into
    maintenance, drain, or a forced-down health state**, and before any `weight` change that would
    meaningfully shift live traffic distribution across a production backend.
11. **Server addressing for every Runtime API command in this procedure is
    `<backend-name>/<server-name>`** as a single positional argument — confirmed directly from the
    source's own worked examples.

### Remove a pool member / remove a backend or frontend

12. **Stop and confirm with the operator before any removal** — deleting a `frontend` stops accepting
    new connections at that VIP's bind address; removing the last/only server from a backend removes
    all serving capacity for anything routed to it.
13. **Remove via the Runtime API's `del server`** (for a dynamic server, without a reload) or by
    deleting the `server` line from the config file and reloading (steps 3-4) for a
    statically-defined one.

## Patterns

- **Config-file changes require a reload; Runtime API commands do not.** Prefer the Runtime API for
  any change that platform supports dynamically (adding/removing/draining a server, changing
  weight) to avoid an unnecessary reload of a live instance.
- **`disable server`, `set server ... state drain`, and `set server ... health down` are three
  distinct documented mechanisms**, not one — see step 9. Report using the specific one issued.
- **Server addressing is always `<backend>/<server>`** across every Runtime API command shown in the
  source (step 11).

## Known limitations

- HAProxy also offers a separate REST-based "Data Plane API" management layer for the same
  frontend/backend/server configuration, using a transactional POST/PUT/DELETE model. This
  procedure does **not** cover it — its reference documentation is served as a JS-rendered
  interactive page that could not be retrieved as page content in this research pass. A future
  contribution covering the Data Plane API specifically needs its own independent research pass
  (e.g. against its underlying OpenAPI/Swagger spec) rather than being inferred from this procedure.
- Exact parameter ranges/defaults for common `server`-line keywords (`weight`, `check`, `disabled`,
  `maxconn`) were not independently confirmed verbatim from a primary source in this pass (see step
  2) — confirm against the target HAProxy version's own current configuration manual before relying
  on anything beyond the bare `server <name> <address>:<port>` form and the Runtime API commands
  explicitly quoted above.
- The exact reload mechanism (init-system command, container orchestration action, or HAProxy's own
  seamless-reload flag) is deployment-specific and wasn't itself confirmed from a primary source in
  this pass — defer to the target environment's own operational runbook.
- Runtime API command syntax has changed across major HAProxy versions historically (general
  release-history awareness, not independently re-verified in this pass) — re-check the exact syntax
  against the target instance's own version before relying on it verbatim.
- Does not cover ACL-based routing rules, GSLB equivalents, or TLS certificate/profile provisioning
  (see `certificate-management` for the last of these).

## Tools

| Operation | Description | Category |
|---|---|---|
| Config file edit + reload | Add/remove/change a `frontend`, `backend`, or `server` line, then reload | Configuration |
| Runtime API — server state | `disable server` / `enable server` / `set server ... state|health|weight ...` | Runtime API (stats socket) |
| Runtime API — dynamic servers | `add server` / `del server` (add/remove a member without reload, where supported) | Runtime API (stats socket) |
| Runtime API — visibility | `show servers state` / `show backend` (confirm current live state) | Runtime API (stats socket) |

## Verification checklist

- [ ] Config-file changes confirmed applied via a successful reload (exit status/log check), not
      assumed in effect immediately on file save (steps 3-4)
- [ ] The specific state-change command actually issued (`disable server` vs. `set server ... state
      drain` vs. `set server ... health down` vs. a weight change) reported by name, not normalized
      into one generic "disabled" status (step 9)
- [ ] Operator confirmation obtained before draining/disabling/forcing-down a live member, changing
      weight meaningfully, or removing a frontend/backend/server from a production instance
- [ ] A dynamic-server Runtime API path (`add server`/`del server`) preferred over a config-file edit
      + reload where the target instance supports it, to avoid an unnecessary reload
- [ ] Any request specifically about the Data Plane API (not the config file / Runtime API surface)
      recognized as out of this procedure's confirmed scope (see Known limitations)
