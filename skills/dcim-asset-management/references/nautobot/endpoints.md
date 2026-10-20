# Endpoints — Nautobot DCIM Devices & Racks

Literal wiring for `procedure.md`. Paths are relative to the instance's own base URL
(`https://{nautobot-host}/api/...`).

Sources: Nautobot documentation, REST API Overview and Device/Rack data model pages (retrieved
2026-10-19; see `procedure.md`). Items marked "per assets spec" come from the Itential-authored OpenAPI
copy in `itential/assets` and are secondary.

## Authentication

`Authorization: Token <token>`; `Content-Type: application/json`; optionally
`Accept: application/json; version=<api version>`.

## Racks

| Operation | Method and path | Notes |
|---|---|---|
| List | `GET /api/dcim/racks/` | `limit`/`offset`, `sort`, `depth` |
| Get | `GET /api/dcim/racks/{id}/` | `{id}` is a UUID |
| Create | `POST /api/dcim/racks/` | Model page: name, location, type, status, height required |
| Update | `PATCH /api/dcim/racks/{id}/` | Partial; `PUT` needs all mandatory fields |
| Delete | `DELETE /api/dcim/racks/{id}/` | |

## Devices

| Operation | Method and path | Notes |
|---|---|---|
| List | `GET /api/dcim/devices/` | Filters per field |
| Get | `GET /api/dcim/devices/{id}/` | |
| Create | `POST /api/dcim/devices/` | Required: location, role, status, device type. Optional: name, rack, position, face, serial, asset tag, platform |
| Update | `PATCH /api/dcim/devices/{id}/` | Partial |
| Delete | `DELETE /api/dcim/devices/{id}/` | |

Related objects: UUID, natural key, or an object of identifying attributes, e.g.
`{"rack": {"location": {"name": "..."}, "name": "..."}}`.

## Bulk

`POST` with a list creates; `PATCH` and `DELETE` on a collection path with a list update or delete.
All-or-none.
