# Grafana Loki: Bounded Range Query over Log Streams

Sources: Grafana Loki 3.6 documentation, Grafana Loki HTTP API, Log queries, Metric queries, Manage tenant isolation, and Grafana Loki configuration parameters (`limits_config` defaults) (retrieved 2026-11-02).

## Common Sequences

- **Retrieve events:** Check the query → Settle the tenant → Read build information → Confirm the stream → Run range query → Qualify response.
- **Retrieve a window larger than one page, or longer than the query length cap:** Check the query → Settle the tenant → Read build information → Confirm the stream → Read the window in slices.

## Check the query

Before any call, confirm that the caller's expression is a log query: a stream selector in braces with at least one label matcher, optionally followed by filter or parser stages.
- An expression that applies a function over a time range to a selector (such as `count_over_time` or `rate`), or aggregates the result (such as `sum by`), is a metric query. It returns numbers, not log lines, and is not covered here even when the caller asks for it by name: do not send it; report that it is outside this skill and stop.

## Settle the tenant

Loki is multi-tenant unless configured otherwise, and then every call names the tenant (see `endpoints.md`), even when only one tenant exists. With multi-tenancy turned off, no tenant is named. Use the tenant the caller names, or the one the existing client already sends. If neither says which mode applies, ask before the first call.

## Read build information

Read the server's version. This procedure follows Loki 3.6; report the version found next to the result, and treat behavior on another release as unverified.
- A refused request (an HTTP error status): report the version as unknown, with the status and Loki's message, and go on; behavior is then unverified.

## Confirm the stream

Choose one label from the caller's selector whose matcher cannot match an empty value: `=` with a non-empty value, or `=~` with a pattern that needs at least one character. List that label's values over the window, narrowed by the braces selector alone, without filter or parser stages. The narrowing applies every label matcher, so one listing answers for all of them.
- No matcher of that kind in the selector: a listing cannot confirm the stream. Skip this step and say in the result that whether a stream matches was not checked.
- At least one value is listed: a stream matches; go on.
- No value is listed: no stream matches the selector. Report that, not an absence of events, and stop.
- Any status other than success: report the status and Loki's message and stop. A refused listing says nothing about whether a stream matches.
- A listing can reach back beyond the window, so a listed value does not prove the stream logged inside it.
- Not documented: whether the query length cap (see Run range query) also applies to a listing. If a listing over a long window is refused, list each part no longer than the cap; a value listed in any part means a stream matches.

## Run range query

Send the caller's log query with an explicit start and end; never rely on the defaults (start one hour before end, end now). Entries at the start are included and entries at the end are not.
- Set the entry limit at or under the deployment's cap (5,000 by default); it defaults to 100.
- The deployment also caps the length of a query's window (30 days and 1 hour by default). A longer window is read in slices. Use the default unless the caller gives another value (see Known limitations). If a query is refused and Loki's message names the query length, halve the window and read both halves.
- Order is newest first by default; oldest first (forward) is also available.
- Success: a status of success and a result type of streams. Each stream carries its label set and its entries, each a timestamp in nanoseconds and the line.
- Any other status, or a refused request: report the status and Loki's message, and do not rewrite the caller's expression.

## Qualify response

Count the entries across every stream in the response. Loki has no completion signal; this count against the limit is the completeness check.
- Fewer than the limit: the limit was not reached, so that window was read in full, within the limits below.
- Exactly the limit: the page is bounded, and more entries may exist anywhere in its window (see Patterns). Read the window in slices, or report the result as bounded with its count.
- A deployment can cap how far back a query reaches. A window that reaches past the cap is shortened, not refused, and retention deletes older entries. Neither limit is visible in the response: report that the older end of the window may be cut by them.
- A query that outruns the deployment's query timeout (one minute by default) gives no usable result. Not documented: whether partial entries come back; treat any status other than success as no result, and narrow the window or the selector.

## Read the window in slices

Loki has no page cursor; a complete range is read with repeated range queries over smaller windows.
- Cut the window into consecutive slices, each no longer than the query length cap and each starting where the previous one ended, and run the range query on each with the same query, limit and order.
- Read the slices oldest first when the order is forward, and newest first when it is backward.
- A slice that comes back full is cut in two and both halves are read again, in the same order. Never continue from a full page's last timestamp.
- If the caller set a result bound, merge the entries of each slice below the limit across streams by timestamp, count them in reading order and stop once the count reaches the bound, keeping from the last slice read only the entries needed to reach it. Report the result as bounded there, with the part of the window read.
- A slice whose start and end are one nanosecond apart cannot be cut. If it still comes back full, report that part of the window as not fully readable.
- The window is read in full when every slice came back with fewer entries than the limit. Report the total across slices and the number of slices read. Qualify response's lookback, retention and timeout points still apply.

## Patterns

- Not documented: which entries a full page holds. Do not take them as the oldest or newest entries of the window.
- Timestamps are nanosecond integers carried as strings; compare them and set slice bounds as integers, since a float loses the last digits.
- Index statistics give an approximate count that leaves out data still held by the ingesters; never report them as a match count.
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
