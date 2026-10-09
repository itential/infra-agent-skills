# CloudWatch Logs Insights query

Start and retrieve a bounded Logs Insights QL query against selected log groups.

Sources: AWS current [log-group discovery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DescribeLogGroups.html), [start query](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_StartQuery.html), [query results](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_GetQueryResults.html), retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## 1. Select log groups

Discovery returns visible groups and continuation tokens. The account/region, selected groups and requested time interval define the query scope; a missing group is not evidence that traffic never existed. Discovery errors for malformed inputs require correction; service-unavailable errors leave discovery incomplete. Delivery-class groups do not support Insights queries.

## 2. Start the query

The request specifies the QL expression, inclusive start/end times and exactly one explicit log-group selector. A successful submission returns a query identifier. Invalid parameters or malformed query syntax require correcting the diagnostic; a missing resource requires checking its identity/access; quota failures require available query capacity; a service failure leaves submission unverified. Starting a query can incur query charges; no fixed price is assumed here.

## 3. Retrieve completion and pages

The query identifier selects results. `Scheduled` or `Running` requires later retrieval; running results are partial. `Complete` permits reading all pages using the result continuation token. `Failed`, `Cancelled`, `Timeout`, and `Unknown` remain those outcomes, never a successful empty query. Query timeout guidance is to reduce or partition the time range for a new query. Result-lookup invalid input, missing query/resource, or unavailable-service errors remain failures.

## 4. Report

Returned records retain their field/value pairs and pointer; statistics describe scan/match volume. Completion includes all available pages within the requested query limit, not proof all matching events were returned without a limit. The result records account/region, group scope, interval, expression, query identifier and native status.

## Patterns

Submitting and retrieving are separate operations. A query identifier does not prove the query ran successfully. Current QL results support pagination beyond one result page; a fixed 10,000-total-results assumption is outdated.

## Known limitations

This binding covers Logs Insights QL, not SQL or PPL. It neither enables logging nor changes log retention. Flow-log fields must match the actual selected group's format; an invented field mapping is not a valid traffic diagnosis.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover groups | Lists visible log-group metadata | Read |
| Start query | Submits a bounded QL query | Query |
| Retrieve results | Reads status and result pages | Read |

## Verification checklist

- Query scope and time units are explicit.
- Completion status and all continuation tokens are handled.
- Limits, scan statistics, and failures remain visible.
