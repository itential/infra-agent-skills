# Grafana Prometheus query

Query a selected Prometheus datasource through Grafana's publisher MCP.

## Common Sequences

- Discover/query: **Resolve datasource** → **Discover metric** → **Query**.

### Resolve datasource

The configured Grafana instance and explicitly identified datasource UID determine the backend. Missing datasource, unsupported backend or insufficient query/read permissions leaves the operation unresolved. This procedure covers Prometheus data sources; similarly named tools can route to other backends, which require their own documented scope.

### Discover metric

Metric-name discovery accepts a regex, time window and positive page/limit. Invalid regex, non-positive pagination, or the publisher's page-size product bound is a request error. Metric metadata supplies the selected metric's documented type/help/unit where available; absence is not an inferred unit.

### Query

An instant query uses the supplied evaluation time. A range query requires starting time, ending time and step in seconds. Invalid time parsing or a missing range step is a failed query. The result preserves native data, warnings and any empty-result hints. Backend warnings, including partial responses, remain visible. An empty result supplies no proof of zero activity; discovery/time/label scope can explain it.

## Patterns

The tool defaults to range mode when the query type is omitted; explicitly selecting the type avoids accidental range-parameter omissions.

## Known limitations

No arbitrary hard-coded thresholds, inferred units or alert updates. Empty-result hints are guidance, not a verified diagnosis.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover metric | Read metric names/metadata | Monitoring read |
| Query | Evaluate supplied PromQL | Monitoring read |

## Verification checklist

- Datasource UID and query type are explicit.
- Range time bounds/step or instant evaluation time are supplied.
- Native warnings and gaps are preserved.

## Sources

- [Publisher Prometheus tools](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/tools/prometheus.go). Retrieved 2026-10-09.
- [Publisher permissions](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/README.md). Retrieved 2026-10-09.
