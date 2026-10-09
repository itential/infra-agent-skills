# Datadog span-search binding

Base URL: the configured Datadog site's API endpoint, for example `https://api.datadoghq.com`. Auth: `DD-API-KEY` and `DD-APPLICATION-KEY`; OAuth uses `apm_read`.

`POST /api/v2/spans/events/search` with JSON:

```json
{
  "data": {
    "type": "search_request",
    "attributes": {
      "filter": {"from": "<start-time>", "to": "<end-time>", "query": "<span-query>"},
      "sort": "timestamp",
      "page": {"limit": 10}
    }
  }
}
```

`filter.from`/`to` accept ISO8601, supported date math, or millisecond timestamps. Optional `options.timezone` and `options.timeOffset` (seconds) are mutually exclusive. Sort values: `timestamp` or `-timestamp`. Continuation takes `meta.page.after` into `data.attributes.page.cursor`.

Response 200: `data[]`, span/trace attributes including `span_id`,`trace_id`,`parent_id`, `start_timestamp`,`end_timestamp`, and optional `single_span`; metadata includes `status` (`done`/`timeout`), `warnings`, `page.after`, and `request_id`. Response 400/422: fix reported input pointer/parameter; 403: permission failure; 429: throttled. Error objects may contain `detail`,`source`,`status`,`title`. No HTTP 200-only completion test is valid.

Source: Datadog [Search spans](https://docs.datadoghq.com/api/latest/spans/search-spans/), APIv2, retrieved 2026-10-09.
