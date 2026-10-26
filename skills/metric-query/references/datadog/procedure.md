# Datadog metric time-series query

Query metric time series on Datadog with the v2 timeseries query operation, limited to the metrics data source.

Sources: Datadog API reference, Metrics section, "Query timeseries data across multiple products" and API rate-limit page (retrieved 2026-10-26). Bindings: [endpoints.md](endpoints.md).

Read-only: no confirmation gates apply.

## Common Sequences

- Metric values: Scope the query, then Run the query, then Report the series.

## Scope the query

Gather the metric query expression (Datadog metric query syntax), a name for it, a start and end time, and optionally an interval. The operation also takes a formula referencing the query name. Use the site the account belongs to; the same operation exists on each Datadog site.

- The operation can query other data sources (logs, spans, events, SLOs, and more); this procedure uses only the metrics source.
- Cross-organization queries are limited to one organization.
- OAuth clients need the timeseries query scope.

## Run the query

Submit the request. Success is HTTP 200 with a timeseries response holding series (group tags, query index, unit), a times array, and a values array.

- The interval is adjusted automatically if too fine for the window.
- Documented errors: 400 bad request, 401 unauthorized, 403 forbidden, 429 rate limited. Each returns a list of error strings. Fix the request for 400, credentials for 401, permissions for 403.
- On 429, wait and retry. The rate-limit page documents reset headers and does not document Retry-After; use the reset and period headers to size the wait. A limit specific to this operation is not documented.

## Report the series

Report the expression, window, interval, group tags, units, and the time/value pairs together. A graph holds a limited number of points, so longer windows are aggregated. An empty series is a query result, not evidence that a service is healthy or unmonitored.

## Patterns

- Request times are in milliseconds; convert units before comparing with another backend.

## Known limitations

- Unconfirmed: the unit of the response `times` values (assumed milliseconds to match the request), and the exact credential headers for this operation (assumed to be the standard Datadog API key and application key pair).
- The v1 query endpoint, metric discovery, and non-metrics data sources are not covered.

## Tools

| Operation | Description | Category |
|---|---|---|
| Query timeseries | Return series for a metrics query over a window | Read |

## Verification checklist

- Site, expression, window, and interval match the request.
- Group tags, units, and times line up with values.
- Errors and 429 responses are reported as failures, not as empty data.
