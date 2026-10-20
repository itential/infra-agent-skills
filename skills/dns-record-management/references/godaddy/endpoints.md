# Endpoints — GoDaddy DNS Records (Domains API v1)

Wiring layer for `procedure.md`. Source: GoDaddy Developer documentation, Domains v1 REST reference,
retrieved 2026-10-19.

**Base URL:** `https://api.godaddy.com` — (unverified: not stated on the pages read; confirm in the vendor's
introduction). Bearer-token authentication. JSON bodies need `Content-Type: application/json`.
Optional header `X-Shopper-Id` is needed only by resellers managing domains outside their own account.

## Add records

`PATCH /v1/domains/{domain}/records` — body is an array of record objects. Success 204. Errors 400, 401,
403, 404, 422, 429, 500, 504.

## Replace records by type and name

`PUT /v1/domains/{domain}/records/{type}/{name}` — body is an array of records; others preserved.
Success 200 (or 204, see the page's inconsistency). Errors 400, 401, 403, 404, 422, 429, 500, 504.

## Replace records by type

`PUT /v1/domains/{domain}/records/{type}` — replaces all records of that type across all names. Success 204.
Same error set.

## Delete records by type and name

`DELETE /v1/domains/{domain}/records/{type}/{name}` — deletes all records matching type and name. Success
204. Errors 400, 401, 403, 404, 409 (domain ineligible for record changes), 422, 429, 500, 504.

## Get records

`GET /v1/domains/{domain}/records/{type}/{name}` — path not confirmed on a vendor page
(unverified). Response shape not confirmed.

## Not covered

The root-level replace-all call and the nameserver endpoint are deliberately excluded.
