# Grafana Loki: Label Discovery and LogQL Stream Query

Sources: Grafana Loki documentation, HTTP API reference (latest), retrieved 2026-10-26.

## Common Sequences

- **Query logs:** List labels and values → Run stream query.

## List labels and values

Read the label names and then the values of a label for the target time window, optionally narrowed by a stream selector. Use real labels to build the selector for the query. A failed label read is a coverage gap in the label set.

## Run stream query

Send the caller's LogQL log query with a start, end, entry limit, and direction (newest first by default). Time may be nanosecond epoch, fractional epoch, or RFC 3339. The limit defaults to 100 entries; the start defaults to one hour back and the end to now when omitted, so set both explicitly.
- Success: a success status and a result of type streams, each stream holding its labels and (timestamp, line) pairs with nanosecond string timestamps.
- A result of type matrix means a metric query was sent; this skill reads log streams only.
- LogQL syntax errors return 400: fix the query. 429: rate limited; back off and honor any `Retry-After` header.
- Multi-tenant deployments need the tenant identifier header; several tenants are separated by a pipe. Without it the query may reach the wrong tenant or fail (unverified: the failure form).

## Patterns

- The entry limit applies per query across streams, so a full limit means the result is likely truncated; narrow the window or selector instead of raising limits blindly.
- Not documented: server-side maximum entries, authentication scheme, and rate limits. Treat a lower returned count than requested with a full-window query as the only completeness signal.

## Known limitations

Log queries only; no metric queries, log push, or tailing.

## Tools

| Operation | Description | Category |
|---|---|---|
| List labels and values | Read stream label names and values | REST API |
| Run stream query | Read log entries for a LogQL selector | REST API |

## Verification checklist

- [ ] Tenant, selector, window, direction, and limit are recorded.
- [ ] A result at the limit is reported as possibly truncated.
- [ ] Errors and empty results are not reported as absence of logs.
