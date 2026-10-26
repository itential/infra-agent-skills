# Log Query: Platform Index

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| Splunk | [splunk/](splunk/procedure.md) | Submit a search job, poll its state, read results in pages | Asynchronous job model; the management REST API must be enabled (Splunk Cloud requires a support request, free trials lack it). Export streaming is not covered. |
| Elasticsearch | [elasticsearch/](elasticsearch/procedure.md) | Read an index mapping, run a bounded search, qualify the hit total | Default result sample is small and totals are exact only up to a threshold. Deep paging is not covered. |
| AWS CloudWatch Logs | [aws-cloudwatch-logs/](aws-cloudwatch-logs/procedure.md) | Start a Logs Insights query, poll status, page results | Two-step start and retrieve; SDK-style calls rather than REST paths. |
| Google Cloud Logging | [google-cloud-logging/](google-cloud-logging/procedure.md) | List entries across resources by filter with page tokens | An empty page can still carry a token. |
