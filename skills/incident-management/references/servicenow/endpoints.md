# Endpoints — ServiceNow incident table (Table API)

Literal wiring layer for `procedure.md`. Operation names in its Tools table map to the calls below.

Written against the ServiceNow Zurich Table API reference, checked 2026-10-14. Field names come from
the sample incident record in that reference; mappings from a form label to a field name that the
reference does not show explicitly are marked as assumptions. Values are placeholders.

## Table name

Every operation below except `read_choices` targets one table: **`incident`**. The Table API is generic, so the table is a
request parameter (`tableName` in the path) rather than part of the operation. ServiceNow's reference
uses `incident` as its own example table name. A client that exposes a generic table operation must be
given `tableName = incident` for those calls; an operation that takes no table name is not a binding for
them. `read_choices` targets a different table, named in its section. The `sys_id` used by read and update calls is the record's identifier in that
table, not the incident number (`INC...`), which is found through `find_incidents`.

## Base path and versions

All calls go to the instance host. Default path form: `/api/now/table/incident[/{sys_id}]`. A versioned
form `/api/now/{api_version}/table/incident[/{sys_id}]` exists; omit the version to use the latest.
Available versions are listed in the instance's REST API Explorer.

**No-match behavior depends on the version.** A search with no hits gets an empty 200 response from
version 2 but a 404 from version 1. Either one means "nothing found"; record which version the client
uses.

The calling user needs enough roles to reach the table; the roles that matter for incidents are named
in `procedure.md`. The reference's examples authenticate with a username and password over HTTPS;
other schemes depend on instance configuration and are not covered here.

## find_incidents

```
GET /api/now/table/incident
```
Useful query parameters (documented): `sysparm_query` (encoded query; operators `=`, `!=`, `LIKE`,
`STARTSWITH`, `ENDSWITH`; `^` joins conditions as AND and `^OR` as OR; column names and values are
case-sensitive), `sysparm_fields` (comma-separated fields to return), `sysparm_limit` and
`sysparm_offset` (paging), `sysparm_display_value` (`true`, `false`, or `all`),
`sysparm_exclude_reference_link`. Name-value pairs may be used instead of `sysparm_query` (for example
`active=true`), and a choice value can be given by its label such as `state=closed` in place of the
stored value.

Examples (shape only): `sysparm_query=active=true^cmdb_ci=<ci_sys_id>` for open incidents on a CI;
`number=<INC number>` for one incident.

## read_incident

```
GET /api/now/table/incident/{sys_id}
```
Same display and field parameters. Returns the record as name-value pairs under `result`.

## create_incident

```
POST /api/now/table/incident
Content-Type: application/json
```
Each call inserts a single record (batch insertion is not offered). The body is name-value pairs. Example
shape from ServiceNow's reference (placeholder values):

```json
{
  "short_description": "<summary>",
  "assignment_group": "<group sys_id>",
  "urgency": "2",
  "impact": "2"
}
```
Success: 201, a `Location` header, and the new record, which in ServiceNow's sample shows state `1`, the
generated `number`, and a calculated `priority`. Anything you omit that the platform does not generate is stored empty.
Other documented statuses: 400 (malformed request) and 404 (not found). The `X-no-response-body: true` request header
omits the body.

## update_incident

```
PATCH /api/now/table/incident/{sys_id}
Content-Type: application/json
```
Body is only the fields to change. Success: 200 and the updated record. Documented errors: 400 and 404.
`PUT` on the same path is also documented as a full update; this procedure uses `PATCH` so that omitted
fields are untouched (assumption: `PUT` can null fields that are omitted, by analogy with insert behavior).

Field names (from the reference's sample record unless marked):

| Form label | Field name | Notes |
|---|---|---|
| Number | `number` | Generated; read-only |
| Caller | `caller_id` | Reference to a user |
| Short description | `short_description` | |
| Description | `description` | |
| Category / Subcategory | `category` / `subcategory` | `subcategory` shown in the sample (assumption for exact label mapping) |
| Business service | `business_service` | |
| Configuration item | `cmdb_ci` | |
| Impact / Urgency | `impact` / `urgency` | Choice values; sample uses `"1"`, `"2"` |
| Priority | `priority` | Calculated; read-only on the form |
| Assignment group | `assignment_group` | Reference; sys_id of the group (a display name when display-value input is on) |
| Assigned to | `assigned_to` | Reference; sys_id of the user (a display name when display-value input is on) |
| State | `state` | Primary state field |
| Incident state | `incident_state` | Sibling field; the sample shows both with the same value |
| On hold reason | `hold_reason` | Present in the sample record, empty until used |
| Additional comments | `comments` | Journal; caller-visible |
| Work notes | `work_notes` | Journal; internal |
| Resolution code | `close_code` | Choice field with instance-defined values. Label mapping assumed from the sample (also used by close scripts) |
| Resolution notes | `close_notes` | Same assumption |
| Resolved by | `resolved_by` | |
| Resolved (date and time) | `resolved_at` | Present in the sample record; empty until resolved |
| Related change request | `rfc` | Assumption: the sample key for the change request link |
| Related problem | `problem_id` | Assumption: sample key for the problem link |
| Caused by change | `caused_by` | Assumption: sample key |
| Parent incident | `parent_incident` | |
| Reopen count | `reopen_count` | |
| Last reopened by / at | not shown in the sample | Documented as form fields; the field names were not found in the sources |

**Notes** are written through `update_incident` with a body holding only `comments` (additional comment) or
`work_notes` (internal note); ServiceNow's own PATCH example sets `comments` with other fields.

### Stored values

`procedure.md` (*State model* and *Choice values*) lists the stored values the sources give and the order
to try for others. In short: `1` (New) comes from the sample record; `6` (Resolved) and `7` (Closed) come
from reference scripts that set the incident state field beside the state field, so applying them to
`state` is an inference. The reference's `state=closed` versus `state=7` filter example is generic, not
an incident-specific mapping.

### Parameters for writes

`sysparm_input_display_value` (default false) treats input as display values and converts, for example,
a reference's display name to its sys_id; `sysparm_display_value`, `sysparm_fields`, and
`sysparm_exclude_reference_link` shape the response. `sys_`-prefixed fields are system-managed and
cannot be set.

## read_choices

```
GET /api/now/table/sys_choice
```
Reads a choice field's options. The documentation names `sys_choice` as the store of choice options;
filtering it by table name and field name (for example `name=incident^element=state`) and the column names
for the stored value and label are assumptions, not read in the sources. This is the only operation here
that does not target the `incident` table. Use only when *Choice values* step 2 applies.

## Documented error handling

The reference lists 400 (bad or malformed request) and 404 (item not found) for create and update, 201
for create and 200 for update, and 204 for delete. It does not give error strings for incident rule
failures. Report FAILED with the actual status and body.

## Not covered

- Deleting an incident is possible through the same table path but is not part of this procedure.
- Cancel, the problem and change tables, and the platform's separate change and problem endpoints.
