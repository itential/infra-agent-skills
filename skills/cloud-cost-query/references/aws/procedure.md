# AWS cost and forecast queries

Retrieve scoped billing measurements, forecasts or recorded anomalies with their native units and qualification.

Sources: AWS current [cost and usage](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [forecast](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostForecast.html), and [anomalies](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetAnomalies.html) references, retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Cost breakdown: Read cost/usage → Continue pages.
- Forecast: Read forecast.
- Investigate an anomaly: Read anomalies → Continue pages → Read cost/usage for the selected scope.

## Read cost/usage

The selected metric, billing scope, date interval, granularity and optional grouping/filter define the request. Historical intervals include their start and exclude their end. Results retain time buckets, group keys, amount, unit and estimated flags. Usage quantities with different units cannot form a meaningful total; the publisher recommends narrowing usage type/group before aggregating usage. Up to two group dimensions are supported. An empty result does not establish that an unqueried account or service had no cost.

## Read forecast

Forecast retrieval returns the mean and, if requested, a prediction interval. Supported cost forecast granularities are daily or monthly; the reference's shared enum also shows hourly, but its operation-specific rule excludes hourly. The returned forecast is an estimate, not a bill or guaranteed saving. Missing historical data or an unhealthy billing view leaves the forecast unavailable.

## Read anomalies

Anomaly retrieval selects a date interval and optional monitor, feedback, or impact filter. The response returns detected anomaly records; the interval selects their end dates. Its history is limited to the service's available anomaly retention. No anomaly returned is not an independent proof that all spending was expected.

## Continue pages

Cost and anomaly queries continue with each returned token. Query parameters stay identical. An invalid token requires a fresh sequence; a changed-request error requires the original parameters or a restart. Failed or abandoned pagination remains incomplete.

## Error handling

For applicable operations: expired reports require a different date interval; unhealthy billing views must become healthy; unavailable data remains unavailable; missing resource ARNs require scope correction; request-rate limits require waiting before another read. Validation errors require corrected inputs. No numeric retry delay is assumed. Exact error names are in the binding.

## Patterns

A management account can query member-account billing data where authorized. Date, metric and grouping must remain constant for a meaningful comparison; the procedure does not automatically classify one service as excessive.

## Known limitations

Service-specific prices, free-tier eligibility, lag guarantees, savings recommendations and CloudTrail correlation are outside this billing procedure. Forecast dates are supplied explicitly; the published date-rule wording must be checked against current API validation if rejected.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read cost/usage | Returns actual/estimated historical billing measurements | Read |
| Read forecast | Returns modeled cost and prediction interval | Read |
| Read anomalies | Returns service-detected anomalies | Read |

## Verification checklist

- Date interval, scope, metric and units are retained.
- Estimates and forecasts are labeled.
- Pagination and unavailable-data errors are accounted for.
