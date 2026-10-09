# Z-Insights aggregate bindings

Sources: [web traffic](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zins/web_traffic.py), [common inputs](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zins/_common.py), master retrieved 2026-10-09.

All tools below use `start_time` and `end_time` in Unix epoch milliseconds, or `start_days_ago`/`end_days_ago` (defaults 9/2). Relative spans are normalized by the connector to seven or fourteen days; explicit timestamps take precedence. The documented valid interval is exactly seven or fourteen days, ending at least one day in the past.

| Measure | MCP tool | Additional inputs |
|---|---|---|
| Location traffic | `zins_get_web_traffic_by_location` | `traffic_unit`, `include_trend`, `trend_interval`, `limit`. |
| Total traffic | `zins_get_web_traffic_no_grouping` | Same, plus `action_filter` and `dlp_engine_filter`. |
| Protocol mix | `zins_get_web_protocols` | `traffic_unit`, `limit`. |
| Threat categories | `zins_get_threat_super_categories` | `traffic_unit`, `limit`. |
| Threat classes | `zins_get_threat_class` | `traffic_unit`, `limit`. |

`traffic_unit`: `TRANSACTIONS` or `BYTES`; `trend_interval`: `DAY` or `HOUR`; `action_filter`: `ALLOW` or `BLOCK`; `limit`: 1–1000, default 50. `include_trend` defaults false. Optional DLP engine values come from the current input schema; unsupported guessed values are not supplied.

Validation errors include `start_time must be less than end_time` and an end-time availability error. The connector inspects GraphQL `errors` as well as SDK failures. `BAD_REQUEST` and `INTERNAL_ERROR` are surfaced as tool errors; HTTP 200 alone is not success.
