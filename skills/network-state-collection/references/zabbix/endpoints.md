# Zabbix — State Collection Wiring

Sources (Zabbix manual, current reference, version 7.4; retrieved 2026-10-26): the pages listed in [procedure.md](procedure.md). Placeholders: `{frontend}`, `{api_token}`, `<HOST_NAME>`, `<HOST_ID>`.

## Transport

All calls are JSON-RPC 2.0 posts to the API script in the frontend, `{frontend}/api_jsonrpc.php`. Content type may be `application/json-rpc`, `application/json`, or `application/jsonrequest`. Authenticate with `Authorization: Bearer {api_token}` (an API token created in the frontend, or a token from the login method). The request body has `jsonrpc`, `method`, `params`, and an `id`; the response has `result` or `error` plus the same `id`. An error object has `code`, `message`, and `data` (detail text).

## Calls

| Operation | Method | Selected parameters |
|---|---|---|
| Retrieve hosts | `host.get` | `filter: {"host": ["<HOST_NAME>"]}`, `output: ["hostid","host","name","status"]`, `selectInterfaces: ["interfaceid","type","ip","dns","port","available","error","errors_from"]`, `selectHostGroups: ["name"]`, `selectParentTemplates: ["name"]` |
| Retrieve items | `item.get` | `hostids: ["<HOST_ID>"]`, `output: ["itemid","name","key_","status","value_type","units","history","trends","lastclock","lastvalue","error"]` |

The `item.get` parameter `hostids` and the `host.get` select parameters `selectHostGroups`, `selectParentTemplates` and `selectInterfaces` are documented in the 7.4 reference. Assumption: `host.get` accepts a name filter and `limit` / `limitSelects` as general API parameters; `limitSelects` is documented to cap subselect rows.

## Field values

| Field | Values |
|---|---|
| Interface `available` | 0 unknown, 1 available, 2 unavailable |
| Interface `error` | Error text, set only when unavailable |
| Interface `errors_from` | Time the interface became unavailable (Assumption: Unix time; the format is not documented) |
| Item `lastclock` | Last update time, shown only within the max history display period (default 24 hours) |

Item `status`: the reference describes 0 as enabled and 1 as disabled in general terms. Unverified: confirm the exact values for the deployed version.

Do not pass the full-field selector (`"extend"`) for interfaces, items, or hosts. The interface `details` object (SNMP `community`, `authpassphrase`, `privpassphrase`), the item fields `password`, `privatekey`, `username`, `snmpv3_authpassphrase` and `snmpv3_privpassphrase`, and the host field `tls_psk` are documented as part of those objects.
