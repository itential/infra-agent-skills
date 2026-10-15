# Endpoints — Prisma SD-WAN, branch site onboarding (site template)

Literal wiring layer for `procedure.md`. Operation names in the procedure's Tools table map to the
calls below.

Written against the Prisma SD-WAN Unified APIs OpenAPI specification (version label "Latest") and the
Prisma SD-WAN Administrator's Guide (last revised 2026-08-11), checked 2026-10-14. Each route is pinned
to the newest version the specification lists for that resource. Shapes are restated with placeholder
values.

## Base URL and versioning

Calls go to the Prisma SASE API gateway host named in the specification's server entry
(`<api_gateway_host>`), with the version in the path: `/sdwan/v<major>.<minor>/api/...`.
Resource families sit at different versions; the version in each route below is the newest listed for that
family (templates, deployments, site status, element operations, and allocate-to-shell are only listed at
2.0). Request bodies carry `_etag` for updates and ignore it on creation.

## authenticate

Per the specification's description (unverified against live behavior):
1. `POST /oauth2/access.token` on the SASE authentication host (`<auth_host>`),
   HTTP Basic with the service-account client id and secret, scope `tsg_id:<tsg-id>`. Tokens last about
   15 minutes.
2. Send `Authorization: Bearer <token>` on every call.
3. The specification says a profile read should follow token minting, or later SD-WAN calls return 403:
   `GET /sdwan/v2.1/api/profile`.

Whether tokens refresh is not stated; mint a new one when a call is rejected after a long gap.

## query_templates

```
POST /sdwan/v2.0/api/bulkconfigurations/sitetemplates/query
```
Body is the common query object (`limit`, `dest_page`, `query_params`, `sort_params`, `retrieved_fields`,
`total_count`, `next_query`). The `query_params` content for filtering by name is not documented
(assumption: field-name keys, as in the platform's other query calls); if a filter fails, list all and
match the name client-side. The deployments counterpart, which lists deployment records, is
`POST /sdwan/v2.0/api/bulkconfigurations/sitetemplates/deployments/query`.

## read_template

```
GET /sdwan/v2.0/api/bulkconfigurations/sitetemplates/{site_template_id}
GET /sdwan/v2.0/api/bulkconfigurations/sitetemplates/{site_template_id}/status
```
Template object: `template_id`, `template_name`, `template_description`, `site_type`, `site_id` (the
reference site), `data` (the stored template text), `variable_map`. The status read returns `status` and
`status_description`; the values are not enumerated.

## create_template

```
POST /sdwan/v2.0/api/bulkconfigurations/sitetemplates
```
```json
{
  "template_name": "<name, max 128>",
  "template_description": "<optional, max 256>",
  "site_type": "<branch>",
  "site_id": "<reference-site-id>"
}
```
`template_name` and `site_type` are required. The specification describes the call as pulling the site's
configuration and storing the generated template. The `site_type` literal for a branch is not shown in
the schema description (assumption: the same value the site's `element_cluster_role` uses; read an
existing site to copy it). Success (200): the template object with `template_id`. A clone call also
exists: `POST /sdwan/v2.0/api/bulkconfigurations/sitetemplates/{site_template_id}/clone`, body
`template_name` and `template_description`; not used by the procedure.

## query_sites / read_site / read_site_status

```
POST /sdwan/v4.13/api/sites/query
GET  /sdwan/v4.13/api/sites/{site_id}
GET  /sdwan/v2.0/api/sites/{site_id}/status
```
The site carries `name` (max 128), `admin_state`, `element_cluster_role`, `address`, `tags`, and policy
stack references. The status read returns `site_id`, `inactive`, `inactive_reason`, `disabled`,
`disabled_reason`, and `region`. The list-all variant is `GET /sdwan/v4.13/api/sites`. Meaning of the
`inactive` flag for a site that has no device yet is not documented.

## deploy_template

```
POST /sdwan/v2.0/api/bulkconfigurations/sitetemplates/{site_template_id}/deployments
```
```json
{
  "variable_map": [
    {"site_name": "<name>", "ion_sw_version": "<version>", "ion_serial_number_1": "<serial or empty>"}
  ]
}
```
`variable_map` is an array of objects; the schema does not say what keys an element carries. The shape
above is assumed from the guide's mandatory variables (one object per site, keys are variable names;
unverified). Mandatory variable names per the guide: `site_name`, `ion_sw_version`,
`ion_serial_number_1`, plus `ion_serial_number_2` for an HA pair. Success (200): a list result whose
`items` hold `{site_id, template_id, deployment_id, variable_map}`, one per site. Named 400 errors:
`INVALID_INPUT_PARAM`, `INVALID_JSON_EXTRA_ATTRIBUTE`, `TEMPLATE_NOT_AVAILABLE`,
`INVALID_VARIABLE_MAP_DATA_TYPE`, `INVALID_VARIABLE_CHARACTER`.

## read_deployment / read_deployment_status

```
GET /sdwan/v2.0/api/bulkconfigurations/sitetemplates/{site_template_id}/deployments/{deployment_id}
GET /sdwan/v2.0/api/bulkconfigurations/sitetemplates/{site_template_id}/deployments/{deployment_id}/status
```
The first returns `site_id`, `template_id`, `deployment_id`, `variable_map`. The second returns `status`
and `status_description`; the set of status values and which are final is not documented. Read the text as
returned and ask the operator for a polling limit.

## delete_deployment

```
DELETE /sdwan/v2.0/api/bulkconfigurations/sitetemplates/{site_template_id}/deployments/{deployment_id}
```
Success (200): the deleted deployment record. What it removes beyond the record is not documented.

## query_machines / read_machine

```
POST /sdwan/v2.5/api/machines/query
GET  /sdwan/v2.5/api/machines/{machine_id}
```
A machine (device in inventory) carries `sl_no` (serial number), `model_name`, `hw_id`, `image_version`,
`connected`, `machine_state`, `inventory_op`, and `em_element_id`. `machine_state` values include
`MACHINE_ALLOCATED`, `MACHINE_CLAIM_PENDING`, `MACHINE_CLAIMED`, `MACHINE_CLAIM_FAILED`,
`MACHINE_ASSIGNED`, `MACHINE_ALLOCATED_TO_SHELL`, `MACHINE_ALLOCATION_TO_SHELL_IN_PROGRESS`, and
`MACHINE_INIT_FAILED`. Filtering by serial number in the query is assumed to use `sl_no` (unverified).
The machine identifier may differ from the serial; use the query to resolve it. A device stuck mid-claim can show `MACHINE_CLAIM_PENDING` or `MACHINE_CLAIM_FAILED`.
The guide's recover action for it has no verified binding here.

## query_elements / read_element

```
GET /sdwan/v3.2/api/elements
GET /sdwan/v3.2/api/elements/{element_id}
```
An element carries `site_id`, `name`, `serial_number`, `model_name`, `software_version`, `role`, `connected`,
`state` (for example `ACTIVE_BOUND_TO_SITE`, `ACTIVE_BOUND_TO_SITE_FAILED`, `ACTIVE_UNBOUND_IN_PROGRESS`,
`ACTIVE_DECLAIM_IN_PROGRESS`, `ACTIVE_DECLAIMED`), and `device_mode`. A 404 means no such element.

## list_element_shells

```
GET /sdwan/v2.1/api/sites/{site_id}/elementshells
GET /sdwan/v2.1/api/sites/{site_id}/elementshells/{element_shell_id}
```
A shell carries `model_name`, `software_version`, `site_id`, `element_id`, `name`, and `state`. Shell
create (`POST` on the same list route, requiring `model_name`, `software_version`, `site_id`) exists but
the procedure relies on the template deployment to create shells. Shell delete is bound below.

## delete_element_shell

```
DELETE /sdwan/v2.1/api/sites/{site_id}/elementshells/{element_shell_id}
```
Success (200): the deleted shell object; 404 means not found. The specification's only named 400 error
is `SHADIGEST_ELEMENT_SHELL_NOT_FOUND`. Whether deleting a shell is refused while it is mid-assignment is
not documented.

## assign_device_to_shell

```
POST /sdwan/v2.0/api/machines/{machine_id}/allocate_to_shell
```
Body: `{"element_shell_id": "<shell-id>"}`. The specification calls this "Allocate Element Shell to
Machine"; that it is the call behind the guide's assign-to-shell action is an inference (unverified), as
is the minimal body. Named 400 error: `ELEMENT_SHELL_NOT_FOUND`. An alternate shell update route exists
for associations: `PUT /sdwan/v2.0/api/sites/{site_id}/elementshells/{element_shell_id}`; its body
semantics are not documented and it is not used.

## unassign_device / declaim_device

```
POST /sdwan/v2.0/api/elements/{element_id}/operations
```
Body: `{"action": "<operation>", "parameters": []}`. The specification gives no list of valid `action`
values. The element's own `deployment_op` field lists `DECLAIM` and `REUNBIND` as deployment operations,
which suggests the action names for unassigning or returning a device to inventory, but they are not
confirmed for this route (unverified binding). Named 400 errors: `ELEMENT_NOT_FOUND`,
`COMMAND_NOT_SUPPORTED`. If no action can be confirmed, report that these two operations have no usable
binding instead of trying values.

Unverified candidate for put-back-in-inventory: the specification also lists
`POST /sdwan/v2.5/api/machines/{machine_id}/operations`, taking a machine object whose `inventory_op`
may be `claim`, `return`, `revoke`, `reuse`, `retire`, `recover`, and others. The specification does not
say which value matches the guide's put-back action; `return` may instead mean returning hardware to the
vendor, which is out of scope. Do not try values; confirm with the operator or vendor first. `recover`
is a possible match for the guide's stuck-claim recovery, equally unverified.

## delete_site

```
DELETE /sdwan/v4.13/api/sites/{site_id}
```
Success (200): the deleted site object. Named 400 errors: `SITE_NOT_FOUND`, `UNKNOWN_SITE`,
`DELETE_FORBIDDEN_INVALID_STATE`, `DELETE_FORBIDDEN_SITE_WAN_EXISTS`,
`DELETE_FORBIDDEN_SITE_WAN_LQM_CONFIG_EXISTS`, `DELETE_FORBIDDEN_ELEMENT_OR_ELEMENT_SHELL_EXISTS`,
`SITE_CONFIG_DELETE_NOTALLOWED_SERVICEENDPOINT_EXISTS`.

## Error handling

Error bodies hold an `_error` array of `{code, message}`. Report FAILED with the status and the codes
as returned. Where a code above is named in `procedure.md`, refer to it by that name. A 403 immediately
after sign-in may be the missing profile read described under authenticate.
