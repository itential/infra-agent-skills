# Google Cloud Logging entry search

Retrieve log entries within explicit resource and time boundaries.

Primary source: [entries list](https://docs.cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list),
Logging v2, retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## 1. Select resources and filter

The query names the parent resources or log views and a filter. A time restriction and a specific
log name/resource type can reduce work. A filter naming an unselected parent returns no matches.
Success at this stage is a query scoped to the requested accessible resources.

## 2. Retrieve entries

The authenticated search returns matching entries and may include a continuation token. Newest-first
ordering is documented for recently ingested events. A negative page size is rejected and requires
input correction; permission failures do not establish that the selected resource has no logs.

## 3. Continue the same search

Each subsequent request supplies the previous continuation token with the other parameters unchanged.
An empty page **with a token** means the service has not finished searching; it is not completion.
Completion is the absence of another token, or an explicitly reported operator-selected result bound.

## Patterns

Parent-resource searches can span storage regions. For a region outage, the documentation supports
selecting log views that exclude the unavailable region; doing so changes the scope and the report
identifies the resulting coverage gap.

## Known limitations

No global retention duration or universal flow-log schema is assumed. This operation does not prove
that a firewall denied traffic merely because a VPC flow entry is absent. Detailed API failure/retry
rules beyond this method require the platform's applicable error guidance.

## Tools

| Operation | Description | Category |
|---|---|---|
| Search entries | Retrieve a filtered page of stored events | Read |
| Continue entries | Read the next page of the same query | Read |

## Verification checklist

- Resource names, filter, time range, ordering, and limits match the requested scope.
- All continuation pages were read or the result is explicitly bounded/incomplete.
- Returned entry timestamps remain intact; transport errors are separate from empty matches.
