# Grafana Loki: Bounded Range Query over Log Streams

Sources: Grafana Loki 3.6 documentation, HTTP API reference, Log queries, Manage multi-tenancy, and Configuration (`limits_config` defaults) (retrieved 2026-11-02).

## Common Sequences

- **Retrieve events:** Read build information → Confirm the stream → Run range query → Qualify response.
- **Retrieve a window larger than one page:** Read build information → Confirm the stream → Read the window in slices.

## Read build information

Read the server's version. This procedure follows Loki 3.6; report the version found next to the result, and treat behavior on another release as unverified.

## Confirm the stream

For each label in the caller's stream selector, list that label's values over the same window, narrowed by the selector.
- The caller's value is listed: a stream matches; go on.
- The value is missing: no stream matches the selector. Report that, not an absence of events, and stop.
- The listing can reach further back than the window asked for, so a listed value does not prove the stream logged inside the window.

## Run range query

Send the caller's log query with an explicit start and end; never rely on the defaults (start one hour before end, end now). Entries at the start are included and entries at the end are not.
- The query must be a log query: a stream selector in braces with at least one label matcher, optionally followed by filter or parser stages. A metric query returns numbers, not lines; report that it is outside this procedure.
- Set the entry limit; it defaults to 100 and the deployment caps it (5,000 by default). Not documented: the response to a limit above the cap, so keep the limit at or under it.
- Order is newest first by default; oldest first (forward) is also available.
- On a deployment that runs several tenants, name the tenant on every call (see `endpoints.md`); a single-tenant deployment needs none.
- Success: a status of success and a result type of streams. Each stream carries its label set and its entries, each a timestamp in nanoseconds and the line.
- Any other status, or a refused request: report the status and Loki's message, and do not rewrite the caller's expression. Not documented: the status code and body for an invalid query.

## Qualify response

Count the entries across every stream in the response.
- Fewer than the limit: the window was read in full, within the limits below.
- Exactly the limit: the page is bounded. More entries may exist, including entries inside the span between the oldest and newest timestamps it returned (see Patterns). Read the window in slices, or report the result as bounded with its count.
- A deployment can cap how far back a query reaches. A window that reaches past the cap is shortened, not refused, and retention deletes older entries. Neither limit is visible in the response: report that the older end of the window may be cut by them.
- A query that runs longer than the deployment's query timeout (one minute by default) does not give a usable result. Not documented: whether partial entries come back; treat any status other than success as no result, and narrow the window or the selector.

## Read the window in slices

Loki has no page cursor; a complete range is read with repeated range queries over smaller windows.
- Cut the window into consecutive slices, each slice's start equal to the previous slice's end, and run the range query on each with the same query and limit.
- A slice that comes back full is cut in two and both halves are read again. Never continue from a full page's last timestamp.
- The window is read in full when every slice came back with fewer entries than the limit. Report the total count across slices and the number of slices read.
- A slice too short to cut further that still comes back full holds more entries than the limit allows: report that part of the window as not fully readable.
- Because a slice's start is included and its end is not, consecutive slices neither overlap nor leave a gap.

## Patterns

- A full page is not the oldest or newest entries of the window. Observed on Loki 3.6.12 over several streams: a full page, in either order, left out entries from inside its own time span. A page that comes back short of the limit held every entry in its window.
- Timestamps are nanosecond integers carried as strings; keep them as integers when comparing them or setting slice bounds, since a float loses the last digits.
- Index statistics give an approximate count that leaves out data still held by the ingesters; never report them as a match count.
- The instant query refuses log queries as a bad request; log lines come only from the range query.
- The live tail is for watching new lines and does not guarantee a complete history.
- Not documented: rate limits. On HTTP 429, back off and honor any `Retry-After` header.

## Known limitations

No push, deletion, rule or configuration calls. Metric queries, live tailing, and queries across several tenants in one call are not covered. The deployment's own limits (lookback cap, retention, entry cap) cannot be read through the query calls.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read build information | Retrieve the server's version | REST API |
| List label values | Retrieve the values one label takes over a window | REST API |
| Run range query | Retrieve log entries for a query over a window | REST API |

## Verification checklist

- [ ] The window was given as an explicit start and end, and the limit and order used are reported.
- [ ] Every page's entry count was compared with the limit; a count from a full page is reported as bounded, never as a total.
- [ ] A selector value missing from the label listing is reported as no matching stream.
- [ ] The lookback cap and retention are named as possible limits on the window's older end.
