# NetClaw protocol MCP bindings

Pinned publisher runtime: commit `95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692`.

| Operation | MCP call | Result evidence |
|---|---|---|
| BGP peers | `bgp_get_peers()` | `peers`, `count`, `source`; source is `mesh-daemon` or `in-process speaker` |
| BGP routes | `bgp_get_rib(prefix=<optional-CIDR>)` | `routes`, `count`, `source` |
| Local summary | `protocol_summary()` | `router_id`, `local_as`, `lab_mode`, `bgp`, `ospf`, `gre`; subobjects may contain errors |
| GRE lines | `gre_tunnel_status()` | `tunnels`, `addresses`, `count`, or `error` |

The BGP daemon read adapter consults its configured `BGP_DAEMON_API`, using `GET /peers`, `GET /status`, and `GET /rib`. Its default is local loopback `http://127.0.0.1:8179`; this reference does not reconfigure it or expose it remotely. The wrapper suppresses daemon transport/non-200 failures and may fall back to an in-process read.

Native BGP configuration error: `BGP not configured. Set NETCLAW_BGP_PEERS, or start the mesh daemon.` This error is reported; the setup suggestions embedded in that vendor error are outside the procedure's read scope. OSPF is not offered because its initializer and connector are incompatible at this revision.

The GRE implementation runs `ip tunnel show` and `ip -br addr show`, filters text for `gre`, and applies a five-second subprocess timeout. It does not check subprocess exit codes. GCF serialization uses session/delta state; when it fails, JSON is the fallback. The literal wire format cannot be assumed to be JSON on every successful call.

Sources: [server](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/protocol-mcp/server.py), [BGP connector](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/protocol-mcp/connectors/bgp_connector.py), [OSPF connector](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/protocol-mcp/connectors/ospf_connector.py), [OSPF constructor](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/protocol-mcp/ospfv3/speaker.py), retrieved 2026-10-09.
