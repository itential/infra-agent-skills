# Prometheus HTTP bindings

Source: [Prometheus HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/) and
[management API](https://prometheus.io/docs/prometheus/latest/management_api/), retrieved 2026-10-09.
The deployment's configured origin is an input; this reference assumes its authenticated API client.

| Operation | Method and path | Input | Result |
|---|---|---|---|
| Check readiness | `GET /-/ready` | None | HTTP 200 when ready |
| Metric names | `GET /api/v1/label/__name__/values` | Optional `start`, `end`, repeated `match[]` | `data` string array |
| Metric metadata | `GET /api/v1/metadata` | Optional `metric`, `limit`, `limit_per_metric` | Metric-name keys with metadata arrays |
| Scrape targets | `GET /api/v1/targets` | Optional `state=active`, `dropped`, or `any` | `activeTargets`, `droppedTargets` |
| Instant evaluation | `GET /api/v1/query` | Required `query`; optional `time`, `timeout`, `limit` | `data.resultType`, `data.result` |
| Range evaluation | `GET /api/v1/query_range` | Required `query`, `start`, `end`, `step`; optional `timeout`, `limit` | Matrix in `data.result` |

Time inputs accept RFC3339 or epoch seconds; outputs use epoch seconds. Query parameters are URL
encoded. Both evaluation operations also support form-encoded POST to the same paths for large
expressions. `limit=0` means no series limit.

The envelope uses `status: success` or `status: error`. On failure, `errorType` and `error` explain
the result; `data` can still be present. `warnings` and `infos` may coexist with successful data.
HTTP 400, 422, and 503 represent invalid parameters, failed expression execution, and timeout/abort
respectively. Scrape entries include `health`, `lastScrape`, `lastError`, and post-relabel `labels`.
