# gtrace IP metadata lookup: bindings

Publisher MCP operations: `asn_lookup(ip, format?)`, `geo_lookup(ip, format?)`, `reverse_dns(ip, format?)`. `format=json` returns structured content; text is the default. Native error prefixes: `invalid IP address`, `ASN lookup failed`, `geo lookup failed`, `reverse DNS lookup failed`. Each failed lookup remains failed; no guessed replacement value is supplied.

## Sources

- [gtrace lookup tool schemas](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/internal/mcp/server.go). Retrieved 2026-10-09.
- [gtrace lookup implementations](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/internal/mcp/handlers.go). Retrieved 2026-10-09.
