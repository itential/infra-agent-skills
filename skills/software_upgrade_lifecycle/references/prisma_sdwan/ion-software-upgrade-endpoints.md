# Endpoints — Prisma SD-WAN ION device software upgrade

Literal wiring layer for `ion-software-upgrade.md`. Operation names in its Tools table map to the
routes below.

Written against the Prisma SD-WAN unified API specification (version labelled "Latest") and the
Prisma SD-WAN Administrator's Guide (last revised August 11, 2026), checked 2026-10-14. Route versions
are the newest the specification lists for each route. Values are placeholders.

## Base address and authentication

The specification names one gateway for all calls: the Prisma SASE API gateway at
`https://api.sase.paloaltonetworks.com`. Paths below are appended to it.

Authentication is a service-account token obtained with the client-credentials grant from the Prisma
SASE authentication service. The token request uses HTTP Basic with the client identifier and secret,
and the requested scope must name the tenant service group as `tsg_id:<TSG_ID>`. The specification's
token route is `POST /oauth2/access.token`, served by the authentication host
`auth.apps.paloaltonetworks.com` (declared as an operation-level server on the token route; assumption: still
current). The specification says tokens last about 15 minutes; re-mint (and repeat the profile call)
if a long upgrade poll outlives the token.

The calls carry the token as a bearer token. Quirk stated by the specification: immediately after
minting a token, call `GET /sdwan/v2.1/api/profile` once; without it, later SD-WAN calls return 403.

Rate limits and retry guidance are not stated (unknown). Back off on HTTP 429 and honor any
`Retry-After` header.

Every write body carries the record's `_etag` (object version), which must match the latest read.
Error bodies return `_error`, a list of `{code, message}`.

## get_element / list_elements

```
GET /sdwan/v3.2/api/elements/{element_id}
GET /sdwan/v3.2/api/elements
POST /sdwan/v3.2/api/elements/query
```
Fields used by the procedure: `id`, `name`, `model_name`, `serial_number`, `software_version`,
`site_id`, `role`, `state`, `connected`, `spoke_ha_config`, `cluster_id`. The query route takes the
generic query body (`limit`, `dest_page`, `query_params`, `retrieved_fields`, `sort_params`); its
accepted filter field names are not listed (unknown), so list and match locally when unsure. The meaning
of `state` values is not described in the specification (unknown). `spoke_ha_config` holds `track`, `source_interface`, `priority` (integer, 1 to 254), `enable`, and `cluster_id`; it has no preemption field.

## list_element_images / get_element_image

```
GET /sdwan/v2.4/api/element_images
GET /sdwan/v2.4/api/element_images/{machine_image_id}
```
Item fields: `id`, `version`, `state`, `type`, `is_lts`, `recommended_release`, `eol_date` (date,
year-month-day), `fips_certified`, `fips_certification_valid`, `release_url`, `ml7_version`, and
`model_software_map` (a list of entries with `model`, `bundle_name`, `security_caps`). The image `id` is
the value sent as `image_id` when scheduling. Allowed values for `state` and `type` are not listed
(unknown).

## get_element_software_state

```
GET /sdwan/v2.0/api/elements/{element_id}/software/state
```
Returns the device's upgrade configuration: `image_id`, `scheduled_download`, `download_interval`,
`scheduled_upgrade`, `upgrade_interval`, `interface_ids`, `_etag`, `id`.

## update_element

```
PUT /sdwan/v3.2/api/elements/{element_id}
```
Used only to change `spoke_ha_config.priority`. The body is the element record (with `_etag`); whether a partial body is
accepted is not stated, so send the full record from the latest read (assumption).

## update_element_software_state

```
PUT /sdwan/v2.0/api/elements/{element_id}/software/state
```
| Field | Notes |
|---|---|
| `image_id` | Digits only, 1 to 30 characters; the image `id` from the images read |
| `scheduled_download` | `MM-DD-YYYY HH:MM:SS`, 24-hour clock. Time zone not stated (unknown) |
| `download_interval` | Integer 0 to 59 (minutes). Accepted only with a valid download time |
| `scheduled_upgrade` | Same format as the download time |
| `upgrade_interval` | Integer 0 to 59 (minutes). Accepted only with a valid upgrade time |
| `interface_ids` | Up to 4 interface identifiers, no duplicates; empty allowed |
| `_etag` | From the latest read of the configuration |

Intent mapping (the guide describes the behavior; field-level mapping is inferred from the schema and
marked as assumption): both times omitted means download then install immediately; download time only
means download only; upgrade time with or without a download time means a timed install. Whether an
update with a new schedule replaces a pending one, and how an already-downloaded image is installed,
are not stated (assumption).

Documented `_error` codes on 400: `SOFTWARE_CONFIG_INVALID_SCHEDULING`,
`SOFTWARE_CONFIG_INVALID_SCHEDULING_AFTER_EOL_DATE`, `SOFTWARE_CONFIG_SCHEDULED_UPGRADE_NOT_SUPPORTED`,
`SOFTWARE_CONFIG_INVALID_DOWNLOAD_INTERVAL`, `SOFTWARE_CONFIG_INVALID_UPGRADE_INTERVAL`,
`SOFTWARE_CONFIG_INVALID_DOWNLOAD_TIME`, `SOFTWARE_CONFIG_INVALID_UPGRADE_TIME`,
`SOFTWARE_CONFIG_INCOMPATIBLE_SCHEDULES`, `SOFTWARE_CONFIG_INVALID_INTERFACES`,
`INVALID_JSON_EXTRA_ATTRIBUTE`, `INVALID_JSON_COMMON_ATTR_MISMATCH`, `INVALID_VERSION_FORMAT`. The
schema's field patterns also name `ELEMENT_STATE_UPDATE_INVALID_IMAGE` (image id) and
`ELEMENT_STATE_UPDATE_INVALID_TIME` (time fields); they are not in the 400 example list, so that they
surface as error codes is an assumption. The
specification gives only the code names, not explanations; the procedure reads them by name (for
example, the end-of-life code means the chosen time is after the image's end-of-life date; the
scheduled-upgrade-not-supported code is consistent with a device on a release before 5.1.1 — inference).

## get_element_software_status

```
GET /sdwan/v2.1/api/elements/{element_id}/software/status
```
Returns up to five status records for operations started by the tenant user. Fields:
`upgrade_state`, `download_percent`, `failure_info`, `active_version`, `active_image_id`,
`upgrade_image_id`, `rollback_version`, `previous_image_id`, `scheduled_download`, `download_interval`,
`scheduled_upgrade`, `upgrade_interval`, `software_version_change_time`, `id`.

`upgrade_state` values listed by the specification: `pending`, `init`, `discovery`, `download`,
`download_init`, `download_complete`, `download_scheduled`, `download_abort`, `download_cancelled`,
`download_cancel_pending`, `upgrade`, `upgrade_init`, `upgrade_complete`, `upgrade_scheduled`,
`upgrade_abort`, `upgrade_cancelled`, `upgrade_cancel_pending`, `upgrade_failed`, `upgrading`, `verify`,
`in-progress`, `install`, `complete`, `done`, `failed`, `download_discovery`, `download_failed`,
`downloading`, `install_failed`, `installing`, `verifying`, `waiting_download_time`,
`waiting_install_time`, `abort_upgrade_pending`, `abort_download_pending`, `invalid`.

An older version of the same read exists at `/sdwan/v2.0/api/elements/{element_id}/software/status`
(described only as an image status read); use the newer one.

## query_element_software_current_status

```
POST /sdwan/v2.1/api/software/current_status/query
```
Generic query body (see the elements query above). Returns the current status of every device with the
status fields above plus `element_id`. Accepted filter fields are not listed (unknown); page with
`limit`, `dest_page`, and `next_query`, and match `element_id` locally.

## query_element_software_status

```
POST /sdwan/v2.1/api/software/status/query
```
Same body and paging; described as the upgrade status of all devices of the tenant.

## query_software_download_history

```
POST /sdwan/v2.0/api/softwarehistory/query
```
Generic query body; returns the tenant's past software downloads. The item fields are not described in
the specification (unknown), so read the response as opaque history evidence.

## Out of scope but listed by the specification

Machine-level (unclaimed device) software routes exist under `/sdwan/v2.0/api/machines/{machine_id}/
software` and its `status` children, plus `machine_upgrade/query` and `upgrade_status/query`. The
update route lists an error whose name suggests it rejects claimed devices (inference), and the guide's
procedure covers claimed devices only, so the procedure does not use them. If a device is unclaimed,
report that this procedure does not cover it.
