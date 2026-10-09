# CloudWatch metric query

Retrieve specified metric statistics or metric-math results for a bounded interval.

Sources: current AWS [metric query API](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricData.html), [query structure](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDataQuery.html), and [result structure](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDataResult.html), retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## 1. Specify the metric request

The request identifies the AWS account/region, metric namespace/name/dimensions, statistic, period and interval, or a supported expression over those inputs. Each query identifier is unique. The start is inclusive and end exclusive; the service rounds older start times to retained resolution. An explicitly wrong unit can produce no data because CloudWatch does not convert units.

## 2. Retrieve and paginate

A successful response contains result series and possibly a continuation token. The same request continues with that token until exhausted. Invalid continuation requires restarting the query rather than reporting a complete result. Each series retains its native status: `Complete` is complete data; `PartialData` remains incomplete until resolved; `InternalError` permits a retry with the token where present; `Forbidden` requires access correction. Math-expression results may not provide a continuation token, so partial results cannot be assumed recoverable by pagination.

## 3. Report evidence

Values are paired with their corresponding timestamps and query identifiers. Global messages and per-series messages are preserved. An empty complete series is reported as no returned samples for the requested metric/unit/window, not zero utilization or a healthy service.

## Patterns

Statistics and period are part of the evidence. Aggregating retained data does not restore earlier high-resolution samples.

## Known limitations

This procedure assumes metric identity and statistic are known; it does not invent service-specific thresholds or a diagnosis from a counter name. CloudWatch retention and metric availability constrain historical queries. AWS credentials/signing failures and service errors block the affected read; the generic API does not establish a fixed retry count.

## Tools

| Operation | Description | Category |
|---|---|---|
| Query metric data | Retrieves metric statistics and expression results | Read |

## Verification checklist

- Metric dimensions, account/region, statistic, unit and interval are recorded.
- Timestamps align with values.
- Pagination, messages and each series' completion status are accounted for.
