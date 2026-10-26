# Zabbix — State Collection Wiring

Sources (Zabbix manual, current reference, version 7.4; retrieved 2026-10-26): the pages listed in [procedure.md](procedure.md). Placeholders: `{frontend}`, `{api_token}`, `<HOST_NAME>`, `<HOST_ID>`.

## Transport

All calls are JSON-RPC 2.0 posts to the API script in the frontend, `{frontend}/api_jsonrpc.php`. Content type may be `application/json-rpc`, `application/json`, or `application/jsonrequest`. Authenticate with `Authorization: Bearer {api_token}` (an API token created in the frontend, or a token from the login method). The request body has `jsonrpc`, `method`, `params`, and an `id`; the response has `result` or `error` plus the same `id`. An error object has `code`, `message`, and `data` (detail text).

## Calls

| Operation | Method | Selected parameters |
|---|---|---|
| Retrieve hosts | `host.get` | `filter: {"host": ["<HOST_NAME>"]}`, `output: ["hostid","host","name","status"]`, `selectInterfaces: ["interfaceid","type","ip","dns","port","available","error","errors_from"]`, `selectHostGroups: ["name"]`, `selectParentTemplates: ["name"]` |
| Retrieve items | `item.get` | `hostids: ["<HOST_ID>"]`, `output: ["itemid","name","key_","status","value_type","units","history","trends","lastclock","error"]` |

Unverified: the `item.get` parameters and the `selectHostGroups` / `selectParentTemplates` names were not read from the pages cited; confirm them in the API reference for the deployed version before binding. Assumption: `host.get` accepts a name filter and `limit` / `limitSelects` as general API parameters; `limitSelects` is documented to cap subselect rows.

## Field values

| Field | Values |
|---|---|
| Interface `available` | 0 unknown, 1 available, 2 unavailable |
| Interface `error` | Error text, set only when unavailable |
| Interface `errors_from` | Time the interface became unavailable (Assumption: Unix time; the format is not stated in the page read) |
| Item `lastclock` | Last update time, shown only within the max history display period (default 24 hours) |

Unverified: the numeric item `status` values (enabled/disabled) were not read; confirm in the item object page.

Do not pass the full-field selector for interfaces (`"extend"`): the interface `details` object, with SNMP `community`, `authpassphrase`, and `privpassphrase`, is part of the documented interface object.
