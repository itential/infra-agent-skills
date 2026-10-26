# Zabbix item history and trends

Read raw history or trend aggregates for a host's monitored items over a bounded interval.

Sources: Zabbix API overview, item.get, item object, history.get, and trend.get reference pages (current manual, retrieved 2026-10-26). Bindings: [endpoints.md](endpoints.md).

Read-only: no confirmation gates apply.

## Common Sequences

- Raw samples: Discover items, then Retrieve history.
- Trend aggregates: Discover items, then Retrieve trends.

## Discover items

Look up items for the host, optionally narrowed by a key fragment, asking for item ID, name, key, value type, units, history retention, trend retention, and last update time.

- No match means no visible item for this user; permissions depend on the user's role and groups. It does not show the host is unmonitored.
- Retention values can be macros. Their effective values are unknown until the deployment resolves them; do not derive an expiry from unresolved text.
- The last-update time only reflects values within the maximum history display period (24 hours by default), so a missing value there does not show the item never collected.

## Retrieve history

Read samples for item IDs, one value type per request.

- The history type must match the item's value type: float, character, log, unsigned, text, or binary. Query items of different types in separate requests. The default type is unsigned and is wrong for other items.
- Time bounds are inclusive. Results carry item ID, time, and value. A sort field, sort order, and limit can be set; a limited result is bounded, so say so.
- Success: a `result` array. Empty results can reflect selection or retention, not zero usage.

## Retrieve trends

Read trend aggregates for numeric items over the interval. Each row has a time, a sample count, and minimum, average, and maximum values. Report them as aggregates, not raw measurements. A limit can be set; this method documents no sort parameter.

## Handle errors

- A JSON-RPC error object (code, message, data) is a failure even on HTTP 200. Invalid parameters need correction, not reinterpretation as no data.
- Authentication or permission errors leave the observations unavailable.
- Rate limits and quotas: not documented. On an HTTP 429 from a fronting proxy, back off and honor any Retry-After header.

## Patterns

- Match response `id` to the request `id`.

## Known limitations

- JSON-typed history is not covered: the history page mentions a JSON type in a search note but does not list it among selectable types (unresolved inconsistency in the vendor docs).
- Retention settings do not guarantee that every expected sample exists.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover items | Resolve item IDs, types, units, retention | Read |
| Retrieve history | Read raw samples for one value type | Read |
| Retrieve trends | Read trend aggregate rows | Read |

## Verification checklist

- Returned item IDs match the requested host and items; the response id matches the request id.
- History type matches each item's value type; trend rows are labelled aggregates.
- Time bounds, limits, units, unresolved retention, and any API error are in the report.
