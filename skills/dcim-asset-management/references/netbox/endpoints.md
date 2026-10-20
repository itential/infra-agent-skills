# Endpoints — NetBox DCIM Devices & Racks

Literal wiring for `procedure.md`. Paths are relative to the instance's own base URL
(`https://{netbox-host}/api/...`; host and any prefix are deployment-specific).

Sources: NetBox Labs REST API, Device and Rack documentation pages (retrieved 2026-10-19; see
`procedure.md`). Items marked "per assets spec" come from the Itential-authored OpenAPI copy in the
`itential/assets` repo and are secondary; confirm against the instance's own schema at `/api/schema/`.

## Authentication

`Authorization: Bearer nbt_<key>.<token>` for current tokens, or `Authorization: Token <token>` for
the deprecated plaintext tokens. Send `Content-Type: application/json` on writes.

## Racks

| Operation | Method and path | Notes |
|---|---|---|
| List | `GET /api/dcim/racks/` | Filters by field name; `limit`/`offset` paging; `brief=true` |
| Get | `GET /api/dcim/racks/{id}/` | Trailing slash required |
| Create | `POST /api/dcim/racks/` | Required per assets spec: `name`, `site`. Optional: `location`, `status`, `rack_type`, `u_height`, `starting_unit`, `desc_units`, `facility_id`, `serial`, `asset_tag` |
| Update | `PATCH /api/dcim/racks/{id}/` | Partial; `PUT` needs all mandatory fields |
| Delete | `DELETE /api/dcim/racks/{id}/` | 204 on success |

## Devices

| Operation | Method and path | Notes |
|---|---|---|
| List | `GET /api/dcim/devices/` | Filter by name, site, rack, status |
| Get | `GET /api/dcim/devices/{id}/` | Returns an `ETag` header |
| Create | `POST /api/dcim/devices/` | Required per assets spec: `device_type`, `role`, `site`. Optional: `name`, `rack`, `position`, `face`, `status`, `serial`, `asset_tag`, `location`, `tenant`, `platform` |
| Update | `PATCH /api/dcim/devices/{id}/` | Send `If-Match: <etag>` for optimistic locking; 412 on mismatch |
| Delete | `DELETE /api/dcim/devices/{id}/` | 204 on success |

Related objects: a numeric id, or an object of identifying attributes, e.g. `{"rack": 123}` or
`{"rack": {"site": {"name": "..."}, "name": "..."}}`.

## Bulk

`POST`, `PATCH`, `PUT` or `DELETE` on a collection path with a JSON array (updates and deletes carry
`id`). All-or-none transaction.

## Status codes

201 create, 200 read/update, 204 delete, 400 validation, 403 permission, 404 missing, 412 entity-tag
mismatch.
