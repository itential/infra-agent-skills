# Datadog Logs: Search Wiring

Sources: Datadog API reference, Logs, Search logs (v2), retrieved 2026-10-26.

`POST https://{datadog_api_host}/api/v2/logs/events/search`. The host depends on the account's site (for example the US, EU, AP1, AP2, UK1, US3, US5, and government sites each have their own `api.` host). Keys and token come from the existing client. The principal needs the `logs_read_data` permission; an OAuth app needs the matching scope.

Request body:

| Field | Meaning |
|---|---|
| `filter.query` | Log search query |
| `filter.from`, `filter.to` | Time bounds; ISO timestamp or date math such as `now-15m` |
| `filter.indexes` | Index list; default is all |
| `filter.storage_tier` | `indexes`, `online-archives`, or `flex` |
| `sort` | `timestamp` or `-timestamp` |
| `page.limit`, `page.cursor` | Page size and the previous `meta.page.after` value |
| `options` | Deprecated timezone and time-offset settings; omit |

Response: `data` (events), `meta.status` (`done` or `timeout`), `meta.elapsed`, `meta.request_id`, `meta.page.after`, `meta.warnings`. Errors: 400, 403, 429.
