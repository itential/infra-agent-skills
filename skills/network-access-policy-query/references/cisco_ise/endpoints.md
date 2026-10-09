# ISE policy query MCP bindings

Sources: [catalogue](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/docs/MCP_TOOLS_CATALOG.md), [implementation schemas](https://github.com/CiscoDevNet/cisco-ise-mcp-official/blob/main/server.py), main, retrieved 2026-10-09.

| Operation | Tool | Inputs |
|---|---|---|
| Policy sets | `ise_search_policy_sets` | `name_substring`; `state_filter` all/enabled/disabled/monitor (default all); `limit` 1–100 (default 20); nonnegative `min_hit_counts`, `max_hit_counts` |
| Authentication rules | `ise_search_authentication_rules` | Optional `policy_set_name`, `identity_source_filter`, `state_filter` all/enabled/disabled, `min_hit_counts`, `max_hit_counts`, `name_substring`; `limit` 1–50 (default 25) |
| Authorization rules | `ise_search_authorization_rules` | Optional `policy_set_name`, `profile_name_filter`, `security_group_filter`, `state_filter` all/enabled/disabled, `min_hit_counts`, `max_hit_counts`, `name_substring`; `limit` 1–50 (default 25) |

All name and state fields are strings; hit-count filters are nonnegative integers. Profile, security-group and identity-source filters are case-insensitive exact names; rule/policy-set name filters are case-insensitive substrings.

Results carry `search_filters`, `total_count`, `count`, `has_more`; rule queries also carry `policy_sets_scanned`, `policy_sets_total`, `rules`. Authorization adds `global_exceptions` outside the ordinary rule return cap. Rule fan-out is bounded at 25 policy sets in the cited catalogue, so coverage counts are essential. Policy-set records contain rank, state, hit counts, default flag, service name and condition summary. Missing hit counts are treated as zero by the publisher.

Failure of the global-exception request fails the authorization call. Other API failures remain failures or reduced scan coverage, as indicated by the returned result; an incomplete scan is not a complete empty result.
