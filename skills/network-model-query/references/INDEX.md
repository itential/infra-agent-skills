# network-model-query: platform references

| Platform | Procedure | Scope | Notes |
|---|---|---|---|
| IP Fabric | [ip_fabric/procedure.md](ip_fabric/procedure.md) | Health assessment; unicast, gateway and multicast paths/diagrams; discovered read queries | Requires enabled MCP and an authorized token. |
| SuzieQ | [suzieq/procedure.md](suzieq/procedure.md) | Table reads, summaries, unique values, assertions and paths | Uses documented CLI against collected data. |
| Topolograph IGP | [topolograph/igp.md](topolograph/igp.md) | Stored graph inventory, paths, subnets and model analysis | Pinned API; no device mutation |
| Topolograph BGP | [topolograph/bgp.md](topolograph/bgp.md) | Stored BGP policy/path model queries | Requires compatible BGP-enabled release; missing VPN-router call excluded |
| Batfish | [batfish/procedure.md](batfish/procedure.md) | Existing snapshot initialization issues, forwarding/reachability, filter analysis and differential evidence | Pybatfish; no snapshot mutation in this query procedure |
| Forward Networks | [forward_networks/procedure.md](forward_networks/procedure.md) | Network/snapshot/device inventory, library NQE and modeled paths | MCP 3.0.0; cache and pagination limitations retained |
