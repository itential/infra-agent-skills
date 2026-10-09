# Topolograph IGP snapshot queries: bindings

Publisher Topolograph MCP v1.5.0, pinned below. An authenticated connection targets the operator-selected instance. Read-only mode is enabled by default and hides/rejects graph-upload and LSP mutations. Tool annotations alone are not an authorization boundary.

| Operation | Published arguments |
|---|---|
| `get_all_graphs` | `protocol: Optional[str]=None, area: Optional[str]=None, is_monitored: Optional[bool]=None, name: Optional[str]=None, latest_only: bool=False, page: int=1, per_page: int=50` |
| `get_graph_by_time` | `graph_time: str` |
| `get_graph_status` | `graph_time: str` |
| `get_network_by_graph_time` | `graph_time: str, network_w_digit_mask: Optional[str]=None, ip_address: Optional[str]=None, node_id: Optional[str]=None` |
| `get_nodes` | `graph_time: str, protocol: Optional[str]=None, watcher: Optional[bool]=None, area: Optional[str]=None, abr: Optional[bool]=None, asbr: Optional[bool]=None, overload: Optional[bool]=None, attached: Optional[bool]=None, maxmetric: Optional[bool]=None, vni: Optional[int]=None, vrf: Optional[str]=None, rt: Optional[str]=None, page: int=1, per_page: int=50` |
| `get_edges` | `graph_time: str, src_node: Optional[str]=None, dst_node: Optional[str]=None, protocol: Optional[str]=None, watcher: Optional[bool]=None, area: Optional[str]=None, edge_query_params: Optional[dict]=None, include: Optional[List[str]]=None, page: int=1, per_page: int=50, is_te_link: Optional[bool]=None` |
| `get_lsps` | `graph_time: str, lsp_name: Optional[str]=None, status: Optional[str]=None, via_node: Optional[str]=None, via_edge: Optional[str]=None, via_edge_key: Optional[str]=None, include_path: bool=False` |
| `get_shortest_path` | `graph_time: str, src_node: str, dst_node: Union[str, List[str]], with_lsps: bool=False` |
| `get_cspf_path` | `graph_time: str, node_a: str, node_b: str, bandwidth: Optional[str]=None, metric_type: str='igp', admin_exclude_any: Optional[List[str]]=None, admin_include_any: Optional[List[str]]=None, admin_include_all: Optional[List[str]]=None, srlg_exclude: Optional[List[int]]=None, setup_priority: int=7, level: Optional[int]=None` |
| `get_network_events` | `graph_time: str, start_time: Optional[str]=None, end_time: Optional[str]=None, last_minutes: Optional[int]=None` |
| `get_adjacency_events` | `graph_time: str, start_time: Optional[str]=None, end_time: Optional[str]=None, last_minutes: Optional[int]=None` |
| `get_events_timeline` | `graph_time: str, start_time: Optional[str]=None, end_time: Optional[str]=None, last_minutes: Optional[int]=None, page: int=1, per_page: int=20` |
| `get_edge_failure_reaction` | `graph_time: str, failed_edges: list[list[str]]` |

Pagination is 1-based where exposed; the response supplies pagination metadata. HTTP failures propagate; graph-aware handlers preserve backend `detail`/`error`, `code`, `action` and snapshot identity. No undocumented automatic retry budget is assumed.

LSP failure codes: `disconnected`, `constraints_unsatisfiable`, `ero_strict_hop_unreachable`, `endpoint_not_found`. CSPF level errors: `isis_level_calculation_unavailable`, `isis_level_unavailable_for_yaml_diagram`. An empty CSPF path with null cost is a valid no-placement result; 404 instead identifies a missing graph.


## Sources

- [Publisher MCP implementation](https://github.com/Topolograph/topolograph-mcp-server/blob/2a7c7e341ac14026d925aed900fdf110f5191246/mcp-server.py). Retrieved 2026-10-09.
- [Publisher compatibility and mode documentation](https://github.com/Topolograph/topolograph-mcp-server/blob/2a7c7e341ac14026d925aed900fdf110f5191246/README.md). Retrieved 2026-10-09.
