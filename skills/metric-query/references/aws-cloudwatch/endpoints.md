# CloudWatch GetMetricData binding

Sources: AWS CloudWatch API reference pages for GetMetricData and MetricDataResult (retrieved 2026-10-26).

An AWS SDK CloudWatch client (SigV4 signing, account and region from its configuration) calls the `GetMetricData` operation.

Request: `StartTime`, `EndTime`, `MetricDataQueries` (required); `NextToken`, `ScanBy` (`TimestampDescending` default, or `TimestampAscending`), `MaxDatapoints` (default 100,800), `LabelOptions.Timezone`. Each query has `Id` and either `MetricStat` (`Metric` with `Namespace`, `MetricName`, `Dimensions`; `Period`; `Stat`; optional `Unit`) or `Expression`; optional `Label`, `Period`, `ReturnData`, `AccountId`.

Response (HTTP 200): `MetricDataResults[]` each with `Id`, `Label`, `StatusCode` (`Complete`, `PartialData`, `InternalError`, `Forbidden`), `Timestamps`, `Values`, `Messages`; top-level `Messages` and `NextToken`.

Error: `InvalidNextToken`, HTTP 400.
