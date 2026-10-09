# Grafana Loki log query

Discover Loki labels and query observed log entries through Grafana's publisher MCP.

## Common Sequences

- Query logs: **Resolve scope** → **Discover labels** → **Query logs**.

### Resolve scope

The requested Grafana datasource UID and observation window select the Loki backend. This procedure is for Loki log streams, not other backends that share a tool name or LogQL metric-result mode. Missing/unsupported datasource or permission failure is not an empty stream.

### Discover labels

Label-name and label-value discovery use the same datasource, optional stream selector and time bounds. Actual values ground the supplied query selector. A failed label read remains a coverage gap, and no label is fabricated from a dashboard title.

### Query logs

The supplied LogQL expression, time bounds, direction and limit select log entries. The publisher caps requested limits to its configured maximum and returns metadata describing returned lines and possible truncation. The original direction and time range remain in the result. Full output preserves per-entry labels; compact output groups entries by stream while retaining varying metadata per line. Query/parser/transport failures remain errors. Empty-result hints do not establish that no logs exist outside the selected scope.

## Patterns

Log timestamps and metric timestamps have different representations in the implementation; this procedure selects stream queries and preserves their timestamps. Compact mode changes representation, not the requested query scope.

## Known limitations

No log configuration writes, source deletion or complete-history promise. A result limit is a coverage boundary, and server-side caps are not universal Loki limits.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover labels | Read stream label keys/values | Log read |
| Query logs | Execute supplied LogQL stream query | Log read |

## Verification checklist

- Datasource, selector and time scope are explicit.
- Direction, effective limit and truncation metadata are retained.
- Errors and empty-result hints are not collapsed into a clean bill of health.

## Sources

- [Publisher Loki tool schemas and implementation](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/tools/loki.go). Retrieved 2026-10-09.
- [Publisher permissions](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/README.md). Retrieved 2026-10-09.
