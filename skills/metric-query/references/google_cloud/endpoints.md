# Cloud Monitoring v3 binding

Source: [projects.timeSeries.list](https://docs.cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list),
retrieved 2026-10-09.

`GET https://monitoring.googleapis.com/v3/projects/{project}/timeSeries`, using an authenticated
client with a documented scope such as `https://www.googleapis.com/auth/monitoring.read`.
The request body is empty.

Required query fields: `filter` (exactly one `metric.type` plus optional label predicates),
`interval.startTime`, `interval.endTime`, and `view` (`FULL` or `HEADERS`).
Optional: `aggregation`, `secondaryAggregation` (requires primary aggregation), `pageSize`, `pageToken`.
`orderBy` is unsupported and remains unset. `nextPageToken` from a response supplies the next request's
`pageToken`. The default/effective maximum page size is 100,000; with `FULL` it counts points,
and with `HEADERS` it counts time series.
