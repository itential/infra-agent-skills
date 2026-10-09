# Zabbix problem/event bindings

Sources: [API](https://www.zabbix.com/documentation/current/en/manual/api),
[problem.get](https://www.zabbix.com/documentation/current/en/manual/api/reference/problem/get),
[event.get](https://www.zabbix.com/documentation/current/en/manual/api/reference/event/get), retrieved 2026-10-09.

`POST {frontend}/api_jsonrpc.php`, existing bearer token, `Content-Type: application/json-rpc`.
Envelope fields: `jsonrpc: "2.0"`, `method`, `params`, `id`.

| Operation | Method | Parameters |
|---|---|---|
| Current problems | `problem.get` | `hostids` or `groupids`/`objectids`, `source: 0`, `object: 0`, `recent: false`, `output: "extend"`, `selectAcknowledges: "extend"`, `selectTags: "extend"`; optional `severities`, `limit`, `sortfield: ["eventid"]`, `sortorder: "DESC"` |
| Historical events | `event.get` | Same identity scope, `source: 0`, `object: 0`, `output: "extend"`, `time_from`, `time_till`, `selectHosts: ["hostid","host","name"]`, optional `selectRelatedObject: "extend"`, `selectAcknowledges: "extend"`, `limit`, `sortfield: ["clock","eventid"]`, `sortorder: "ASC"` |

For overlap queries, `problem_time_from` and `problem_time_till` are a required pair and apply only
to trigger events. They answer a different question from `time_from`/`time_till` (event creation).
`recent: true` includes unresolved plus recently resolved problems under configured `ok_period`.
A JSON-RPC `error` with `code`, `message`, and `data` is not an empty successful `result`.
