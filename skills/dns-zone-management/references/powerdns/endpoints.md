# Endpoint Wiring — PowerDNS Authoritative Server DNS Zone Management

Literal API calls behind each capability named in `procedure.md`. All calls are the PowerDNS
Authoritative Server HTTP API's Zones resource, JSON request/response bodies, authenticated with an
`X-API-Key` header. Source: doc.powerdns.com Authoritative Server HTTP API reference, retrieved
2026-09-17. Exact field and error completeness is unverified; see `procedure.md`'s Known
limitations for specifics.

## Create a Zone

Tool hint: Create Zone (Zones resource, create operation).

Literal route: `POST /servers/{server_id}/zones`

Body fields (documented):

| Field | Notes |
|---|---|
| `name` | Zone name, trailing dot. |
| `kind` | `Native` confirmed; a full current enum (e.g. `Master`/`Slave` roles) was not independently verified — check the target instance's own schema. |
| `masters` | Empty array for a self-managed primary zone; populated with primary server addresses for a secondary zone. |
| `nameservers` | Array of authoritative name server hostnames used to seed the zone's initial NS RRset. |

Query parameter: `rrsets` (boolean, default `true`) — whether the response body includes the
generated RRsets.

Response (201 Created): the created zone object, including the auto-generated SOA and NS RRsets (if
`rrsets` was left `true`).

Errors: a default JSON error-object response on failure; no specific error code/string is documented
— report whatever literal error body the server returns.

## Retrieve a Zone

Tool hint: Retrieve Zone (Zones resource, get-by-id operation).

Literal route: `GET /servers/{server_id}/zones/{zone_id}`

`zone_id` is typically the zone's name (with trailing dot).

Query parameters: `rrsets` (default `true`), `record_count` (default `false`), `rrset_name` (filter to
one record name), `rrset_type` (filter to one type, requires `rrset_name`), `include_disabled`
(default `true`).

Response (200 OK): the zone object.

## List Zones

Tool hint: List Zones (Zones resource, list operation).

Literal route: `GET /servers/{server_id}/zones`

Query parameters: `zone` (filter to one zone name — returns an empty array if no such zone exists),
`dnssec` (default `true`; setting to `false` is documented as improving query performance by omitting
DNSSEC-related fields from the response).

Response (200 OK): array of zone objects.

## Update a Zone

Tool hint: Update Zone (Zones resource, update operation).

Literal route: `PUT /servers/{server_id}/zones/{zone_id}`

Body: any of the confirmed-changeable fields — `kind`, `masters`, `catalog`, `account`, `soa_edit`,
`soa_edit_api`, `api_rectify`, `dnssec`, `nsec3param`. Fields outside this set are ignored rather than
applied or rejected.

Response: `204 No Content` on success.

Errors: `422 Unprocessable Entity` when the requested change itself is invalid (exact trigger
conditions not documented); a default JSON error-object response for other malformed
input.

## Delete a Zone

Tool hint: Delete Zone (Zones resource, delete operation).

Literal route: `DELETE /servers/{server_id}/zones/{zone_id}`

No request body. Removes the zone's own configuration/metadata and every RRset it contains.

Response: `204 No Content` on success.

Errors: a default JSON error-object response on failure; no specific error code/string is documented,
and no "zone must be empty first" precondition is documented either — see
`procedure.md`'s Known limitations.

## Notify Zone

Tool hint: Notify Zone.

Literal route: `PUT /servers/{server_id}/zones/{zone_id}/notify`

No request body confirmed. Meaningful for a primary (`Master`-role) zone, or a secondary zone with
re-notify enabled.

Response: `200 OK` on success; error response otherwise (exact error shape not confirmed).

## Export Zone

Tool hint: Export Zone.

Literal route: `GET /servers/{server_id}/zones/{zone_id}/export`

Response: `200 OK`, body is the zone's contents in zone-file/AXFR text form (not JSON).

## Trigger a Zone Transfer (secondary zones)

Tool hint: Retrieve Slave Zone / axfr-retrieve.

Literal route: `PUT /servers/{server_id}/zones/{zone_id}/axfr-retrieve`

Body: optionally, a specific primary server address to pull from instead of the zone's already
configured one(s).

Response: not documented beyond that it triggers an immediate transfer attempt
for a secondary zone — behavior against a non-secondary zone is unconfirmed (see `procedure.md`'s
Known limitations).

## Field reference (zone-level fields only)

| Field | Location | Notes |
|---|---|---|
| `name` | Create request, response | Zone name, trailing dot. |
| `kind` | Create/Update request, response | `Native` confirmed; full enum unconfirmed. |
| `masters` | Create/Update request, response | Primary server addresses for a secondary zone. |
| `nameservers` | Create request | Seeds the zone's initial NS RRset; not itself a field on the returned zone object as an editable list post-creation. |
| `account` | Update request, response | Free-text account identifier. |
| `soa_edit` / `soa_edit_api` | Update request, response | Controls automatic SOA serial handling; exact semantics of specific values not independently confirmed. |
| `api_rectify` | Update request, response | Whether PowerDNS auto-rectifies DNSSEC data after API-driven RRset changes (see `dns-record-management`'s PowerDNS procedure). |
| `dnssec` | Update request, response | Whether DNSSEC signing is enabled for the zone. |
| `nsec3param` | Update request, response | DNSSEC NSEC3 parameters. |
| `serial` / `notified_serial` | Response only | Server-managed; not accepted in request bodies. |
