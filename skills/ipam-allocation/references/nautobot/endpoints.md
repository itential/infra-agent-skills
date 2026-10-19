# Endpoint Mapping — Nautobot IPAM Allocation

Literal Nautobot REST operations behind the capabilities in `procedure.md`. **Secondary source:** Nautobot's
generated OpenAPI schema v2.4.14 as copied into the Itential `assets` repository (retrieved 2026-10-19);
Nautobot's own hosted API docs were not reachable. All rows are therefore *(unverified)* against a live
instance; confirm on the target instance's `/api/docs/`.

| Capability | Operation | Notes |
|---|---|---|
| List available child prefixes | `GET /api/ipam/prefixes/{id}/available-prefixes/` | `{id}` is the parent prefix ID. |
| Allocate child prefix | `POST /api/ipam/prefixes/{id}/available-prefixes/` | Body requires `prefix_length` and `status`; optional `type`, `role`, `location`, `tenant`, `vlan`, `rir`, `description`, `tags`. |
| List available IPs | `GET /api/ipam/prefixes/{id}/available-ips/` | Query `limit`, `offset`, `range_start`, `range_end`. |
| Allocate next available IP | `POST /api/ipam/prefixes/{id}/available-ips/` | Body requires `status`; optional `dns_name`, `description`, `role`, `tenant`, `tags`. Schema also allows an array body *(unverified)*. |

## Auth / headers

`Authorization: Token <token>` (the schema describes the `Token` prefix). `Content-Type: application/json`
on writes. Base URL is the instance's own host (placeholder: `https://nautobot.example.com`).

## Error signals

Exhaustion message string: not documented in the sources — unknown. A missing `status` is reported by a
tracker issue as HTTP 400 with a "This field is required" message *(secondary, unverified)*.
