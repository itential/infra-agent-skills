# AWS Network MCP Server: Tool Bindings

Sources: AWS Labs MCP documentation, "AWS Network MCP Server" reference page and the server's README in the awslabs/mcp repository (retrieved 2026-10-26).

The server is an MCP server run locally on the same host as the MCP client. Each operation in `procedure.md` resolves to one of the tools below by name. If the tool is not available in the connected server, report the operation as unsupported rather than substituting a call.

Parameters: Not documented: per-tool input parameters. Read each tool's input schema from the connected server before calling it. Documented only generally: a `profile_name` input selects an AWS CLI profile for cross-account access, and some tools take separate `tgw_account_profile_name` and `cloudwan_account_profile_name` inputs (which tools is not documented). The server also honors the `AWS_PROFILE` and `AWS_REGION` environment variables.

Response and error formats: Not documented. Preserve whatever status, message, and resource identity a tool returns.

| Operation (procedure heading) | MCP tool |
|---|---|
| Read path methodology | `get_path_trace_methodology` |
| Locate endpoints | `find_ip_address` |
| Locate endpoints | `get_eni_details` |
| Read VPC and ENI | `list_vpcs` |
| Read VPC and ENI | `get_vpc_network_details` |
| Read traffic evidence | `get_vpc_flow_logs` |
| Read transit and hybrid network | `list_transit_gateways` |
| Read transit and hybrid network | `get_tgw_details` |
| Read transit and hybrid network | `get_tgw_routes` |
| Read transit and hybrid network | `get_all_tgw_routes` |
| Read transit and hybrid network | `list_tgw_peerings` |
| Read transit and hybrid network | `detect_tgw_inspection` |
| Read traffic evidence | `get_tgw_flow_logs` |
| Read transit and hybrid network | `list_core_networks` |
| Read transit and hybrid network | `get_cloudwan_details` |
| Read transit and hybrid network | `get_cloudwan_attachment_details` |
| Read transit and hybrid network | `get_cloudwan_routes` |
| Read transit and hybrid network | `get_all_cloudwan_routes` |
| Read transit and hybrid network | `list_cloudwan_peerings` |
| Read transit and hybrid network | `get_cloudwan_peering_details` |
| Read transit and hybrid network | `detect_cloudwan_inspection` |
| Read traffic evidence | `get_cloudwan_logs` |
| Simulate route change | `simulate_cloud_wan_route_change` |
| Read transit and hybrid network | `list_vpn_connections` |
| Read firewall configuration | `list_network_firewalls` |
| Read firewall configuration | `get_firewall_rules` |
| Read traffic evidence | `get_network_firewall_flow_logs` |

Permissions the documentation lists for the server's role: EC2 Describe calls for network interfaces, security groups, ACLs, route tables, subnets, VPCs, internet and NAT gateways, VPC endpoints, Transit Gateway objects, VPN connections, flow logs, and regions; Network Manager Get and List calls for core networks, policies, routes, attachments, and Transit Gateway registrations and associations; Network Firewall Describe and List calls; load balancer Describe; CloudWatch Logs StartQuery and GetQueryResults; and STS GetCallerIdentity. None of the listed actions creates or modifies a network resource.
