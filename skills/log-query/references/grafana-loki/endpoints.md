# Grafana Loki: Query Wiring

Sources: Grafana Loki 3.6 documentation, Grafana Loki HTTP API, Manage tenant isolation, and Grafana Loki configuration parameters (`limits_config` defaults) (retrieved 2026-11-02).

Server address and credentials come from the existing client; Loki's API has no authentication of its own, so any login is handled in front of it. With `auth_enabled: true` (the default) every call carries `X-Scope-OrgID: <tenant>`. With `auth_enabled: false` the header is not needed and the single tenant is named `fake`.

| Operation | Method and path | Notes |
|---|---|---|
| Read build information | `GET /loki/api/v1/status/buildinfo` | Fields: `version`, `revision`, `branch`, `buildDate`, `buildUser`, `goVersion`. |
| List label values | `GET /loki/api/v1/label/{name}/values` | `start` and `end` (default 6 h ago and now), `since` (a duration before `end`; an explicit `start` wins), `query` (a stream selector that narrows the streams considered). Response `data`: an array of strings. Not documented: a successful empty listing can come back without `data`; read that as no values. |
| Run range query | `GET /loki/api/v1/query_range` | `query`; `start` (default one hour ago; included); `end` (default now; excluded); `since`; `limit` (default 100, stream results only); `direction` (`forward` or `backward`, default `backward`). |

Timestamps: an integer is a Unix time in nanoseconds, a float is Unix seconds with a fraction, and RFC 3339 or RFC 3339 nano strings are accepted.

Response fields: `status` (`success`), `data.resultType` (`streams` for a log query, `matrix` for a metric query), `data.result[].stream` (the label set), `data.result[].values` (pairs of a nanosecond timestamp string and the line; newest first for `backward`, oldest first for `forward`), `data.stats`.

Limits, as Loki 3.6 defaults that a deployment may change: `max_entries_limit_per_query` 5000; `query_timeout` 1m; `max_query_length` 30d1h; `max_query_lookback` 0s, meaning no cap (a window reaching past a set cap is shortened, not refused). `retention_period` deletes older entries.

Errors: HTTP 400 for a log query sent to the instant query, `GET /loki/api/v1/query`.

Unverified: the status code and body for an invalid query, for a `limit` above `max_entries_limit_per_query`, and for a window longer than `max_query_length`; whether `Retry-After` accompanies a 429 response.
