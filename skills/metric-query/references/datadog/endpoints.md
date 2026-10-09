# Datadog metric query binding

Source: [query time-series points](https://docs.datadoghq.com/api/latest/metrics/query-timeseries-points/),
retrieved 2026-10-09. Existing authenticated client and site selection are prerequisites.

`GET {datadog_api_origin}/api/v1/query` takes required `from`, `to` (epoch seconds) and `query`.
The operation requires `timeseries_query` permission; OAuth integrations use that scope.
A successful HTTP 200 response includes `status`, `series`, `query`, `from_date`, and `to_date`.
Series may include `pointlist`, `interval`, `tag_set`, and `unit`. Returned timestamps and
intervals are milliseconds. A non-`ok` status can provide `error`; non-success HTTP responses
400, 403, and 429 have an `errors` array.

The vendor currently recommends `/api/v2/query/timeseries`; its different request schema is not
implied by the v1 binding.
