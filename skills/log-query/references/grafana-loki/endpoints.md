# Grafana Loki: HTTP API Wiring

Sources: Grafana Loki documentation, HTTP API reference (latest), retrieved 2026-10-26.

Base address, credentials, and TLS come from the existing client. Not documented: authentication.

| Operation | Method and path | Notes |
|---|---|---|
| List labels | `GET {loki}/loki/api/v1/labels` | Query `start`, `end`, `since`, `query` (stream selector). Default start is six hours back. |
| List label values | `GET {loki}/loki/api/v1/label/{name}/values` | Same query parameters. |
| Run stream query | `GET {loki}/loki/api/v1/query_range` | Query `query` (required), `limit` (default 100), `start` (default one hour back), `end`, `since`, `direction` (`forward` or `backward`, default `backward`), `interval`, `step` (metric queries only). |

Optional header `X-Scope-OrgID: {tenant}`; separate several tenants with `|`.

Response: `status`, `data.resultType` (`streams` or `matrix`), `data.result[].stream`, `data.result[].values` as `[timestamp_ns_string, line]`, `data.stats`. Documented error codes: 400 for LogQL errors, 429 for rate limiting.
