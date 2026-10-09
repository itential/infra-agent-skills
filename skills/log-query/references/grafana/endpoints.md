# Grafana Loki log query: bindings

Publisher MCP bindings:

| Operation | Tool and parameters |
|---|---|
| Label names | `list_loki_label_names(datasourceUid, matcher?, startRfc3339?, endRfc3339?)` |
| Label values | `list_loki_label_values(datasourceUid, labelName, matcher?, startRfc3339?, endRfc3339?)` |
| Stream query | `query_loki_logs(datasourceUid, logql, startRfc3339?, endRfc3339?, limit?, direction?, queryType="range", format?)` |

`direction` is `forward` or `backward`; `format` is `full` or `compact`. Metadata includes `linesReturned`, `maxLinesAllowed`, `resultsTruncated`, nullable `totalLinesScanned`, `startTime`, `endTime`. A null scanned count is not zero. The default line count is 10; the maximum is configurable by the MCP server. Error details depend on backend and are retained unchanged.

## Sources

- [Publisher Loki tool schemas and implementation](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/tools/loki.go). Retrieved 2026-10-09.
- [Publisher permissions](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/README.md). Retrieved 2026-10-09.
