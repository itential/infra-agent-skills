# Topolograph BGP model queries: bindings

Publisher Topolograph MCP v1.5.0, pinned below. An authenticated connection targets the operator-selected instance. Read-only mode is enabled by default and hides/rejects graph-upload and LSP mutations. Tool annotations alone are not an authorization boundary.

| Operation | Published arguments |
|---|---|
| `list_bgp_graphs` | `page: int=1, per_page: int=50` |
| `get_bgp_graph` | `bgp_graph_time: str` |
| `list_bgp_nodes` | `bgp_graph_time: str, role: Optional[str]=None, asn: Optional[str]=None, page: int=1, per_page: int=50` |
| `list_bgp_sessions` | `bgp_graph_time: str, igp_relation: Optional[str]=None, bgp_session_type: Optional[str]=None, page: int=1, per_page: int=50` |
| `search_bgp_routes` | `bgp_graph_time: str, router_id: Optional[str]=None, prefix: Optional[str]=None, vrf: Optional[str]=None, rd: Optional[str]=None, rt: Optional[str]=None, afi: Optional[int]=None, safi: Optional[int]=None, bmp_rib: Optional[str]=None, evidence: Optional[str]=None, as_path_contains: Optional[str]=None, origin: Optional[str]=None, local_pref: Optional[int]=None, med: Optional[int]=None, community: Optional[str]=None, large_community: Optional[str]=None, extended_community: Optional[str]=None, label: Optional[int]=None, originator_id: Optional[str]=None, peer_ip: Optional[str]=None, nexthop: Optional[str]=None, bmp_source: Optional[str]=None, table_filters: Optional[str]=None, ribs: Optional[str]=None, sort: Optional[str]=None, order: str='asc', page: int=1, per_page: int=50` |
| `get_bgp_node_route_summary` | `bgp_graph_time: str, router_id: str` |
| `get_bgp_route_state` | `bgp_graph_time: str, at: Optional[str]=None` |
| `compare_bgp_routes` | `bgp_graph_time: str, t0: str, t1: str, router_id: Optional[str]=None, t0_graph_time: Optional[str]=None` |
| `get_bgp_events_timeline` | `bgp_graph_time: str, start_time: Optional[str]=None, end_time: Optional[str]=None, last_minutes: Optional[int]=None, event_name: Optional[str]=None, event_status: Optional[str]=None, as_rows: bool=False` |
| `list_bgp_bindings` | `bgp_graph_time: str` |
| `get_bgp_binding` | `bgp_graph_time: str, graph_time: str` |
| `get_vrf_inventory` | `graph_time: str, router_id: Optional[str]=None, rd: Optional[str]=None` |
| `resolve_route` | `graph_time: str, start_node: str, destination: str, rt: Optional[str]=None, vrf: Optional[str]=None, rd: Optional[str]=None, evidence: str='loc_rib', with_lsps: bool=True, changed_edge_costs: Optional[dict]=None` |

Pagination is 1-based where exposed; the response supplies pagination metadata. HTTP failures propagate; graph-aware handlers preserve backend `detail`/`error`, `code`, `action` and snapshot identity. No undocumented automatic retry budget is assumed.

BGP route differences use `added`, `withdrawn`, `changed`; changed rows include `diff_prev`. `evidence` is `pre_policy`, `post_policy`, `loc_rib`, or `fib`. `bmp_source` and `table_filters` are ignored for router-scoped route searches. `list_vpn_routers` from NetClaw is absent at the cited publisher commit and is not bound here.


## Sources

- [Publisher MCP implementation](https://github.com/Topolograph/topolograph-mcp-server/blob/2a7c7e341ac14026d925aed900fdf110f5191246/mcp-server.py). Retrieved 2026-10-09.
- [Publisher compatibility and mode documentation](https://github.com/Topolograph/topolograph-mcp-server/blob/2a7c7e341ac14026d925aed900fdf110f5191246/README.md). Retrieved 2026-10-09.
