# Datadog Logs: Search Events with Cursor Paging

Sources: Datadog API reference, Logs, Search logs (v2), retrieved 2026-10-26.

## Common Sequences

- **Retrieve events:** Run search → Follow cursor until none is returned or the chosen page bound is reached.

## Run search

Submit a search with the caller's query, a start and end time, optionally the log indexes and storage tier, a sort direction (oldest or newest first), and a page size. Times accept absolute timestamps or relative date math. Without an index list, all indexes are searched. The storage tier can be live indexes, online archives, or flex storage, depending on the account.
- Success: an event array plus a status of done or timeout, a cursor for the next page when more remain, and optional warnings.
- Timeout status or warnings can accompany partial data: report them with the events.
- 400: correct the request. 403: the principal lacks log-read permission (or OAuth scope); stop and report. 429: rate limited; back off and honor any `Retry-After` header.

## Follow cursor

Repeat the same search with the cursor from the previous response, leaving all other fields unchanged, until no cursor comes back. The row count of one page is not the number of matches.

## Patterns

- The old timezone and time-offset options are deprecated; use explicit timestamps or date math.
- Use the API host for the account's own Datadog site; a key from one site does not work against another.
- Not documented in the sources read: the default and maximum page size, and the rate-limit values. Treat them as unknown and rely on the status and 429 handling above.

## Known limitations

Search is not an archive export or index administration. No log pipeline or index configuration.

## Tools

| Operation | Description | Category |
|---|---|---|
| Search log events | Query events and receive a continuation cursor | REST API |

## Verification checklist

- [ ] Site, indexes, storage tier, query, interval, and sort match the request.
- [ ] The search status and any warnings are reported.
- [ ] Remaining cursors are either exhausted or reported as unread.
