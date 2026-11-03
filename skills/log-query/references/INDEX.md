# Log Query: Platform Index

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| Splunk | [splunk/](splunk/procedure.md) | Submit a search job, poll its state, read results in pages | Asynchronous job model; the management REST API must be enabled (Splunk Cloud requires a support request, free trials lack it). Export streaming is not covered. |
| Elasticsearch | [elasticsearch/](elasticsearch/procedure.md) | Read an index mapping, run a bounded search, qualify the hit total | Default result sample is small and totals are exact only up to a threshold. Deep paging is not covered. |
| AWS CloudWatch Logs | [aws-cloudwatch-logs/](aws-cloudwatch-logs/procedure.md) | Start a Logs Insights query, poll status, page results | Two-step start and retrieve; SDK-style calls rather than REST paths. |
| Google Cloud Logging | [google-cloud-logging/](google-cloud-logging/procedure.md) | List entries across resources by filter with page tokens | An empty page can still carry a token. |
| Grafana Loki | [grafana-loki/](grafana-loki/procedure.md) | Confirm a stream's labels, run a bounded range query, read a larger window in slices | Log queries only; metric queries and live tail are not covered. No page token, and a full page is not the oldest or newest entries: a larger window is read as slices that each come back below the limit. A window reaching past a configured lookback cap is shortened without an error. Written against Loki 3.6. |

**Completion (Grafana Loki):** Loki returns no completion signal and no page token. A page holding fewer entries than the limit is the only sign that the window was read in full.
