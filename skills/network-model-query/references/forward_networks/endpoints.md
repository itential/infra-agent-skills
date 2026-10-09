# Forward MCP 3.0.0 bindings

These are publisher MCP inputs, not REST parameters. The authenticated server already has its Forward API connection configured.

| Operation | MCP binding | Inputs/evidence |
|---|---|---|
| Networks | `list_networks` | `limit` (default 25, capped 100), `offset`, `all_results` (false here); native text and network records |
| Snapshots | `list_snapshots` | `network_id`, same list bounds; snapshot `id`, `createdAt`, `processedAt`, `state` where supplied |
| Latest snapshot | `get_latest_snapshot` | `network_id`; snapshot metadata |
| Devices | `list_devices` | `network_id`, `snapshot_id`, `limit`, `offset`; records plus total count |
| Query library | `list_nqe_queries` | Optional `directory`; use returned `queryId` |
| Query by ID | `run_nqe_query_by_id` | `network_id`, `query_id`, `snapshot_id`, `parameters`, `options.limit`, `options.offset`; API evidence has `snapshotId`, `items`, `totalNumItems` |
| Batch query | `run_nqe_query_by_id` | Same identifiers with `all_results=true`; unfiltered/unsorted only in this procedure; response is a count/preview and optional local entity ID |
| Modeled path | `search_paths` | `network_id`, `snapshot_id`, `dst_ip`, either `from` or `src_ip`; optional numeric `ip_proto`, string `src_port`/`dst_port`, `intent`, `max_candidates`, `max_results`, `max_return_path_results`, `max_seconds`, `include_network_functions` |

Path intents documented by the tool schema are `PREFER_DELIVERED`, `PREFER_VIOLATIONS`, `VIOLATIONS_ONLY`. The single-path MCP handler converts its request to the bulk API representation. API result evidence includes `info.paths`, `returnPathInfo`, `timedOut`, `unrecognizedValues`, and total-hit metadata; each path retains `forwardingOutcome` and `securityOutcome`.

## Conditions and implementation boundaries

- The NQE handler returns a warning without executing when `all_results` is false and `options.limit` is absent, zero or greater than 1000. A limit from 1 through 1000 avoids that documented guard; it does not guarantee a complete dataset.
- Error matching in the inspected handler includes `Invalid module path`, `NQE_RUNTIME_ERROR`, and `result exceeds maximum length`. The latter can trigger batch mode.
- Path validation requires `dst_ip` to parse as an IP address or CIDR; device names are not accepted there. A source must be supplied with `from` or `src_ip`.
- The inspected cache key includes query ID, query parameters, network and snapshot, but excludes `options`. Cached single-page results cannot establish correct pagination across differing offsets.
- `all_results` submits limit/offset but omits filter/sort options. Its returned preview normally contains up to five rows, not the complete fetched data.

Sources: publisher [tool schemas](https://github.com/forwardnetworks/forward-mcp/blob/f9f6f9e8f38b45c804d845ead949a43f7d2dc566/internal/service/tools.go), [handlers](https://github.com/forwardnetworks/forward-mcp/blob/f9f6f9e8f38b45c804d845ead949a43f7d2dc566/internal/service/mcp_service.go), [client](https://github.com/forwardnetworks/forward-mcp/blob/f9f6f9e8f38b45c804d845ead949a43f7d2dc566/internal/forward/client.go), retrieved 2026-10-09.
