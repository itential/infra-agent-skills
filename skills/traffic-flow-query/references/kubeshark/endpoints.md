# Kubeshark L4 flow query: bindings

Paths are relative to the authenticated Hub API surface supplied by the deployment; reverse-proxy prefixes must follow that deployment's configuration.

| Operation | Binding | Parameters/result |
|---|---|---|
| Read flows | `GET /mcp/flows` | `format=compact|full|raw`, `aggregate=pod|namespace|node|service`, `l4proto=tcp|udp`, `ip`, `ns`, `pod`, `svc`, `limit` |
| Summary | `GET /mcp/flows/summary` | No required query parameters |

Flow response: `flows`, `total`, `truncated`; peer fields `client`, `server`; `client_stats`, `server_stats`, `totals`. Handshake fields `tcp_handshake_p50_us`, `tcp_handshake_p90_us`, `tcp_handshake_p99_us`. A gated Hub requires `mcp:use`; 403 means the capability is absent. In direct CLI URL mode, a 401 from an expired token requires a new token and restarted client. Secrets are never literal example values.

## Sources

- [Kubeshark L4 tools](https://docs.kubeshark.com/en/mcp/l4_tools). Retrieved 2026-10-09.
- [Kubeshark MCP installation](https://docs.kubeshark.com/en/mcp/cli). Retrieved 2026-10-09.
- [Kubeshark MCP access controls](https://docs.kubeshark.com/en/mcp). Retrieved 2026-10-09.
