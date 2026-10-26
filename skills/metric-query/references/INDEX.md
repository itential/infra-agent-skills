# Metric Query — Platform Index

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| Prometheus | [prometheus/](prometheus/procedure.md) | Evaluate a PromQL expression at one instant or over a range; list metric names, metadata, and scrape targets; readiness check | HTTP API. The caller supplies the PromQL expression. |
| Zabbix | [zabbix/](zabbix/procedure.md) | Find items for a host, read raw history for one value type, read trend aggregates | JSON-RPC API. Retention settings can be macros that are unresolved in the response. Zabbix also appears under `network-state-collection`, which reads current host, interface, and item state; this directory covers history and trends only. |
| Amazon CloudWatch | [aws-cloudwatch/](aws-cloudwatch/procedure.md) | Read metric statistics or metric-math results with the platform's metric-data retrieval call, with pagination | Per-series status values; resolution drops as data ages. |
