# Endpoints — Prisma SD-WAN site snapshots (unified API)

Literal wiring layer for `procedure.md`. Operation names in its Tools table map to the calls below.

Written against the Prisma SD-WAN unified API specification (version listed as "Latest"), checked
2026-10-14, and the Prisma SD-WAN Administrator's Guide (2026 edition). Every snapshot route in the
specification exists only in the `v2.0` form, which is therefore the newest available; no newer route
version for these operations is listed. Values are placeholders.

## Base and authentication

Gateway host (from the specification's server entry): `https://api.sase.paloaltonetworks.com`. Routes
below are relative to it.

Authentication is a bearer token from the Prisma SASE token endpoint using a service account, with a
scope naming the tenant service group. The specification states that right after minting a token, one
call to the profile route (`GET /sdwan/v2.1/api/profile`) must be made, or later SD-WAN calls return
403. The specification says tokens last about 15 minutes; re-mint (and repeat the profile read) if a long poll outlives the token.

Errors: a 400 response carries an `_error` array of entries with `code` and `message`. Other statuses
are not documented for these routes; treat them as FAILED and report the status and body.

## generate_site_snapshot

```
POST /sdwan/v2.0/api/sites/{site_id}/snapshots
Content-Type: application/json
```
Body fields (all optional in the schema): `snapshot_name`. Other schema fields (`id`, `_etag`) are generic
and ignored on create. Response 200: `id` (the job identifier), `snapshot_name`, `site_id`, `status`,
`status_description`.

Documented 400 error codes (names from the specification's example; meanings are inferred from the names): `INVALID_JSON`, `SITE_ID_REQUIRED`, `INVALID_SITEID`, and `EXPORT_ALREADY_IN_PROGRESS` (assumed: a capture for this site is already running; wait for it).

Known error text (from the guide): export is refused on a site with an element shell; the message reads
"Export Snapshot not allowed on the site having element shell". Match on it to report NOT_ALLOWED. Whether
it arrives as a 400 entry is an assumption.

## read_snapshot_job_status

```
GET /sdwan/v2.0/api/sites/{site_id}/snapshots/{id}/status
```
`id` is the job identifier from the create response. Response 200: `id`, `status`, `status_description`.

## retrieve_snapshot_yaml

```
GET /sdwan/v2.0/api/sites/{site_id}/snapshots/{id}
```
Response 200: `id`, `snapshot_name`, `site_id`, `status`, `status_description`, `yaml_configuration` (the
file as a string).

## query_snapshot_exports

```
POST /sdwan/v2.0/api/sites/snapshots/query
Content-Type: application/json
```
Body is the platform's generic query object (for example `limit`, `dest_page`, `query_params`,
`sort_params`, `retrieved_fields`). The specification gives no accepted values for the filter and sort
objects; the exact shape is unverified. The specification's 400 example for the sibling redeploy-list route is an empty-input error (`INPUT_JSON_EMPTY`), so an empty body may be rejected: send at least one paging field such as `limit`. This route's own 400 example is `INVALID_REQUEST_PARAM`.
Response 200: `items` (each with `id`, `snapshot_name`, `site_id`, `status`, `status_description`,
`yaml_configuration`), plus `count`, `total_count`, and `next_query` for paging.

## create_site_deployment

```
POST /sdwan/v2.0/api/sitesnapshots
Content-Type: application/json
```
Body: `yaml_configuration` (the YAML text as a string). The specification describes the call as create or
retry of a site deployment. Response 200: `id` (job identifier), `yaml_name`, `yaml_configuration`,
`status`, `status_description`.

Documented 400 error codes (names only, meanings inferred): `INVALID_JSON`, `EXPORT_ALREADY_IN_PROGRESS`, `INVALID_YAML_NAME`, `INVALID_YAML`, `YAML_SYNTAX_INVALID`, `RESOURCE_VERSION_UNSUPPORTED`, `SITES_NOT_FOUND`, `SITES_COUNT_INVALID`, `SITE_ADDRESS_MISSING`.

## read_site_deployment

```
GET /sdwan/v2.0/api/sitesnapshots/{id}
```
Response 200: `id`, `yaml_name`, `status`, `status_description`.

## query_site_deployments

```
POST /sdwan/v2.0/api/sitesnapshots/query
Content-Type: application/json
```
Same generic query body as `query_snapshot_exports`. The specification's 400 example for this route is `INPUT_JSON_EMPTY`, so send at least one paging field such as `limit`. Response 200: `items` (each with `id`, `yaml_name`,
`status`, `status_description`), plus paging fields.

## Not bound

The bulk configuration-state query routes in the specification report configuration state for sites,
elements, networks, and policy sets; they are not snapshot operations and no step here uses them.
