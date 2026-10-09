# Datadog time-series points

Retrieve values for a supplied Datadog metric expression and time range.

Primary source: [query time-series points](https://docs.datadoghq.com/api/latest/metrics/query-timeseries-points/),
Metrics API v1, retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## 1. Scope the query

The operation requires a metric expression, start time, end time, and permission to query time series.
The client uses the account's Datadog site.

## 2. Read the points

The query returns series, their labels, units, and points. Input times use epoch seconds; returned
point times use milliseconds. A successful response is checked for its native status and any error.
Bad input (400) requires query/parameter correction; forbidden access (403) requires permission
review; throttling (429) remains a rate-limit failure and follows the deployment's retry guidance.
This endpoint page does not establish a fixed retry delay.

## 3. Report the observation

The result retains the expression, actual series, units, sample interval, and time range. An empty
series is a query result, not a conclusion that a service was healthy or unmonitored.

## Patterns

Time units differ across input and output. Conversion precedes comparison with another backend.

## Known limitations

Datadog recommends its v2 time-series endpoint for new integrations. This deliberately scoped v1
binding does not cover dashboards, metric discovery, forecasts, or capacity recommendations.

## Tools

| Operation | Description | Category |
|---|---|---|
| Query metric points | Read scoped metric values | Read |

## Verification checklist

- The site, time range, and query match the request.
- Native status, units, labels, sample interval, and timestamp units are preserved.
