# Endpoint Mapping — NetBox IPAM Prefix Allocation

Literal NetBox REST API operations behind each capability named in `SKILL.md`. Bind these to a concrete
tool (e.g. a FlowAI-discovered adapter tool, a direct REST call). Sourced from NetBox's own OpenAPI
schema (`/api/schema/`, v4.6.7).

| Capability (SKILL.md) | Operation | Body / notes |
|---|---|---|
| Create an aggregate (top-level block) | `POST /api/ipam/aggregates/` | Body: `{"prefix": "<cidr>", "rir": <rir_id>}` — both required. |
| Create a prefix directly | `POST /api/ipam/prefixes/` | Body: `{"prefix": "<cidr>", "status": "container"|"active"|"reserved"|"deprecated", ...}` — only `prefix` required. |
| List available child prefixes | `GET /api/ipam/prefixes/{id}/available-prefixes/` | No body. `{id}` = parent prefix's NetBox ID. Returns array of not-yet-existing candidate prefixes. |
| Allocate (carve out) a child prefix | `POST /api/ipam/prefixes/{id}/available-prefixes/` | Body: `{"prefix_length": <int>}` — **required**, no default. Accepts an array for bulk allocation. Returns full `Prefix` record(s), not the reduced candidate shape. |
| List available IPs in a prefix | `GET /api/ipam/prefixes/{id}/available-ips/` | No body. Returns up to the pagination limit — not a full enumeration for large prefixes. |
| Allocate the next available IP | `POST /api/ipam/prefixes/{id}/available-ips/` | Body: `{"prefix_length": <int>}` — **optional**, defaults to the prefix's own mask if omitted. Accepts an array for bulk allocation. |

## Auth / headers

`Authorization: Bearer nbt_<key>.<token>` (v2, recommended) or `Authorization: Token <token>` (v1
legacy). `Content-Type: application/json` on all writes.

## Documented/observed error signal for pool exhaustion

`available-ips` and `available-prefixes` POST return **HTTP 400** (not 404/409) when the pool can't
satisfy the request, with a body message matching: *"An insufficient number of IP addresses are
available within `<prefix>` (`<N>` requested, `<M>` available)."* Source: NetBox community/issue-tracker
corroboration, not the OpenAPI schema itself (schemas don't carry response-body prose) — this is a
secondary-sourced fact, not independently confirmed against the schema.
