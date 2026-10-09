# metric-query: platform references

| Platform | Procedure | Scope | Notes |
|---|---|---|---|
| Prometheus | [prometheus/procedure.md](prometheus/procedure.md) | PromQL instant/range evaluation, metric discovery, scrape metadata | HTTP API v1; metric metadata is experimental |
| Zabbix | [zabbix/procedure.md](zabbix/procedure.md) | Item discovery, typed history, numeric hourly trends | Current API reference; retention macros need resolution |
| Google Cloud Monitoring | [google_cloud/procedure.md](google_cloud/procedure.md) | Project time-series retrieval with optional aggregation | Monitoring v3 |
| Datadog | [datadog/procedure.md](datadog/procedure.md) | Scoped time-series points | Metrics v1 query; vendor recommends v2 for new integrations |
| Auvik | [auvik/procedure.md](auvik/procedure.md) | Device/interface/service/component statistics and SNMP poller history/current OID reads | Explicit statistic/interval selection |
| Grafana Prometheus | [grafana/procedure.md](grafana/procedure.md) | Metric/label discovery and PromQL evaluation | Publisher MCP bindings |
| AWS CloudWatch | [aws_cloudwatch/procedure.md](aws_cloudwatch/procedure.md) | Scoped metric statistics and metric-math queries using known metric identities | Native dimensions, status and continuation |
| Docker | [docker/procedure.md](docker/procedure.md) | One-shot container resource statistics | Platform-specific memory/PID interpretation |
