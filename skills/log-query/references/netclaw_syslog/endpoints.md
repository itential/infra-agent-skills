# NetClaw syslog stored-record queries: bindings

Publisher MCP tool bindings at the pinned commit:

| Tool | Parameters |
|---|---|
| `syslog_get_status` | No arguments |
| `syslog_query` | `start_time?`, `end_time?`, `severity_min?`, `severity_max?`, `facility?`, `hostname?`, `source_ip?`, `message_contains?`, `limit?`, `offset?` |
| `syslog_get_message` | `message_id` |
| `syslog_get_severity_counts` | `start_time?`, `end_time?` |

List result fields: `total`, `returned`, `messages`. `limit` defaults to 100, schema maximum 1000; `offset` defaults to 0. Detail ID argument is `message_id`. Error text includes `Receiver not started`, missing-ID messages, not-found messages and `Error:`. Time filters `start_time`/`end_time` are listed for recognition only and are blocked on this version due to the aware/naive timestamp defect.
The implementation reverses the intuitive numeric severity-bound names: its minimum parameter acts as an upper numeric bound and its maximum as a lower bound. These filters remain blocked until the installed contract is corrected/verified; the read may instead return bounded unfiltered rows with their actual severity. Counts retain native severity labels.

## Sources

- [NetClaw publisher receiver implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/syslog-mcp/syslog_mcp_server.py). Retrieved 2026-10-09.
- [Publisher receiver guide](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/syslog-mcp/README.md). Retrieved 2026-10-09.
- [Publisher store behavior](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/syslog-mcp/message_store.py). Retrieved 2026-10-09.
- [Publisher record schema](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/syslog-mcp/models.py). Retrieved 2026-10-09.
