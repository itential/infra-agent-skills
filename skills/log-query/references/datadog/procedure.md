# Datadog log search

Read matching log events through the documented v2 cursor-paged search.

Primary sources: [v2 search](https://docs.datadoghq.com/api/latest/logs/search-logs-post/) and
[paging guide](https://docs.datadoghq.com/logs/guide/access-your-log-data-programmatically/),
retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## 1. Select the search

The operation uses a query, time interval, selected indexes/storage tier, sort order, and page bound.
The authenticated principal needs log-read permission for the account's Datadog site.

## 2. Read and continue pages

A successful call returns event objects and metadata. The continuation cursor supplies the next
page with the remaining search parameters unchanged. Each result retains its identifier, timestamp,
message, and relevant attributes. An operator-selected page bound is reported as partial coverage.

## 3. Check completion and errors

A completed search carries the native done status. Timeout status or warnings can accompany partial
data and remain visible. Bad requests (400) require parameter correction; authorization errors (403)
require access review; throttling (429) follows applicable rate-limit guidance. The endpoint does not
specify a universal retry interval.

## Patterns

Paging metadata controls continuation; the number of rows in one page is not the total number of
matching events. The old global timezone/time-offset options are deprecated and do not affect the
query, so this procedure uses explicit time boundaries.

## Known limitations

Log search is not an archive/export replacement. Index configuration and pipeline administration
are outside this sequence. NetClaw's custom MCP tool names and automatic sanitization are not assumed.

## Tools

| Operation | Description | Category |
|---|---|---|
| Search log events | Read matching events and continuation metadata | Read |

## Verification checklist

- Site, indexes/storage tier, filter, interval, and sort match the request.
- Native status/warnings and any unread continuation cursor are reported.
