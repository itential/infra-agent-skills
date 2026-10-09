# Google Cloud Monitoring time-series query

Read one metric type within a chosen project and interval.

Primary source: [time-series list](https://docs.cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list),
Monitoring v3, retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## 1. Select query scope

The documented query selects a project, one metric type, and an interval. Labels may narrow that
selection. A full-data view returns points; a headers view returns series identities.

## 2. Retrieve the series

The authenticated read includes optional alignment/reduction settings. Without aggregation, raw
series are returned. Success supplies the selected view. The page-size unit differs between views:
points for full data, series for headers. The response's continuation token retrieves the next page.

## 3. Interpret the result

Points are returned newest first. Server-side sorting is unsupported. The report retains the actual
interval, labels, aggregation, and pagination state. Operation-specific retry intervals and a
complete error catalogue are not stated on this method page; an API error remains an unsuccessful
query, and deployment-specific error guidance applies.

## Patterns

Changing aggregation changes the question being answered. A page-size limit is not a total-count
assertion about the metric.

## Known limitations

This covers time-series reads only. Alert-policy management, incident queries, and universal device
metric names are not established by this method.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read time series | Retrieve matching series and continuation pages | Read |

## Verification checklist

- The selected project, metric type, interval, and view match the request.
- Aggregation and continuation state are visible in the result.
- Errors are not represented as successful empty data.
