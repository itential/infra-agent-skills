# Metric Query — Platform Index

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| Prometheus | [prometheus/](prometheus/procedure.md) | Evaluate a PromQL expression at one instant or over a range; list metric names, metadata, and scrape targets; readiness check | HTTP API. The caller supplies the PromQL expression. |
| Zabbix | [zabbix/](zabbix/procedure.md) | Find items for a host, read raw history for one value type, read trend aggregates | JSON-RPC API. Retention settings can be macros that are unresolved in the response. |
| Datadog | [datadog/](datadog/procedure.md) | Query metric time series with the v2 timeseries query call (metrics data source only) | The v1 query endpoint is not covered. Unconfirmed: response time unit and credential headers. Appears separately under `alert-monitor-management`, which covers monitors and downtimes only. |
| Amazon CloudWatch | [aws-cloudwatch/](aws-cloudwatch/procedure.md) | Read metric statistics or metric-math results with the platform's metric-data retrieval call, with pagination | Per-series status values; resolution drops as data ages. |
| Google Cloud Monitoring | [google-cloud-monitoring/](google-cloud-monitoring/procedure.md) | List time series for one metric type with optional aggregation and paging | Monitoring API v3. Points come newest first; server-side ordering is not supported. |
