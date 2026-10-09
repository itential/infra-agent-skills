# Datadog Logs API v2 binding

Sources: [search logs](https://docs.datadoghq.com/api/latest/logs/search-logs-post/),
[paging guide](https://docs.datadoghq.com/logs/guide/access-your-log-data-programmatically/),
retrieved 2026-10-09. An existing authenticated client uses the account's site origin and
`logs_read_data` permission (or OAuth scope).

`POST {datadog_api_origin}/api/v2/logs/events/search` accepts:

```json
{
  "filter": {
    "from": "2026-01-01T00:00:00Z",
    "to": "2026-01-02T00:00:00Z",
    "indexes": ["<INDEX_NAME>"],
    "query": "service:<SERVICE_NAME>",
    "storage_tier": "indexes"
  },
  "page": {"limit": 100},
  "sort": "timestamp"
}
```

Success: `data` event array, `meta.status` (`done`/`timeout`), optional `meta.warnings`, and
`meta.page.after`. A continuation request sets `page.cursor` to `meta.page.after` and retains the
other fields. `sort` is `timestamp` or `-timestamp`. Supported storage tiers are `indexes`,
`online-archives`, and `flex`; availability depends on the account.
`options.timezone` and `options.timeOffset` are deprecated/no-op fields.
HTTP 400, 403, and 429 return `errors` arrays.
