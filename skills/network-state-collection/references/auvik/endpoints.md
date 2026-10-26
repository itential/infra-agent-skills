# Auvik — State Collection Wiring

Source: Auvik API v1 OpenAPI specification (retrieved 2026-10-26); procedure in [procedure.md](procedure.md). Placeholders: `{base_url}`, `{username}`, `{api_key}`, `{tenant_ids}`, `{device_id}`.

## Authentication and base URL

HTTP Basic with the Auvik username and that user's API key as the password; the user's role must permit the reads. The specification's server entry is the `us1` host (`https://auvikapi.us1.my.auvik.com`). Assumption: other regions use a matching regional host, which the specification does not state; take the base URL from the account's region. Responses use the JSON:API media type.

## Calls

| Operation | Method and path | Notes |
|---|---|---|
| Verify credentials | `GET /v1/authentication/verify` | 200 valid, 401 invalid |
| Resolve tenants | `GET /v1/tenants` | 400, 403, 404, 500 possible |
| Read device info | `GET /v1/inventory/device/info` | Filters: `filter[networks]`, `filter[deviceType]`, `filter[makeModel]`, `filter[vendorName]`, `filter[onlineStatus]`, `filter[modifiedAfter]`, `filter[notSeenSince]`, `filter[stateKnown]`; `tenants` (comma-separated tenant IDs); `include=deviceDetail`, `fields[deviceDetail]` |
| Read one device info | `GET /v1/inventory/device/info/{device_id}` | |
| Read device detail | `GET /v1/inventory/device/detail` and `/{device_id}` | |
| Read extended detail | `GET /v1/inventory/device/detail/extended` and `/{device_id}` | `filter[deviceType]` is required on the collection; also `filter[modifiedAfter]`, `filter[notSeenSince]`, `filter[stateKnown]`, `tenants` |
| Networks, interfaces, components | `GET /v1/inventory/network/info`, `/v1/inventory/interface/info`, `/v1/inventory/component/info` | Filters: `filter[networkType]`, `filter[scanStatus]`, `filter[devices]` (networks); `filter[interfaceType]`, `filter[parentDevice]`, `filter[adminStatus]`, `filter[operationalStatus]` (interfaces); `filter[deviceId]`, `filter[deviceName]`, `filter[currentStatus]` (components); all accept `filter[modifiedAfter]` and `tenants` |

Paging parameters on lists: `page[first]` with `page[after]`, or `page[last]` with `page[before]` (default size 100 on device lists). `filter[onlineStatus]` values: online, offline, unreachable, testing, unknown, dormant, notPresent, lowerLayerDown.

## Error responses

| Status | Meaning in the specification |
|---|---|
| 400 | Bad request |
| 401 | Credentials invalid (verify call) |
| 403 | Forbidden; may also reflect an IP-level block (unverified, see procedure Patterns) |
| 404 | Not found |
| 500 | Something went wrong |
