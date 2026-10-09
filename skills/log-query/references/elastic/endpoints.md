# Elasticsearch read bindings

Sources: [mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-mapping),
[search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html),
and [count/partial semantics](https://www.elastic.co/docs/solutions/search/the-search-api),
retrieved 2026-10-09. An existing authenticated API client and selected index are prerequisites.

| Operation | Method and path | Inputs/results |
|---|---|---|
| Read mapping | `GET /{index}/_mapping` | Index-keyed mappings; requires `view_index_metadata` |
| Search selected index | `POST /{index}/_search` | JSON `query`, optional `size`, `_source`, `sort`, `timeout`, `track_total_hits`; requires `read` |
| Count selected matches | `POST /{index}/_search` | Same selection, `size: 0`, `track_total_hits: true`; no early-termination request |

Results: `hits.hits`, `hits.total.value`, `hits.total.relation` (`eq` or `gte`), `timed_out`,
`terminated_early` when present, `_shards.failed`, and `_shards.failures`.
By default, totals are exact only up to 10,000 matches. `track_total_hits: false` omits the total.
The JSON `query` and query-string `q` are not combined: when both exist, `q` takes precedence.

For mapping reads, `allow_no_indices` defaults to true and `ignore_unavailable` defaults to false.
No credentials, index names, or deployment origins are embedded in this binding.
