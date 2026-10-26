# Citrix ADC (NetScaler) — Virtual Server and Service/Binding CRUD Procedure

Creates, reads, updates, and deletes a load-balancing virtual server (`lbvserver`, the VIP
equivalent) and a service (a pool-member equivalent), and binds/unbinds a service to a virtual
server, on Citrix ADC / NetScaler via the NITRO REST API. Assumes an authenticated NITRO session or
per-call credential is already available. Does not cover content-switching virtual servers, GSLB,
rewrite/responder policy authoring, or SSL certificate provisioning (see `certificate-management`).

Source: NetScaler developer docs, NITRO API reference ("current-release" tree, mapped to ADC 14.1 at
retrieval time), https://developer-docs.netscaler.com/en-us/adc-nitro-api — specifically the
resource-operations guide, the basic load-balancing use case, the basic-operations (authentication)
guide, the disable-service use case, and the error-messages reference — retrieved 2026-09-17. Where
a fact (e.g. the `servicegroup` binding object's exact name) was inferred by extension of a
confirmed general naming pattern rather than found in a worked example, that is flagged below and in
`endpoints.md` rather than presented as directly sourced.

## Operational procedure

### Create a service (pool-member equivalent)

1. **Confirm the service doesn't already exist under the intended name** — NITRO identifies each
   service object by its own `name`, distinct from the backend address it targets; look it up first
   if there's any doubt, since this platform documents a specific rejection for a duplicate
   service on the same port and type (see `endpoints.md`).
2. **Build the service object** — set `name`, `ip` (the backend member's own address — note this
   field is named `ip` on a service object, not the same field name the virtual server uses for its
   own address), `servicetype` (e.g. `HTTP`, `TCP`), and `port`.
3. **Create the service.** See `endpoints.md` for the literal call. Treat a 2xx response as success;
   if the platform reports a duplicate-object condition (documented in this source's error catalog
   as "service exists with the same port and service type"), report that back rather than retrying
   blindly.

### Create a virtual server (VIP)

4. **Build the virtual server object** — set `name`, `servicetype`, `ipv46` (the VIP's own address —
   note the field name differs from the service object's `ip` field), and `port`.
5. **Create the virtual server.** See `endpoints.md`. Treat a 2xx response as success.
6. **Bind each service to the virtual server** — submit a binding object naming the virtual server
   and the service, plus an optional `weight` for load distribution. This is a separate call from
   creating either object — a virtual server with no bound services will accept connections per its
   own definition but have nothing to load-balance to, so confirm at least one binding succeeded
   before reporting the VIP fully provisioned.
7. **Confirm the binding** — read the virtual server's bindings back and confirm the intended
   service is present before reporting CREATED end-to-end.

### Read a virtual server or service

8. **Look up by name** — a single resource is retrieved by name in the URL path. If not found,
   report NOT_FOUND rather than an assumed-empty result.

### Update a virtual server or service

9. **Submit only the fields being changed**, addressing the specific resource by name. Confirm the
   response reflects the intended new value before declaring the change applied.

### Disable a service without deleting it (drain equivalent)

10. **Distinguish a graceful drain from an immediate disable** — this platform documents a
    `graceful` field (Yes/No) and a `delay` (seconds) on the disable action: with `graceful: Yes`,
    the service stops accepting new connections and finishes disabling only once existing
    connections close, and during the `delay` window new requests are only routed to the service if
    the requesting client already holds a persistent session there. Without `graceful: Yes` (or with
    it set to No), treat the disable as immediate rather than assuming a drain occurred.
11. **Stop and confirm with the operator before disabling a service serving live traffic**,
    especially a non-graceful disable, since that immediately removes serving capacity from
    whatever virtual server(s) the service is bound to.
12. **Re-enabling** — this source's disable-service page did not include the enable call's own
    worked example. By extension of the same action-query-parameter pattern used for disable, an
    enable action is expected to exist, but its exact call is Unverified — do not assert its literal form as documented; confirm the exact syntax against
    the target NetScaler's own current NITRO reference before relying on it, and report this gap
    rather than guessing at the payload shape if the calling tool needs to re-enable a service.

### Remove a binding / delete a service / delete a virtual server

13. **Stop and confirm with the operator before any delete** — deleting a virtual server stops
    accepting new connections at that VIP's address:port; deleting a service or unbinding it from
    all virtual servers removes it from every load-balancing decision that referenced it.
14. **Delete the target object or binding.** See `endpoints.md`. Treat a 2xx/success response as
    confirmation; if the platform rejects the delete (e.g. an object still in use elsewhere), report
    the failure verbatim — this source's error catalog does not list every possible
    still-in-use rejection string, so don't fabricate one.

## Patterns

- **The VIP's own address field (`ipv46` on `lbvserver`) and a member's own address field (`ip` on
  `service`) use different field names on this platform** — do not conflate them when building
  either payload.
- **Binding is always a separate call from creating either endpoint of the binding.** A virtual
  server or service can exist with zero bindings; don't assume creating one implies the other is
  wired up.
- **`servicegroup` is a documented alternative to individual `service` objects** for grouping many
  backend members under one named group with its own member-binding sub-resource — this procedure
  covers only the plain `service`/`lbvserver` model; the
  `servicegroup` variant's exact binding object name and fields are Unverified, with no worked example (see `endpoints.md`). Treat `servicegroup` as a known gap, not as covered by this procedure.

## Known limitations

- Grounded in the plain `service` + `lbvserver` + `lbvserver_service_binding` model only — the
  `servicegroup` object (and its own member sub-binding) is a documented alternative on this
  platform for larger member pools, but is Unverified, with no worked example. Do not extend this procedure to `servicegroup` calls.
- Two different authentication mechanisms are both documented for this platform (a session login
  returning a cookie-based token, and a per-call header-based credential pair) but one documented worked example uses a generic HTTP Basic Auth flag in a way that isn't clearly reconciled with the
  header-based mechanism as described elsewhere in the same source — see `endpoints.md`'s
  Authentication section. Confirm which mechanism the target environment actually expects before
  scripting against it.
- Re-enabling a disabled service is Unverified, with no worked example (step 12) —
  treat the exact call as unverified until confirmed against the target NetScaler's own reference.
- Does not cover content-switching virtual servers, GSLB, rewrite/responder policy binding, or SSL
  certificate/profile provisioning (see `certificate-management` for the last of these).

## Tools

| Operation | Description | Category |
|---|---|---|
| Service CRUD | Create/read/update/delete a `service` object (pool-member equivalent) | NITRO Configuration |
| Virtual server CRUD | Create/read/update/delete an `lbvserver` object | NITRO Configuration |
| Binding management | Bind/unbind a service to/from a virtual server | NITRO Configuration |
| Service disable/enable | Change a service's admin state, with optional graceful drain | NITRO Configuration |

## Verification checklist

- [ ] Duplicate-service check considered before create, given this platform's documented
      same-port-and-type rejection (step 1)
- [ ] Correct address field used for each object type — `ipv46` for the virtual server, `ip` for the
      service — not conflated
- [ ] Binding created and read back to confirm the intended service is actually attached to the
      virtual server before reporting the VIP fully provisioned (steps 6-7)
- [ ] `graceful`/`delay` semantics correctly applied and reported when disabling a service, not
      assumed to be an immediate hard stop unless that's what was actually requested/set (step 10)
- [ ] Operator confirmation obtained before any disable-with-live-traffic, delete, or unbind of a
      production object
- [ ] Any `servicegroup`-based request recognized as out of this procedure's confirmed scope and
      flagged rather than handled as if it were a plain `service` (see Known limitations)
