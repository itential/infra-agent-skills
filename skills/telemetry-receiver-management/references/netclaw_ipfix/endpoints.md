# NetClaw ipfix receiver lifecycle: bindings

Publisher MCP tool bindings at the pinned commit:

| Tool | Parameters |
|---|---|
| `ipfix_start_receiver` | `port?`, `bind_address?` |
| `ipfix_stop_receiver` | No arguments |
| `ipfix_get_status` | No arguments |

Responses are MCP text content. `Error:` and `Unknown tool:` are failure prefixes; already-running/already-stopped messages are distinct outcomes. Status is JSON encoded inside text content. No assumption that MCP `isError` alone detects failure is valid.


## Sources

- [NetClaw publisher receiver implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/ipfix_mcp_server.py). Retrieved 2026-10-09.
- [Publisher receiver guide](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/README.md). Retrieved 2026-10-09.
- [Publisher store behavior](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/message_store.py). Retrieved 2026-10-09.
- [Publisher record schema](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/models.py). Retrieved 2026-10-09.
- [Publisher flow parser/cache](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/flow_parser.py). Retrieved 2026-10-09.
