# Endpoints — Akamai Edge DNS Record Sets

Wiring layer for `procedure.md`. Source: Akamai TechDocs Edge DNS API v2 reference, retrieved 2026-10-19.

**Base path:** `https://{host}/config-dns/v2` — not confirmed on the vendor reference pages (unverified). `{host}` is the account's EdgeGrid API hostname (placeholder).
Requests are signed with EdgeGrid. Bodies and responses are JSON.

**Common:** optional query parameter `accountSwitchKey` selects another account for multi-account users.
Errors follow RFC 7807 problem details.

## Get record set

`GET /zones/{zone}/names/{name}/types/{type}` — `name` is the full name including the zone, e.g.
`www.example.com`. 200 returns `name`, `type`, `ttl` (0 means uncached) and `rdata` (array of strings).
Errors: 401 (not logged in), 404 (zone or record set missing, e.g. "Zone not found: example.com").

## Create record set

`POST /zones/{zone}/names/{name}/types/{type}` — body requires `name`, `type`, `ttl` (integer, 0 or more)
and `rdata` (array; each string is one record's data in master file format). Success: 201 with the record
set and a `Location` header. Errors: 400, 401, 404, 409 (already exists), 412 (concurrency tag mismatch),
415 (needs `application/json`), 422 (semantically invalid, e.g. TTL out of range).

## Replace record set

`PUT /zones/{zone}/names/{name}/types/{type}` — same body as create; `name` and `type` must match an
existing set. Success: 200 with the replaced set. Errors: 400, 401, 404, 409, 412, 415, 422. The 412 text is
"If-Match header does not match current ETag".

## Delete record set

`DELETE /zones/{zone}/names/{name}/types/{type}` — success 204, empty body. Errors: 401, 404, 412.

## Concurrency tag

The 412 responses refer to an `If-Match` header holding the current ETag. Which responses return the ETag
and whether it is required is not stated in the pages read (unverified).
