# cloud-network-inspection: platform references

| Platform | Procedure | Scope | Notes |
|---|---|---|---|
| AWS Network MCP | [aws/procedure.md](aws/procedure.md) | VPC/ENI/TGW/Cloud WAN/VPN/firewall configuration; logs; route simulation | Multi-region IP lookup is supported; flow logs require CloudWatch destinations. |
| Azure | [azure/procedure.md](azure/procedure.md) | VNet, NIC effective policy/routes, NSG, hybrid routing, load-balancer configuration, Application Gateway health and supporting resources | Azure CLI; no CIS score |
| Equinix Fabric | [equinix/fabric.md](equinix/fabric.md) | Connections, ports, routers, networks/IP blocks, service catalogues, route/filter relationships and telemetry configuration | Read-only Fabric MCP |
| Equinix Network Edge | [equinix/network-edge.md](equinix/network-edge.md) | Virtual devices, account/project/metro/device-type catalogues and ACL/template associations | Read-only Network Edge MCP |
