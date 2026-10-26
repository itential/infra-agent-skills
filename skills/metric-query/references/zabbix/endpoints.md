# Zabbix JSON-RPC bindings

Sources: Zabbix API overview, item.get, item object, history.get, trend.get reference pages (current manual, retrieved 2026-10-26).

Transport: JSON-RPC 2.0 over HTTP to the frontend's `api_jsonrpc.php`; content type `application/json-rpc` (also `application/json` or `application/jsonrequest`). Authentication: `Authorization: Bearer <token>` with an API token or a token from `user.login`. Each request carries `jsonrpc`, `method`, `params`, `id`. The frontend path is a deployment input.

| Operation | Method | Parameters | Result |
|---|---|---|---|
| Discover items | `item.get` | `hostids`; optional `search` on `key_`; `output` fields such as `itemid`, `name`, `key_`, `value_type`, `units`, `history`, `trends`, `lastclock` | item array |
| Retrieve history | `history.get` | `itemids`, `history`, `time_from`, `time_till`; optional `sortfield` (`itemid`, `clock`, `ns`), `sortorder`, `limit`, `output` | samples with `itemid`, `clock`, `ns`, `value` |
| Retrieve trends | `trend.get` | `itemids`, `time_from`, `time_till`; optional `limit`, `output` | rows with `itemid`, `clock`, `num`, `value_min`, `value_avg`, `value_max` |

History type values: 0 float, 1 character, 2 log, 3 unsigned (default), 4 text, 5 binary. `value_type` on items uses the same numbering. `time_from` and `time_till` are Unix timestamps, both inclusive.

Errors return an `error` object with `code`, `message`, and `data` in place of `result`.
