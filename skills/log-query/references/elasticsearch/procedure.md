# Elasticsearch: Bounded Log Search and Hit Count

Sources: Elasticsearch REST API reference, Search and Get mapping operations (rolling reference), retrieved 2026-10-26.

## Common Sequences

- **Retrieve events:** Read mapping → Run search → Qualify response.
- **Count matches:** Read mapping → Run search with full hit counting and no documents returned → Qualify response.

## Read mapping

Retrieve the field definitions of the target index, data stream, or alias so the query names real fields. Needs the index-metadata privilege.
- A named index that does not exist is an error by default. A wildcard that matches nothing returns an empty result by default. Report the two cases differently.

## Run search

Send a query over the target with the caller's time restriction. Needs the read privilege on the target. Only ten documents come back unless a size is requested, and the from-plus-size window is capped by the index's result-window setting (10,000 by default). A short-form query-string parameter, if used, overrides a query in the request body.
- Success: a hit list, a total with a relation of equal or at-least, a timed-out flag, and shard counts.
- A timeout or shard failures can return partial results: report them.

## Qualify response

Check the timed-out flag, the failed-shard count and failure details, the early-termination flag when present, and the total's relation. The total is exact only up to 10,000 by default; request full counting for an exact count (slower), or disabling counting leaves the total unknown. Failure entries can be fewer than the failed-shard count because duplicate failures are merged.

## Patterns

- Hit total and returned documents answer different questions; report both.
- Reading past the result window needs the documented sorted-cursor approach with a point in time. Not covered here: consult the platform's pagination guidance and do not invent a page cursor.
- Not documented: rate limits for this endpoint. On HTTP 429, back off and honor any `Retry-After` header.

## Known limitations

No index creation, mapping change, or ES|QL. A sample is not an exhaustive export.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read mapping | Retrieve field definitions | REST API |
| Run search | Retrieve matches and totals | REST API |

## Verification checklist

- [ ] Target, query fields, and interval match the mapping and the request.
- [ ] Total relation, timeout, and shard failures were checked.
- [ ] A bounded sample is not described as complete.
