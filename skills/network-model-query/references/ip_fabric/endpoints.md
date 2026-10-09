# IP Fabric MCP bindings

Source: [IP Fabric MCP Server](https://docs.ipfabric.io/latest/IP_Fabric_Settings/integration/mcp/), retrieved 2026-10-09. Remote MCP is `https://<ipfabric-host>/mcp`, authenticated with `Authorization: Bearer <token>` through the configured client.

| Operation | Tool | Inputs |
|---|---|---|
| Assess health | `ipf_network_health_assess` | Deployment tool schema supplies any filters; setup guide does not publish a full input schema |
| Unicast path | `ipf_pathlookup_unicast` | Required `src`, `dst`, `snapshotId`, `groupBy`; optional `protocol` (`icmp` default, `tcp`, `udp`), `l4Options`, `vrf`, `includeGraphLayout=false` |
| Host gateway path | `ipf_pathlookup_host-to-gateway` | Required `src`, `snapshotId`, `groupBy`; optional `vrf`, `includeGraphLayout=false` |
| Multicast path | `ipf_pathlookup_multicast` | Required `src`, `group`, `receiver` (comma-separated IPs), `snapshotId`, `groupBy`; optional `includeGraphLayout=false` |
| Unicast PNG | `ipf_png_pathlookup_unicast` | Unicast parameters except `includeGraphLayout` |
| Gateway PNG | `ipf_png_pathlookup_host-to-gateway` | Gateway parameters except `includeGraphLayout` |
| Multicast PNG | `ipf_png_pathlookup_multicast` | Multicast parameters except `includeGraphLayout` |
| Discover query | `ipf_api_endpoint_search` | Natural-language lookup; exact argument name from `tools/list` |
| Inspect contract | `ipf_api_endpoint_details` | Selected endpoint; exact argument name from `tools/list` |
| Invoke read | `api_invoke` | Method/path/parameters from inspected endpoint and deployed tool schema |

`groupBy` accepts `siteName`, `routingDomain`, or `stpDomain`. The guide documents `$last` for the latest snapshot and `Snapshot not found` for an unavailable snapshot. HTTP `401 Unauthorized` is an authentication/permission failure; `404 Not Found` can indicate an incorrect MCP location or a disabled server. Other operation-specific errors are resolved through endpoint details, not assumed from the setup guide.
