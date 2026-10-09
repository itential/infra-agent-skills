# CloudWatch Logs Insights bindings

Sources: [DescribeLogGroups](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DescribeLogGroups.html), [StartQuery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_StartQuery.html), [GetQueryResults](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_GetQueryResults.html), retrieved 2026-10-09.

An authorized AWS SDK Logs client binds account/region and signing. SDK operations (Boto3 equivalents):

| Operation | SDK operation | Fields |
|---|---|---|
| Discover groups | `DescribeLogGroups` / `describe_log_groups` | Optional `logGroupNamePrefix` or `logGroupNamePattern` (not both); `nextToken`; response `logGroups`, `nextToken` |
| Start QL query | `StartQuery` / `start_query` | Required `startTime`, `endTime` (epoch seconds, inclusive), `queryString`; `queryLanguage: CWLI`; exactly one of `logGroupName`, `logGroupNames`, `logGroupIdentifiers`; optional `limit`; response `queryId` |
| Retrieve | `GetQueryResults` / `get_query_results` | `queryId`, optional `nextToken`, `maxItems`; response `status`, `results`, `statistics`, `nextToken` |

Current QL limit: up to 100,000 query results, at most 10,000 per result request; result token expires after one hour. Up to 50 explicitly selected log groups. These values are current API limits, not claims about every older SDK model.

Exact errors: `InvalidParameterException` (400), `ResourceNotFoundException` (400), `ServiceUnavailableException` (500). Submission additionally returns `LimitExceededException` or `MalformedQueryException` (400, query compilation detail). Discovery documents invalid parameter and unavailable-service errors. Preserve AWS authentication/permission diagnostics and request identifiers without credentials.
