# NetClaw ipfix stored-record queries: bindings

Publisher MCP tool bindings at the pinned commit:

| Tool | Parameters |
|---|---|
| `ipfix_get_status` | No arguments |
| `ipfix_query_flows` | `start_time?`, `end_time?`, `exporter_ip?`, `src_ip?`, `dst_ip?`, `src_port?`, `dst_port?`, `protocol?`, `version?`, `min_bytes?`, `limit?`, `offset?` |
| `ipfix_get_flow` | `flow_id` |
| `ipfix_top_talkers` | `start_time?`, `end_time?`, `limit?` |
| `ipfix_get_templates` | No arguments |

List result fields: `total`, `returned`, `flows`. `limit` defaults to 100, schema maximum 1000; `offset` defaults to 0. Detail ID argument is `flow_id`. Error text includes `Receiver not started`, missing-ID messages, not-found messages and `Error:`. Time filters `start_time`/`end_time` are listed for recognition only and are blocked on this version due to the aware/naive timestamp defect.
Native top-talker aggregation sums observed bytes/packets per source/destination and protocol; missing counters are treated as zero by that summary implementation, so zero is not proof of a measured zero. Template inventory shows cached definitions, not guaranteed freshness. Zero-valued port/protocol filters are ignored by current truthiness checks and are unsupported for exact filtering.

## Sources

- [NetClaw publisher receiver implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/ipfix_mcp_server.py). Retrieved 2026-10-09.
- [Publisher receiver guide](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/README.md). Retrieved 2026-10-09.
- [Publisher store behavior](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/message_store.py). Retrieved 2026-10-09.
- [Publisher record schema](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/models.py). Retrieved 2026-10-09.
- [Publisher flow parser/cache](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/ipfix-mcp/flow_parser.py). Retrieved 2026-10-09.
