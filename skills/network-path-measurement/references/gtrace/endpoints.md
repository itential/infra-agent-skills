# gtrace local path measurement: bindings

Publisher gtrace MCP:

| Operation | Tool and arguments |
|---|---|
| Trace | `traceroute(target, protocol?, port?, max_hops?, timeout?, packets?, ipv4?, ipv6?, detect_nat?, ecmp_flows?, discover_mtu?, probe_size?, decode?, format?, view?)` |
| Repeated trace | `mtr(target, protocol?, port?, max_hops?, timeout?, cycles?, interval?, ecmp_flows?, decode?, format?)` |

Protocols: `icmp`, `udp`, `tcp`. `format` is `text` or `json`; JSON is returned in MCP `structuredContent`. Text `view` is `table` or `graph` and is ignored for JSON.

Error prefixes from the publisher handlers: `traceroute requires root privileges`, `MTR requires root privileges`, `invalid timeout`, `invalid interval`, `invalid configuration`, `failed to resolve target`, `failed to create tracer`, `traceroute failed`, `MTR failed`. These identify the failed operation; no retry duration is implied.

## Sources

- [gtrace publisher README](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/README.md). Retrieved 2026-10-09.
- [Tool schemas](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/internal/mcp/server.go). Retrieved 2026-10-09.
- [Tool error handling](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/internal/mcp/handlers.go). Retrieved 2026-10-09.
