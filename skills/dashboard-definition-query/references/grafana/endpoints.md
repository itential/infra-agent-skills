# Grafana dashboard definition inspection: bindings

Bindings target Grafana's publisher MCP server at the cited commit.

| Operation | Tool arguments | Result |
|---|---|---|
| Search | `search_dashboards(query?, folderUid?, tag?, starred?, limit?, page?)` | `dashboards`, page `total`, `hasMore`; default limit 50, maximum 100 |
| Summary | `get_dashboard_summary(uid)` | Compact definition summary |
| Full definition | `get_dashboard_by_uid(uid, version?)` | Native classic/v2 definition |
| Property | `get_dashboard_property(uid, jsonPath)` | Selected native value |
| Query definitions | `get_dashboard_panel_queries(uid, panelId?, variables?)` | Panel queries and datasource references |

Examples of native paths: classic `$.panels`, `$.templating.list`; v2 `$.elements`, `$.variables`. Exact property errors are generated with prefixes `create JSONPath evaluable` and `apply JSONPath`; both require correcting the selection rather than treating the dashboard as empty. Search requires `dashboards:read` and `folders:read` with appropriate scopes.

## Sources

- [Publisher dashboard implementation](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/tools/dashboard.go). Retrieved 2026-10-09.
- [Publisher search implementation](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/tools/search.go). Retrieved 2026-10-09.
- [Publisher setup and permission reference](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/README.md). Retrieved 2026-10-09.
