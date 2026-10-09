# ISE authentication diagnostic MCP bindings

Sources: [server.py](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/server.py) and [catalogue](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/docs/MCP_TOOLS_CATALOG.md), main, retrieved 2026-10-09.

| Operation | MCP tool | Inputs |
|---|---|---|
| Locate sessions | `active_sessions_search` | Optional `username`, `calling_station_id`, `nas_ip_address`, `framed_ip_address`, `audit_session_id`, `server`; `minutes` explicit 1–1440 (default 60); `limit` 1–20 (default 10) |
| Applied session detail | `sessions_search_with_advanced_details` | Optional `username`, `calling_station_id`; `minutes` 1–1440 (default 60), `limit` 1–10 (default 1) |
| Matched policy | `sessions_search_with_policy_details` | Same inputs as applied detail |
| AAA failure | `ise_investigate_aaa_failure` | At least one `calling_station_id` or `username`; `minutes` 1–1440 explicit (implementation default 1440); `limit` 1–10 (default 1) |
| Step latency | `sessions_search_with_latency_details` | Optional `username`, `calling_station_id`, nonnegative `min_latency_ms`, `max_latency_ms`; `minutes` 1–1440, `limit` 1–10 |
| Deployment counters | `get_active_session_counts` | None |

Current-schema corrections: AAA's public MAC input is `calling_station_id`, not the catalogue's `mac_address`. The numeric schema allows `minutes=0` but the source description specifies a positive duration; zero is not used by this procedure. The policy view projects out posture, auth method/protocol, framed IP, PSN node, response time, timestamp and protocol fields from its nested session; use the detail view when those are needed.

Locate results: `search_filters.lookup` = `direct` or `authlist_scan`, `total_matching_active_sessions`, `sample_size`, `active_sessions_sample`, optional `sampling_note`. Detail/policy/latency results carry `total_sessions_found`, `actual_sessions_returned`, `sessions`; policy context includes `resolution_errors` or `policy_context_note`; latency context includes `execution_steps` with nullable `text`/`latency_ms` and optional `latency_context_note`.

AAA results: `search_filters.source_api`, `total_failures_found`, `actual_failures_returned`, `has_more`, `failures`; each failure can contain reason code/text, cause, resolution, execution steps and `failure_context_note`. Counter results: `active_count`, `posture_count`, `profiler_count`.

`ISE_BUSY` is the publisher's retryable MnT backpressure condition; backoff is required. Authentication, API and parsing errors remain distinct from valid empty results. The catalogue does not establish an exhaustive error catalogue for each upstream ISE version.
