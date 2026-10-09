# Grafana Prometheus query: bindings

Publisher MCP bindings:

| Operation | Tool and parameters |
|---|---|
| Metric names | `list_prometheus_metric_names(datasourceUid, regex?, limit?, page?, startRfc3339?, endRfc3339?)` |
| Metadata | `list_prometheus_metric_metadata(datasourceUid, metric, limit?, limitPerMetric?)` |
| Query | `query_prometheus(datasourceUid, expr, endTime, queryType, startTime?, stepSeconds?)` |

Query type is `instant` or `range`; time inputs accept RFC3339 or the publisher's relative-time syntax. Range requires `startTime` and `stepSeconds`. Response includes `data`, optional `warnings`, optional `hints`. Range-step error: `stepSeconds must be provided when queryType is 'range'`. Names pagination requires positive `limit`/`page`; the installed implementation enforces a maximum product and returns an error when exceeded.

## Sources

- [Publisher Prometheus tools](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/tools/prometheus.go). Retrieved 2026-10-09.
- [Publisher permissions](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/README.md). Retrieved 2026-10-09.
