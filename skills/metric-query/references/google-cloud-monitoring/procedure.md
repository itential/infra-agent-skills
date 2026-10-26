# Google Cloud Monitoring time-series query

List time series for one metric type in a project, folder, or organization over a bounded interval.

Sources: Cloud Monitoring API v3 reference for the time series list method (retrieved 2026-10-26). Bindings: [endpoints.md](endpoints.md).

Read-only: no confirmation gates apply.

## Common Sequences

- Metric values: Scope the query, then Retrieve and page, then Report.

## Scope the query

Choose the parent (project, organization, or folder), a filter naming exactly one metric type with optional label predicates, a time interval, and a view: full (points) or headers (series identities only). Optionally add alignment and reduction settings, and a second aggregation (only valid with the first).

## Retrieve and page

Send the read. Success is a response with matching series and, when more remain, a token for the next page.

- The default and maximum page size is 100,000. With the full view it counts points; with headers it counts series.
- Without aggregation, raw series come back.
- Follow the token until none is returned.
- Points are returned newest first; ordering by the server is not supported, so do not set an ordering.
- Authorization needs one of the cloud-platform, monitoring, or read-only monitoring scopes.
- Not documented on this method's page: rate limits, quota values, and an error catalogue. Treat any API error as an unsuccessful query; on HTTP 429, back off and honor any Retry-After header.

## Report

State the parent, metric type, interval, view, aggregation, and paging state with the series. Changing aggregation changes the question answered. A page-size limit is not a total count.

## Known limitations

- One metric type per filter.
- Alert policies and metric discovery are not covered.

## Tools

| Operation | Description | Category |
|---|---|---|
| List time series | Retrieve matching series and continuation pages | Read |

## Verification checklist

- Parent, metric type, interval, and view match the request.
- Aggregation and continuation state appear in the report.
- Errors are reported as failures, not as empty data.
