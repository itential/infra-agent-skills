# Google Cloud Logging: List Entries with Page Tokens

Sources: Google Cloud Logging API reference, entries.list (v2) (retrieved 2026-10-26).

## Common Sequences

- **Retrieve entries:** Select resources and filter → List entries → Continue with page tokens.

## Select resources and filter

Name the parent resources to search (projects, folders, organizations, billing accounts, or specific log views; up to 100) and a filter in the Logging query language, at most 20,000 characters. An empty filter returns everything in the named resources. A timestamp range and indexed fields make the search faster. A filter that names a resource not listed among the parents matches nothing.

## List entries

Request entries with a page size (default 50; negative is rejected) and an order: oldest first by default, or newest first, which suits recent events. Equal timestamps are ordered by insert identifier.
- Success: entries and, when more may exist, a page token.
- Permission errors do not show that the resource has no logs.

## Continue with page tokens

Repeat the same request with the previous token and everything else unchanged. An empty page that carries a token means the search ran out of time before covering everything: keep going. The search is complete when a response carries no token, or when the caller's own result bound is reached and reported.

## Patterns

- Searches over a parent can span storage regions. If a region is unavailable, searching only log views that exclude it is documented; the result then has a coverage gap that must be reported.
- Authorization needs an OAuth read scope and an IAM permission to list entries (or to access the view).
- Not documented in the sources read: quotas and rate limits. On HTTP 429 or a quota error, back off and honor any `Retry-After` header.

## Known limitations

Entry reads only; no sinks, exclusions, retention, or log-based metrics.

## Tools

| Operation | Description | Category |
|---|---|---|
| List entries | Read a filtered page of entries and a continuation token | REST API |

## Verification checklist

- [ ] Parents, filter, order, and page size match the request.
- [ ] Pages were read until no token remained or the bound was reported.
- [ ] Permission or transport errors are separate from empty matches.
