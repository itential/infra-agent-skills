# AWS CloudWatch Logs: Logs Insights Query

Sources: Amazon CloudWatch Logs API Reference, StartQuery and GetQueryResults (retrieved 2026-10-26).

## Common Sequences

- **Retrieve events:** Start query → Poll results until a terminal status → Read remaining pages.

## Start query

Submit the caller's Logs Insights query with start and end times (epoch seconds, both inclusive), the log groups to search, and optionally a maximum result count. Name log groups in exactly one way (a single name, a list of names, or identifiers) unless the query text itself selects sources. Up to 50 log groups can be named. A monitoring account can query linked source accounts using ARNs. Up to 100 queries can run concurrently per region, shared with scheduled queries. Not documented: query price. Keep the time range and log group set as narrow as the request allows.
- Success: a query identifier. It does not mean the query succeeded.
- Invalid parameter or malformed query: fix and resubmit. Missing resource: check names and access. Limit exceeded: wait for running queries. Service unavailable: the submission is unverified; retry after a pause and back off on throttling, honoring any `Retry-After` header.

## Poll results

Read results using the query identifier. Status values are scheduled, running, complete, failed, cancelled, timeout, and unknown. Running returns partial results only. Queries time out after 60 minutes; narrow the time range or split the query rather than retrying unchanged.
- Complete: results are final.
- Failed, cancelled, timeout, unknown: report that status; it is not an empty success.

## Read remaining pages

When a continuation token is returned, request the next page with it. A page holds up to 10,000 events and a query can return up to 100,000 events in total (Logs Insights QL only; not PPL or SQL). Tokens expire after one hour.

## Patterns

- Results hold only the requested fields plus a record pointer that can retrieve the full record.
- Statistics report records scanned and matched, and bytes scanned; they describe the full run, not the returned page.
- Not documented: API-level request rate limits. Back off on throttling errors.

## Known limitations

Query start and retrieval only. No log group creation, retention change, or query cancellation. Result retention for past queries is defined in the service quotas. Not documented: retention of past query results.

## Tools

| Operation | Description | Category |
|---|---|---|
| Start query | Submit a query over log groups and a time range | SDK/API call |
| Get query results | Read status, rows, statistics, and tokens | SDK/API call |

## Verification checklist

- [ ] Account, region, log groups, interval, and query text are recorded.
- [ ] Status was complete (or the non-complete status was reported) and all tokens were consumed or reported as unread.
- [ ] A result limit or per-query cap is reported as a bound, not as the total.
