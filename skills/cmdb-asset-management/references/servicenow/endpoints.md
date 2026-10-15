# Endpoint Wiring — ServiceNow CMDB Configuration Item Management

Literal API calls behind each capability named in `procedure.md`. Base URL:
`https://<instance>.service-now.com`. Auth: Basic (username/password) or OAuth 2.0, per the target
instance's configuration.

## Create or Update a CI (CMDB Instance API)

Tool hint: `POST /api/now/cmdb/instance/{className}` — e.g.
`POST /api/now/cmdb/instance/cmdb_ci_linux_server`.

Body: a JSON object of the CI's attributes for that class (e.g. `name`, `host_name`, `ip_address`,
`discovery_source`, plus class-specific fields). The Identification and Reconciliation Engine (IRE)
evaluates this payload against the class's identification rules; if a match is found, the matched CI
is updated instead of a new one created.

Response: `201 Created` for a genuinely new CI, or a response reflecting the matched/updated existing
`sys_id` when IRE found a match — check which occurred, not just the HTTP status class.

Documented constraint: "You can only insert, update, or delete one record at a time" — no bulk
operations via this endpoint.

Documented missing-field error example: omitting `discovery_source` has been observed to produce a
validation error naming that field specifically, on at least some CI classes.

## Read a CI (Table API)

Tool hint: single record — `GET /api/now/table/{class-table-name}/{sys_id}`; filtered list —
`GET /api/now/table/{class-table-name}?sysparm_query={encoded-query}`.

Example class tables: `cmdb_ci` (base — common fields only), `cmdb_ci_server`,
`cmdb_ci_linux_server`, `cmdb_ci_computer`, etc.

Query parameters:
- `sysparm_query` — encoded query string filter (ServiceNow encoded-query syntax, e.g.
  `location=<sys_id>^operational_status=1`).
- `sysparm_fields` — comma-separated field list to limit the response payload.
- `sysparm_limit` — maximum records to return (server default: 10000).
- `sysparm_offset` — starting record index, for pagination.
- `sysparm_display_value` — `true` (display values only), `false` (raw/database values only, default),
  or `all` (both raw and display value for every field, useful for reference fields).
- `sysparm_exclude_reference_link` — boolean; when true, drop the `link` sub-object ServiceNow
  normally includes for reference fields in the response.
- `sysparm_view` — `desktop`, `mobile`, or `both`; affects which view's field set is returned.
- `sysparm_no_count` — boolean; when true, skips the `select count(*)` ServiceNow otherwise runs
  alongside a list query (a performance consideration for large tables, not a correctness one).

Example:
```
curl "https://instance.servicenow.com/api/now/table/incident/a9e30c7dc61122760116894de7bcc7bd" \
  --request GET \
  --header "Accept:application/json" \
  --user 'username':'password'
```
Response shape:
```json
{
  "result": {
    "sys_id": "a9e30c7dc61122760116894de7bcc7bd",
    "number": "INC0000046",
    "short_description": "Can't access SFA software",
    "urgency": "3"
  }
}
```
(Table API response shape shown against `incident` as the documented example table; the same
`{"result": {...}}` / `{"result": [...]}` shape applies against any table, including CI class tables.)

## Read CI Relationships (Table API against `cmdb_rel_ci`)

Tool hint: `GET /api/now/table/cmdb_rel_ci?sysparm_query=parent={sys_id}^ORchild={sys_id}`.

Fields of note on each `cmdb_rel_ci` record: `parent` (reference to the parent-side CI), `child`
(reference to the child-side CI), `type` (reference to a relationship-type record, e.g. "Depends
on::Used by").

## Update a CI Directly (Table API)

Tool hint: `PATCH /api/now/table/{class-table-name}/{sys_id}` (partial update) or
`PUT /api/now/table/{class-table-name}/{sys_id}` (full update — replaces the full record per
ServiceNow's PUT semantics, so omitted fields may be cleared rather than left unchanged; prefer PATCH
unless a full replace is genuinely intended).

## Delete a CI (Table API)

Tool hint: `DELETE /api/now/table/{class-table-name}/{sys_id}`.

## General Table API endpoint pattern reference

- GET (list): `/api/now/table/{tableName}` or versioned `/api/now/{api_version}/table/{tableName}`.
- GET (single): `/api/now/table/{tableName}/{sys_id}`.
- POST (create): `/api/now/table/{tableName}`.
- PATCH (partial update) / PUT (full update): `/api/now/table/{tableName}/{sys_id}`.
- DELETE: `/api/now/table/{tableName}/{sys_id}`.
