# CloudWatch metric binding

Sources: [GetMetricData](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricData.html), [MetricDataQuery](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDataQuery.html), [MetricDataResult](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDataResult.html), retrieved 2026-10-09.

An authenticated AWS SDK CloudWatch client supplies account/region and SigV4 signing. SDK operation: `GetMetricData` (Boto3 `get_metric_data`). Required: `StartTime`, `EndTime`, `MetricDataQueries`. A query has `Id` and exactly one of `MetricStat` or `Expression`. `MetricStat` identifies `Metric` (`Namespace`, `MetricName`, `Dimensions`) plus `Period`, `Stat`, optional `Unit`. `ReturnData` selects raw results. Maximum 500 query structures per request.

Continuation: `NextToken`; order: `ScanBy` (`TimestampAscending`/`TimestampDescending`). Results: `MetricDataResults[]` with `Id`, `Timestamps`, `Values`, `StatusCode`, `Messages`; overall `Messages`, `NextToken`. `InvalidNextToken` is HTTP 400. A returned HTTP success does not override `PartialData`, `InternalError`, or `Forbidden` in a result.
