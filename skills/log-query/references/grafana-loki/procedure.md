# Grafana Loki: Bounded Range Query over Log Streams

Sources: Grafana Loki 3.6 documentation, HTTP API reference, Log queries, Metric queries, Manage multi-tenancy, and Configuration (`limits_config` defaults) (retrieved 2026-11-02).

## Common Sequences

- **Retrieve events:** Check the query → Read build information → Confirm the stream → Run range query → Qualify response.
- **Retrieve a window larger than one page, or longer than the query length cap:** Check the query → Read build information → Confirm the stream → Read the window in slices → Qualify response.

## Check the query

Before any call, confirm that the caller's expression is a log query: a stream selector in braces with at least one label matcher, optionally followed by filter or parser stages.
- An expression that applies a function over a time range to a selector (such as `count_over_time` or `rate`), or aggregates the result (such as `sum by`), is a metric query. It returns numbers, not log lines, and this procedure does not cover it, even when the caller asks for it by name. Do not send it; report that it is outside this skill and stop.
- Settle the tenant before the first call. Loki runs in multi-tenant mode unless configured otherwise, and in that mode every call names the tenant (see `endpoints.md`), even when a single tenant uses the deployment. With multi-tenancy turned off, no tenant is named. If neither the caller nor the client says which mode applies, ask.

## Read build information

Read the server's version. This procedure follows Loki 3.6; report the version found next to the result, and treat behavior on another release as unverified.
- Any status other than success: report the status and Loki's message and stop.

## Confirm the stream

Choose one label from the caller's selector that is matched with `=` or `=~`, and list its values over the window, narrowed by the whole selector. The narrowing applies every matcher in the selector, so one listing answers for all of them.
- At least one value is listed: a stream matches; go on.
- No value is listed: no stream matches the selector. Report that, not an absence of events, and stop.
- Any status other than success: report the status and Loki's message and stop. A refused listing says nothing about whether a stream matches.
- The listing can reach further back than the window asked for, so a listed value does not prove the stream logged inside the window.
- Not documented: whether the query length cap (see Run range query) also applies to a listing. If a listing over a long window is refused, list each part no longer than the cap; a value listed in any part means a stream matches.

## Run range query

Send the caller's log query with an explicit start and end; never rely on the defaults (start one hour before end, end now). Entries at the start are included and entries at the end are not.
- Set the entry limit; it defaults to 100 and the deployment caps it (5,000 by default). Not documented: the response to a limit above the cap, so keep the limit at or under it.
- The deployment also caps the length of a query's window (30 days and 1 hour by default). A longer window is read in slices. Not documented: the status for a window over the cap.
- Order is newest first by default; oldest first (forward) is also available.
- Success: a status of success and a result type of streams. Each stream carries its label set and its entries, each a timestamp in nanoseconds and the line.
- Any other status, or a refused request: report the status and Loki's message, and do not rewrite the caller's expression. Not documented: the status code and body for an invalid query.

## Qualify response

Count the entries across every stream in the response, or in each slice when the window was sliced.
- Fewer than the limit: that window was read in full, within the limits below.
- Exactly the limit: the page is bounded, and more entries may exist anywhere in its window (see Patterns). Read the window in slices, or report the result as bounded with its count.
- A deployment can cap how far back a query reaches. A window that reaches past the cap is shortened, not refused, and retention deletes older entries. Neither limit is visible in the response: report that the older end of the window may be cut by them.
- A query that runs longer than the deployment's query timeout (one minute by default) does not give a usable result. Not documented: whether partial entries come back; treat any status other than success as no result, and narrow the window or the selector.

## Read the window in slices

Loki has no page cursor; a complete range is read with repeated range queries over smaller windows.
- Cut the window into consecutive slices, each no longer than the query length cap and each starting where the previous one ended, and run the range query on each with the same query and limit.
- A slice that comes back full is cut in two and both halves are read again. Never continue from a full page's last timestamp.
- If the caller set a result bound, stop once the entries counted reach it, and report the result as bounded there, with the part of the window read.
- A slice whose start and end are one nanosecond apart cannot be cut. If it still comes back full, report that part of the window as not fully readable.
- The window is read in full when every slice came back with fewer entries than the limit. Report the total across slices and the number of slices read, then qualify it as in Qualify response.
- Because a slice's start is included and its end is not, consecutive slices neither overlap nor leave a gap.

## Patterns

- Not documented: which entries a full page holds. Do not take them as the oldest or newest entries of the window. A full page shows only that its window holds at least the limit.
- Timestamps are nanosecond integers carried as strings; keep them as integers when comparing them or setting slice bounds, since a float loses the last digits.
- Index statistics give an approximate count that leaves out data still held by the ingesters; never report them as a match count.
- The instant query refuses log queries as a bad request; log lines come only from the range query.
- The live tail is for watching new lines and does not guarantee a complete history.
- Not documented: rate limits. On HTTP 429, back off and honor any `Retry-After` header.

## Known limitations

No push, deletion, rule or configuration calls. Metric queries, live tailing, and queries across several tenants in one call are not covered. The deployment's own limits (lookback cap, retention, entry cap, query length cap) cannot be read through the query calls.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read build information | Retrieve the server's version | REST API |
| List label values | Retrieve the values one label takes over a window | REST API |
| Run range query | Retrieve log entries for a query over a window | REST API |

## Verification checklist

- [ ] Only a log query was sent; a metric query was reported as not covered, without running it.
- [ ] Every call named the tenant, unless multi-tenancy is turned off.
- [ ] The window was given as an explicit start and end within the query length cap, and the limit and order used are reported.
- [ ] Every page's entry count was compared with the limit; a count from a full page is reported as bounded, never as a total.
- [ ] A label listing with no value is reported as no matching stream, and a refused listing as refused.
- [ ] The lookback cap and retention are named as possible limits on the window's older end.
