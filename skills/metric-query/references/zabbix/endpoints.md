# Zabbix metric bindings

Sources: [API](https://www.zabbix.com/documentation/current/en/manual/api),
[item.get](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/get),
[item object](https://www.zabbix.com/documentation/current/en/manual/api/reference/item/object),
[history.get](https://www.zabbix.com/documentation/current/en/manual/api/reference/history/get),
[trend.get](https://www.zabbix.com/documentation/current/en/manual/api/reference/trend/get), retrieved 2026-10-09.

Transport: `POST {frontend}/api_jsonrpc.php`, JSON-RPC 2.0, `Content-Type: application/json-rpc`,
with an existing `Authorization: Bearer <API_TOKEN>`. The frontend deployment path is an input.
Each envelope supplies `jsonrpc: "2.0"`, `method`, `params`, and a unique `id`.

| Operation | Method | Parameters | Result |
|---|---|---|---|
| Discover items | `item.get` | `hostids`, optional `search: {"key_":"<KEY_FRAGMENT>"}`, `output: ["itemid","name","key_","value_type","units","history","trends","lastclock"]` | Item array |
| Retrieve history | `history.get` | `itemids`, `history`, `time_from`, `time_till`, `output: "extend"`, optional `sortfield: ["clock","ns"]`, `sortorder: "ASC"`, `limit` | Sample array with `itemid`, `clock`, `ns`, `value` |
| Retrieve trends | `trend.get` | `itemids`, `time_from`, `time_till`, optional `limit`; `output: ["itemid","clock","num","value_min","value_avg","value_max"]` | Aggregate rows |

History selector: `0` float, `1` character, `2` log, `3` unsigned numeric (default), `4` text,
`5` binary. The current history page mentions JSON type `6` in a search caveat but omits it from
its selector table; that inconsistency is unresolved, so JSON history is outside this binding.
`time_from` and `time_till` include their boundaries and use epoch timestamps.

JSON-RPC errors expose `error.code`, `error.message`, and `error.data`; the API's invalid-parameter
example uses code `-32602`. Such a response is not an empty `result`. `id` correlates the exchange.
