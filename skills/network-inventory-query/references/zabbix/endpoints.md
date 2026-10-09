# Zabbix inventory bindings

Sources: [API](https://www.zabbix.com/documentation/current/en/manual/api),
[host.get](https://www.zabbix.com/documentation/current/en/manual/api/reference/host/get),
[interface fields](https://www.zabbix.com/documentation/current/en/manual/api/reference/hostinterface/object),
[item.get](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/get),
[item fields](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/object), retrieved 2026-10-09.

`POST {frontend}/api_jsonrpc.php`, `Content-Type: application/json-rpc`, existing bearer token.
Envelope: `jsonrpc: "2.0"`, `method`, `params`, and correlation `id`.

| Operation | Method | Selected parameters |
|---|---|---|
| Retrieve hosts | `host.get` | `filter: {"host":["<HOST_NAME>"]}`, `output: ["hostid","host","name","status"]`, `selectInterfaces: ["interfaceid","type","ip","dns","port","available","error","errors_from"]`, `selectHostGroups: ["name"]`, `selectParentTemplates: ["name"]` |
| Retrieve items | `item.get` | `hostids: ["<HOST_ID>"]`, `output: ["itemid","name","key_","status","value_type","units","history","trends","lastclock","error"]` |

`available`: 0 unknown, 1 available, 2 unavailable. `errors_from` is the interface-unavailability
start, not a timestamp proving when the entire device failed. Item `status`: 0 enabled, 1 disabled.
`lastclock` normally displays only values within the last 24 hours; the deployment can change that
window. `limit` bounds primary results; `limitSelects` bounds supported subselects.
`selectInterfaces: "extend"` is deliberately avoided because interface details can include SNMP
credentials. Errors use `error.code`, `error.message`, and `error.data`, not an empty `result`.
