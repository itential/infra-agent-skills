# Infrahub MCP bindings

Source: [MCP methods](https://docs.infrahub.app/mcp/references/methods), retrieved 2026-10-09. An authenticated configured MCP connection supplies transport and instance location. Exact deployment schemas remain available through `tools/list`.

| Operation | Tool | Documented inputs and result contract |
|---|---|---|
| Discover schema | `get_schema` | Optional `kind`, `branch`, `expand`; omitted kind returns catalog |
| Inspect session | `get_session_info` | No arguments; current session branch and instance address |
| Read objects | `get_nodes` | Required `kind`; optional `branch`, `filters`, `partial_match=false`, `include_attributes=false`, `limit=50` (minimum -1), `offset=0`; -1 requests all |
| Search names | `search_nodes` | Required `query` (nonempty), `kind`; optional `branch`, `limit=10` (1–100); name substring only |
| GraphQL read | `query_graphql` | Required `query`; optional `branch`; mutation AST rejected |
| Scalar object change | `node_upsert` | Required `kind`, `data`; optional `id` or `hfid` selects update; neither selects create; scalar attributes only |
| Delete object | `node_delete` | Required `kind` and either `id` or `hfid` |
| Relationship mutation | `mutate_graphql` | Required `query`; session branch only; no branch override |
| Propose change | `propose_changes` | Required `title`; optional `description`, `destination_branch`; creates `CoreProposedChange` |
| Reset session | `reset_session_branch` | Optional `branch`; omission clears cached selection |

The typed query response contains `nodes`, `count`, `total_count`, `has_more`, `offset`, `limit`; `has_more=null` means count failed. `hfid` is an array of human-friendly identifier segments. The mutation input is `query`, not the older wrapper's `mutation`; proposal title is required. No complete stable MCP error code table is stated in the cited reference.
