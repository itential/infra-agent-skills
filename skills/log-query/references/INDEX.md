# log-query: platform references

| Platform | Procedure | Scope | Notes |
|---|---|---|---|
| Google Cloud Logging | [google_cloud/procedure.md](google_cloud/procedure.md) | Entries search and continuation pages | Logging v2 |
| Datadog | [datadog/procedure.md](datadog/procedure.md) | Log event search and cursor paging | Logs API v2 |
| Elasticsearch | [elastic/procedure.md](elastic/procedure.md) | Mapping inspection and scoped Query DSL search/count | Existing indices only |
| Splunk | [splunk/procedure.md](splunk/procedure.md) | Scoped search jobs, results and export | Native completion/pagination retained |
| Grafana Loki | [grafana/procedure.md](grafana/procedure.md) | Label discovery and scoped log queries | Publisher MCP bindings |
| AWS CloudWatch Logs | [aws_cloudwatch/procedure.md](aws_cloudwatch/procedure.md) | Log-group discovery and bounded Logs Insights QL jobs/results | Account/region/time scope retained |
| NetClaw syslog | [netclaw_syslog/procedure.md](netclaw_syslog/procedure.md) | Retained receiver messages and statistics | Unverified time/severity filters blocked |
| Fortinet FortiAnalyzer | [fortinet_fortianalyzer/procedure.md](fortinet_fortianalyzer/procedure.md) | Historical Log View filtering and details | Documented GUI procedure; no wrapper cursor assumptions |
