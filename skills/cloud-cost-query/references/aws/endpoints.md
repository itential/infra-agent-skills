# AWS Cost Explorer bindings

Sources: [GetCostAndUsage](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [GetCostForecast](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostForecast.html), [GetAnomalies](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetAnomalies.html), retrieved 2026-10-09.

The authorized AWS SDK Cost Explorer client handles signing and its service endpoint.

| Operation | SDK operation | Required and selected inputs |
|---|---|---|
| Historical query | `GetCostAndUsage` / Boto3 `get_cost_and_usage` | `TimePeriod: {Start, End}`, `Granularity`, `Metrics`; optional `Filter`, `GroupBy` (up to 2), `BillingViewArn`, `NextPageToken` |
| Forecast | `GetCostForecast` / `get_cost_forecast` | `TimePeriod`, `Granularity: DAILY` or `MONTHLY`, `Metric`; optional `Filter`, `PredictionIntervalLevel` (51–99), `BillingViewArn` |
| Anomalies | `GetAnomalies` / `get_anomalies` | `DateInterval`; optional `MonitorArn`, `Feedback`, `TotalImpact`, `MaxResults`, `NextPageToken` |

Historical metrics include `AmortizedCost`, `BlendedCost`, `NetAmortizedCost`, `NetUnblendedCost`, `NormalizedUsageAmount`, `UnblendedCost`, `UsageQuantity`. Forecast cost-metric enums use uppercase, e.g. `UNBLENDED_COST`; they are not interchangeable literal strings.

Historical output: `ResultsByTime`, `GroupDefinitions`, `NextPageToken`; forecast: `ForecastResultsByTime`, `Total`; anomalies: `Anomalies`, `NextPageToken`.

Documented errors: cost/usage `BillExpirationException`, `BillingViewHealthStatusException`, `DataUnavailableException`, `InvalidNextTokenException`, `LimitExceededException`, `RequestChangedException`, `ResourceNotFoundException`; forecast health/data/rate/resource errors; anomaly invalid-token/rate errors. These operation errors use HTTP 400, so status alone is not a useful classification.
