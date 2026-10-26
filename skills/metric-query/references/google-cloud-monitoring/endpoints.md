# Cloud Monitoring v3 time series list binding

Source: Cloud Monitoring API v3 reference for the time series list method (retrieved 2026-10-26).

`GET https://monitoring.googleapis.com/v3/{name}/timeSeries` with an empty body. `{name}` is `projects/{project}`, `organizations/{organization}`, or `folders/{folder}`.

Required query parameters: `filter` (one `metric.type` plus optional label predicates), `interval` (`interval.startTime`, `interval.endTime`), `view` (`FULL` or `HEADERS`).

Optional: `aggregation`, `secondaryAggregation`, `pageSize` (default and maximum 100,000), `pageToken`. `orderBy` is unsupported. The response's `nextPageToken` feeds the next `pageToken`.

OAuth scopes: `https://www.googleapis.com/auth/cloud-platform`, `.../monitoring`, or `.../monitoring.read`.
