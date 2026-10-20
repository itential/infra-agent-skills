# Endpoint Wiring — Aruba ClearPass Endpoint Repository

Literal API calls behind each operation named in `procedure.md`. JSON bodies over HTTPS, base
`https://<clearpass-host>/api`, bearer token in the `Authorization` header (`Bearer <token>`).

Sources: HPE Aruba Networking Developer Hub, ClearPass Policy Manager API reference
(developer.arubanetworks.com/cppm/reference/...), retrieved 2026-10-19. The operation set was
scoped with the endpoint workflows and OpenAPI file in the Itential assets repository (a secondary
source used only to choose operations; every field below was read from the vendor pages).

## Obtain a token (out of scope for the procedure, listed for binding)

`POST /oauth` — body: `grant_type` (client_credentials, password, or refresh_token), `client_id`,
`client_secret` (unless the client is public), `username`/`password` for the password grant,
`refresh_token` for the refresh grant, optional `scope`. Response: `access_token`, `token_type`
(always Bearer), `expires_in`, optional `refresh_token`, `scope`. Errors: 400, 406, 415.

## List endpoints

`GET /endpoint` — query: `filter` (JSON, default `{}`), `sort` (default `+id`), `offset` (default 0),
`limit` (default 25, 1–1000), `calculate_count`, `profile_details` (required, default false),
`nad_details` (required, default false). Errors: 401, 403, 406, 415, 422.

## Read endpoint

`GET /endpoint/mac-address/{mac_address}` — query: `profile_details`, `nad_details` (both required,
default false). Errors: 401, 403, 404, 406, 415.
`GET /endpoint/{endpoint_id}` — by numeric id (assumed same shape; not separately read).

## Create endpoint

`POST /endpoint` — body: `mac_address` and `status` (required; Known, Unknown, Disabled), optional
`description`, `randomized_mac`, `device_insight_tags`, `attributes`. Response 201 with the endpoint
record. Errors: 401, 403, 406, 415, 422.

## Update endpoint

`PATCH /endpoint/mac-address/{mac_address}` — body fields (all optional): `mac_address`,
`description`, `status`, `randomized_mac`, `device_insight_tags`, `attributes`, `profile`
(only `device_category`, `device_os_family`, `device_name` writable). Response 200 (record) or 204.
Errors: 304, 401, 403, 404, 406, 415, 422.
`PATCH /endpoint/{endpoint_id}` — by id; the same fields minus `profile`.

## Replace endpoint

`PUT /endpoint/mac-address/{mac_address}` — body requires `mac_address`, `status`, and a `profile`
object carrying all three writable profile fields. Response 200 or 204. Errors: 304, 401, 403, 404,
406, 415, 422.

## Delete endpoint

`DELETE /endpoint/mac-address/{mac_address}` — response 204, no body. Errors: 401, 403, 404, 406, 415.
`DELETE /endpoint/{endpoint_id}` — by id (assumed same shape; not separately read).
