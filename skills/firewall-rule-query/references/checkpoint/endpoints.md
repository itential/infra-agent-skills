# Check Point Management MCP rule bindings

Source: [publisher tool implementation](https://github.com/CheckPointSW/mcp-servers/blob/main/packages/management/src/index.ts), Management API v2.1/R82.10+, retrieved 2026-10-09. MCP parameter names below use underscores; the wrapper translates them to the management API's hyphenated fields.

| Operation | Tool | Inputs |
|---|---|---|
| Discover packages | `show_packages` | Optional `domain`, `filter`, `limit` (default 50), `offset` (default 0), `details_level` uid/standard/full, `show_installation_targets` (default true) |
| List access layers | `show_access_layers` | Optional `domain`, `filter`, `limit`, `offset`, `details_level` |
| Resolve access layer | `show_access_layer` | `name` or `uid`; optional `domain`, `details_level` |
| Read access rulebase | `show_access_rulebase` | `name` or `uid`; optional `package`, `domain`, `filter`, `limit` (default 50; zero triggers all-pages helper), `offset` (default 0), `details_level`, `show_raw` (default false) |
| Read selected rule | `show_access_rule` | Required `layer`; at least one `name`, `uid`, numeric `rule_number`; optional `package`, `domain`, `details_level`, `show_hits`, `hits_settings` |
| Read NAT rulebase | `show_nat_rulebase` | Required `package`; optional `domain`, `filter`, `limit`, `offset`, `details_level`, `show_hits`, `hits_settings`, `use_object_dictionary` |

Access rulebase also supports `format` = table/model-friendly, `expand_groups`, `group_mode` = in-rule/as-reference, `dereference_group_members`, `show_membership`, `use_object_dictionary`, `show_hits` and `hits_settings` (`from_date`, `to_date`, `target`). Filter settings include `search_mode` = general/packet and optional packet matching controls; their complete installed schema governs use rather than an inferred string expression.

In MDS deployments, `domain` identifies routing scope. The optional cross-domain scope field is excluded from this procedure. Paginated raw responses expose `from`, `to`, `total`; the publisher's formatted response emits a next-page hint using `offset: <to>`. A caller preserves scope when following that hint.

Exact formatted-read errors include `Error: Either name or uid parameter is required to identify the rulebase.` and `Error parsing rulebase: <message>`. These are returned as text and are not necessarily MCP `isError` results. Other API errors retain the upstream management response; no exhaustive error code catalogue is established here.
