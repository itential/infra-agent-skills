# Datadog v2 timeseries query binding

Sources: Datadog API reference, Metrics section, "Query timeseries data across multiple products" (retrieved 2026-10-26).

| Operation | Method and path | Notes |
|---|---|---|
| Query timeseries | `POST /api/v2/query/timeseries` on the account's Datadog site API host | JSON body below |

Request: `data.type` is `timeseries_request`; `data.attributes` holds `from` and `to` (Unix epoch milliseconds, required), `queries` (required), `formulas` (required), and optional `interval` (milliseconds). Each query has `data_source` (use `metrics`), `query`, and `name`. Each formula has `formula` (an expression over query names such as `a+b`) and an optional `limit` object with `count` and `order` (`asc` or `desc`).

Response (200): `data.type` is `timeseries_response`; `data.attributes` holds `series` (with `group_tags`, `query_index`, `unit`), `times`, `values`.

Errors: 400, 401, 403, 429, each with an `errors` array of strings.

Permission: the `timeseries_query` scope for OAuth applications. Assumption: API key and application key headers authenticate other clients; the vendor reference does not state this.
