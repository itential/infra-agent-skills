# Elasticsearch: Search Wiring

Sources: Elasticsearch REST API reference, Search and Get mapping operations (rolling reference), retrieved 2026-10-26.

Cluster address and credentials come from the existing client.

| Operation | Method and path | Notes |
|---|---|---|
| Read mapping | `GET /{index}/_mapping` | Needs `view_index_metadata`. `allow_no_indices` defaults true, `ignore_unavailable` defaults false, `expand_wildcards` defaults `open`. |
| Run search | `POST /{index}/_search` | Needs `read`. Body: `query`, `size` (default 10), `sort`, `_source`, `timeout`, `track_total_hits` (default 10000; `true` for exact; `false` omits). Query parameter `q` overrides a body query. |

Response fields: `hits.hits`, `hits.total.value`, `hits.total.relation` (`eq` or `gte`), `timed_out`, `terminated_early` (when set), `_shards.failed`, `_shards.failures`. For a count only, send `size` 0 with `track_total_hits` true.

Unverified: whether `Retry-After` accompanies a 429 response.
