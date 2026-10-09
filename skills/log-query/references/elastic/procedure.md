# Elasticsearch log search and count

Inspect an existing index mapping and retrieve scoped log matches with qualified counts.

Primary sources: [search semantics](https://www.elastic.co/docs/solutions/search/the-search-api),
[search operation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html),
[mapping retrieval](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-mapping),
rolling reference, retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Retrieve matching events: Read mapping → Search selected index → Qualify response.
- Count matching events: Read mapping → Count selected matches → Qualify response.

## Read mapping

Mapping retrieval identifies available fields and types for the selected index/data stream. It needs
index-metadata permission. An unavailable explicit index is an error by default; an allowed wildcard
with no matches can return an empty result. Those cases are reported separately.

## Search selected index

The query uses actual mapped fields and an explicit requested event/time selection. A successful
search returns matching hits. The default returns only ten documents; requested size bounds the
returned sample. No additional page is implied by a large total. Search authorization requires read
access to the selected index.

## Count selected matches

Exact count requests enable full hit tracking. Otherwise the native count relation distinguishes
an equality from a lower bound. Disabling tracking means the total is unknown. Early termination,
timeout, and shard failure still constrain a count, even when its relation says equality.

## Qualify response

The result retains timeout status, failed-shard details, and any early-termination flag. Query or
transport errors remain failed searches. A timeout can return partial results; it is not evidence
that the index contained only the rows returned. A failed shard is reported with its documented
reason. The number of failure objects can be smaller than the failed-shard count because duplicate
failures are consolidated.

## Patterns

Hit count and retrieved-hit count answer different questions. Exact counting has a performance
cost. The procedure preserves native count qualifiers that some third-party wrappers discard.

## Known limitations

This is bounded Query DSL retrieval/counting. It does not create indices, modify mappings, install
an MCP server, or provide an ES|QL catalogue. Deep pagination requires its separate documented
search-after/point-in-time sequence; it is not approximated by inventing a page cursor here.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read mapping | Retrieve selected index field definitions | Read |
| Search selected index | Retrieve matching stored events | Read |
| Count selected matches | Request fully tracked hit totals | Read |

## Verification checklist

- Selection and query fields match the mapping and requested interval.
- Count relation, timeout, early termination, and shard failures are all checked.
- A bounded event sample is not represented as an exhaustive export.
