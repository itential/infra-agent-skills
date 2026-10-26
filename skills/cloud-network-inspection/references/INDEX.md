# Cloud Network Inspection: Platform Index

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| AWS | [aws-network-mcp/](aws-network-mcp/procedure.md) | VPC and ENI detail, Transit Gateway and Cloud WAN configuration and routes, peerings, inspection detection, Site-to-Site VPN list, Network Firewall rules, flow-log and Cloud WAN event queries, one-region Cloud WAN route-change simulation | Binds to the AWS Network MCP server by tool name; Not documented: per-tool input schemas, so read each tool's schema at runtime. AWS Network Firewall is also a vendor of `firewall-management` and is separate there (configuration management); only read access to its rules and flow logs is covered here. Flow-log tools need CloudWatch Logs destinations. Transit Gateway route tools need Network Manager registration. |
| Azure | [azure-cli/](azure-cli/procedure.md) | Subscription selection, VNets and peerings, NSGs, effective NIC rules and routes, ExpressRoute and VPN gateway reads, load balancer and Application Gateway backend health, firewall, route table, Network Watcher, private endpoint, and DNS record reads | Azure CLI only; commands are inline (no endpoints file). Azure Firewall commands come from a CLI extension. No scoring or compliance output. Azure DNS record reads are limited to listing record sets in a known zone; Azure DNS and Route 53 record management are in `dns-record-management`, and Azure Firewall policy authoring is out of scope. |

Both platforms are read-only in this skill. AWS and Azure are the only clouds covered.
