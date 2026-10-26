# Amazon CloudWatch metric query

Read metric statistics or metric-math results for a bounded window with the metric-data retrieval operation.

Sources: AWS CloudWatch API reference pages for GetMetricData and MetricDataResult (retrieved 2026-10-26). Bindings: [endpoints.md](endpoints.md).

Read-only: no confirmation gates apply.

## Common Sequences

- Metric values: Specify the request, then Retrieve and page through results, then Report the evidence.

## Specify the request

Identify the AWS account and region, then for each query give a unique ID and either a metric (namespace, metric name, dimensions, period, statistic, optional unit) or a math expression over other queries. Add a start and end time.

- Start is inclusive, end is exclusive. Older starts are rounded down: to the minute if under 15 days old, to a 5-minute boundary at 15 to 63 days, to an hour beyond 63 days.
- Retention by resolution: periods under 60 seconds for 3 hours (custom high-resolution metrics only), 60 seconds for 15 days, 5 minutes for 63 days, 1 hour for 455 days. Older data is only available at the coarser resolution.
- A specified unit that does not match the collected unit returns null results; no unit conversion occurs. Omit the unit to get all.
- Up to 500 queries per request and 100,800 data points per page by default.

## Retrieve and page through results

Send the request. Success is HTTP 200 with a result per query plus an optional continuation token.

- Repeat the identical request with the token until none is returned. The default order is newest first.
- Per-series status: Complete means all points in range were returned; PartialData means more can be fetched with the token; InternalError means retry using the token if present; Forbidden means access must be corrected.
- Math-expression results do not return a token, so partial expression results cannot be completed by paging.
- An invalid token returns HTTP 400 (see endpoints.md); restart the query rather than reporting a complete result.
- Global and per-series messages can accompany a success; keep them.
- Rate limits and throttling: not documented on the reference pages for this operation. On a throttling error, back off before retrying and honor any Retry-After header.

## Report the evidence

Pair each value with its timestamp and query ID, with account, region, statistic, period, and unit. An empty complete series means no samples for that metric, unit, and window; it does not mean zero utilisation or a healthy service.

## Patterns

- Statistic and period are part of the evidence; coarser periods cannot be turned back into finer samples.
- Aligning start and end to the period and hour boundaries gives faster responses.

## Known limitations

- Metric identity (namespace, name, dimensions) must be known; discovery is not covered.
- Metrics Insights queries are a different query form and are not covered.

## Tools

| Operation | Description | Category |
|---|---|---|
| Get metric data | Retrieve metric statistics and expression results | Read |

## Verification checklist

- Account, region, dimensions, statistic, period, unit, and window are recorded.
- Timestamps pair with values and every token was followed to the end.
- Each series' status and all messages are reported.
