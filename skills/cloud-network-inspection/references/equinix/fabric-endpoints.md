# Equinix Fabric read-tool bindings

Source: [Fabric Tools](https://docs.equinix.com/equinix-api/mcp-servers/fabric-mcp-server/), retrieved 2026-10-09. OAuth client endpoint: `https://mcp.equinix.com/fabric`. Exact arguments, UUID fields, filter operators and continuation schemas come from the live `tools/list` contract and linked API reference.

| Operation family | Published read tools |
|---|---|
| Connections / ports / routers / networks / IP blocks | `search_connections`, `search_ports`, `get_vlan_port`, `search_routers`, `search_networks`, `search_ip_blocks` |
| Metro / project / packages / prices | `list_metros`, `get_metro`, `list_project`, `list_router_packages`, `search_prices` |
| Service profiles | `search_service_profiles`, `get_service_profile`, `list_service_profile_metros` |
| Routes / protocols / prior actions | `search_routes`, `list_routing_protocols`, `list_routing_protocol_actions`, `search_router_commands` |
| Route filters | `search_route_filters`, `list_route_filters_for_connection`, `list_route_filter_connections`, `search_route_filter_attachments_for_fcr` |
| Filter rules and history | `list_route_filter_rules`, `get_route_filter_rule`, `get_route_filter_changes`, `list_route_filter_change`, `list_route_filter_rule_changes`, `get_route_filter_rule_change` |
| Route aggregations | `search_route_aggregations`, `get_route_aggregation`, `list_route_aggregations_for_connection`, `list_route_aggregation_connections`, `search_route_aggregation_attachments_for_fcr` |
| Aggregation rules and history | `list_route_aggregation_rules`, `get_route_aggregation_rule`, `list_route_aggregation_changes`, `get_route_aggregation_change`, `list_route_aggregation_rule_changes`, `get_route_aggregation_rule_change` |
| Streams | `list_streams`, `get_stream`, `get_stream_network_edge_device` |
| Stream assets / subscriptions / alerts | `search_attached_assets`, `list_stream_attached_assets_by_type`, `get_stream_attached_asset`, `list_stream_subscriptions`, `get_stream_subscription`, `list_stream_alert_rules`, `get_stream_alert_rule` |

The current page contains additional similarly named project/change-history entries without a stated permission level. This extraction uses the explicitly Viewer-labelled entries above; the missing contract is not inferred. `refresh_routes` is excluded despite Viewer classification because its description creates a route action. Token reads, Application Connect and every mutating tool are outside this procedure. No stable universal MCP error schema is published on the tool catalogue page.
