# NetClaw snmptrap stored-record queries: bindings

Publisher MCP tool bindings at the pinned commit:

| Tool | Parameters |
|---|---|
| `snmptrap_get_status` | No arguments |
| `snmptrap_query` | `start_time?`, `end_time?`, `source_ip?`, `version?` enum ['v1', 'v2c', 'v3'], `trap_oid?`, `trap_oid_prefix?`, `limit?`, `offset?` |
| `snmptrap_get_trap` | `trap_id` |
| `snmptrap_get_counts` | `start_time?`, `end_time?` |

List result fields: `total`, `returned`, `traps`. `limit` defaults to 100, schema maximum 1000; `offset` defaults to 0. Detail ID argument is `trap_id`. Error text includes `Receiver not started`, missing-ID messages, not-found messages and `Error:`. Time filters `start_time`/`end_time` are listed for recognition only and are blocked on this version due to the aware/naive timestamp defect.
SNMPv1/v2c observations retain parse errors and numeric OIDs. Current SNMPv3 rows are placeholders, not authenticated decoded traps. Full-detail serialization can return the community string unmasked although list display masks it; details are sensitive and the community value is excluded from reports.

## Sources

- [NetClaw publisher receiver implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/snmptrap_mcp_server.py). Retrieved 2026-10-09.
- [Publisher receiver guide](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/README.md). Retrieved 2026-10-09.
- [Publisher store behavior](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/message_store.py). Retrieved 2026-10-09.
- [Publisher record schema](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/models.py). Retrieved 2026-10-09.
- [Publisher trap parser](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/snmptrap-mcp/trap_parser.py). Retrieved 2026-10-09.
