# Prometheus HTTP bindings

Sources: Prometheus HTTP API reference and management API reference (rolling "latest" docs, retrieved 2026-10-26). The server origin is a deployment input.

| Operation | Method and path | Input | Result |
|---|---|---|---|
| Check readiness | `GET /-/ready` (HEAD also accepted) | none | 200 when ready to serve queries |
| Metric names | `GET /api/v1/label/__name__/values` | optional `start`, `end`, repeated `match[]` | string array in `data` |
| Metric metadata | `GET /api/v1/metadata` | optional `metric`, `limit`, `limit_per_metric` | map of metric name to metadata entries |
| Scrape targets | `GET /api/v1/targets` | optional `state` (`active`, `dropped`, `any`), `scrapePool` | `activeTargets`, `droppedTargets`; each active target carries `health`, `lastScrape`, `lastError`, `labels` |
| Instant evaluation | `GET` or `POST /api/v1/query` | `query`; optional `time`, `timeout`, `limit`, `lookback_delta`, `stats` | `data.resultType` (`vector`, `matrix`, `scalar`, `string`) and `data.result` |
| Range evaluation | `GET` or `POST /api/v1/query_range` | `query`, `start`, `end`, `step`; optional `timeout`, `limit`, `lookback_delta`, `stats` | matrix in `data.result` |

Timestamps are RFC 3339 or Unix seconds. `POST` bodies are form-encoded.

Envelope fields: `status` (`success` or `error`), `data`, `errorType`, `error`, `warnings`, `infos`. Errors: 400 bad parameter, 422 expression not executable, 503 timeout or abort.
