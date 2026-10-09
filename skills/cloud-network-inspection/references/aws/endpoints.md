# AWS Network MCP bindings

Sources: [publisher reference](https://awslabs.github.io/mcp/servers/aws-network-mcp-server), [README](https://github.com/awslabs/mcp/blob/main/src/aws-network-mcp-server/README.md), retrieved 2026-10-09.

The approved local `awslabs.aws-network-mcp-server` uses MCP over stdio. `tools/list` supplies each current `inputSchema`; `tools/call` invokes the selected tool. Input schemas not published in the overview are explicitly version-dependent; no guessed REST route or parameter is substituted. `profile_name` selects an AWS profile where supported; some cross-account tools expose `tgw_account_profile_name` and `cloudwan_account_profile_name`.

| Capability | Exact tools |
|---|---|
| Methodology and endpoint identity | `get_path_trace_methodology`, `find_ip_address`, `get_eni_details` |
| VPC configuration/traffic | `list_vpcs`, `get_vpc_network_details`, `get_vpc_flow_logs` |
| Transit Gateway configuration/routes | `list_transit_gateways`, `get_tgw_details`, `get_tgw_routes`, `get_all_tgw_routes` |
| Transit Gateway peerings/inspection/traffic | `list_tgw_peerings`, `detect_tgw_inspection`, `get_tgw_flow_logs` |
| Cloud WAN configuration | `list_core_networks`, `get_cloudwan_details`, `get_cloudwan_attachment_details` |
| Cloud WAN routes | `get_cloudwan_routes`, `get_all_cloudwan_routes` |
| Cloud WAN peerings/inspection/events | `list_cloudwan_peerings`, `get_cloudwan_peering_details`, `detect_cloudwan_inspection`, `get_cloudwan_logs` |
| Cloud WAN simulation | `simulate_cloud_wan_route_change` |
| VPN | `list_vpn_connections` |
| Network Firewall | `list_network_firewalls`, `get_firewall_rules`, `get_network_firewall_flow_logs` |

An MCP error or failed AWS operation is an error result; no common wrapper success/error schema is promised by the cited overview. The binding therefore preserves returned status, diagnostic and resource identity. IAM requirements are in the publisher reference; the deployment's authorized policy must cover the requested operations.
