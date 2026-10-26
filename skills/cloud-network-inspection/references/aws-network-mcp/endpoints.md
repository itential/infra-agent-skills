# AWS Network MCP Server: Tool Bindings

Sources: AWS Labs MCP documentation, "AWS Network MCP Server" reference page and the server's README in the awslabs/mcp repository (retrieved 2026-10-26).

The server is an MCP server run locally on the same host as the MCP client. Each operation in `procedure.md` resolves to one of the tools below by name. If the tool is not available in the connected server, report the operation as unsupported rather than substituting a call.

Parameters: Not documented: per-tool input parameters. Read each tool's input schema from the connected server before calling it. Documented only generally: a `profile_name` input selects an AWS CLI profile for cross-account access, and some tools take separate `tgw_account_profile_name` and `cloudwan_account_profile_name` inputs (which tools is not documented). The server also honors the `AWS_PROFILE` and `AWS_REGION` environment variables.

Response and error formats: Not documented. Preserve whatever status, message, and resource identity a tool returns.

| Operation (procedure heading) | MCP tool | Reads |
|---|---|---|
| Read path methodology | `get_path_trace_methodology` | Troubleshooting method for a path |
| Locate endpoints | `find_ip_address` | ENI for an IP, searched across regions |
| Locate endpoints | `get_eni_details` | ENI configuration, security groups, network ACLs, routing |
| Read VPC and ENI | `list_vpcs` | VPCs in a region |
| Read VPC and ENI | `get_vpc_network_details` | VPC network configuration |
| Read traffic evidence | `get_vpc_flow_logs` | VPC flow logs from CloudWatch Logs, with filtering |
| Read transit and hybrid network | `list_transit_gateways` | Transit Gateways in a region |
| Read transit and hybrid network | `get_tgw_details` | Transit Gateway configuration and operational detail |
| Read transit and hybrid network | `get_tgw_routes` | Routes of one route table, with filtering |
| Read transit and hybrid network | `get_all_tgw_routes` | All route tables and routes |
| Read transit and hybrid network | `list_tgw_peerings` | Transit Gateway peerings |
| Read transit and hybrid network | `detect_tgw_inspection` | AWS Network Firewall and third-party firewalls attached to a Transit Gateway |
| Read traffic evidence | `get_tgw_flow_logs` | Transit Gateway flow logs from CloudWatch Logs |
| Read transit and hybrid network | `list_core_networks` | Cloud WAN core networks in a region |
| Read transit and hybrid network | `get_cloudwan_details` | Core network configuration and operational state |
| Read transit and hybrid network | `get_cloudwan_attachment_details` | Attachments by type |
| Read transit and hybrid network | `get_cloudwan_routes` | Routes for one segment and region |
| Read transit and hybrid network | `get_all_cloudwan_routes` | Routing tables across segments and regions |
| Read transit and hybrid network | `list_cloudwan_peerings` | Transit Gateway peerings of a core network |
| Read transit and hybrid network | `get_cloudwan_peering_details` | Peering detail from both sides |
| Read transit and hybrid network | `detect_cloudwan_inspection` | Network Function Groups that perform inspection |
| Read traffic evidence | `get_cloudwan_logs` | Cloud WAN topology and routing change events |
| Simulate route change | `simulate_cloud_wan_route_change` | Modeled effect of a change, one region |
| Read transit and hybrid network | `list_vpn_connections` | Site-to-Site VPN connections in a region |
| Read firewall configuration | `list_network_firewalls` | AWS Network Firewalls in a region |
| Read firewall configuration | `get_firewall_rules` | Stateless and stateful rules |
| Read traffic evidence | `get_network_firewall_flow_logs` | Firewall flow logs from CloudWatch Logs |

Permissions the documentation lists for the server's role: EC2 Describe calls for network interfaces, security groups, ACLs, route tables, subnets, VPCs, internet and NAT gateways, VPC endpoints, Transit Gateway objects, VPN connections, flow logs, and regions; Network Manager Get and List calls for core networks, policies, routes, attachments, and Transit Gateway registrations and associations; Network Firewall Describe and List calls; load balancer Describe; CloudWatch Logs StartQuery and GetQueryResults; and STS GetCallerIdentity. None of the listed actions creates or modifies a network resource.
