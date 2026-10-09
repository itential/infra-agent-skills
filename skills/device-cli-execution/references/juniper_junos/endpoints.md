# Junos MCP command bindings

Sources: [README](https://github.com/Juniper/junos-mcp-server) and [tool definitions](https://github.com/Juniper/junos-mcp-server/blob/main/jmcp.py), main retrieved 2026-10-09.

| Operation | Tool | Parameters |
|---|---|---|
| List mapped routers | `get_router_list` | None. |
| Refresh facts | `gather_device_facts` | `router_name`; optional `timeout` in seconds. |
| Execute command | `execute_junos_command` | `router_name`, `command`; optional `timeout`. |
| Execute on multiple routers | `execute_junos_command_batch` | `router_names[]`, `command`; optional per-router `timeout`. |
| Read configuration | `get_junos_config` | `router_name`. |
| Compare rollback | `junos_config_diff` | `router_name`, `version` (documented 1–49, default 1). |

The configuration reader runs `show configuration | display inheritance no-comments | display set | no-more`; historical comparison runs `show configuration | compare rollback <version>`.

MCP text content and annotations preserve results. The implementation detects error content and may mark `isError`; callers also inspect native CLI output. Exact mapped-router failure: `Router <name> not found in the device mapping.` Connection exceptions are returned with error text. Blocklist refusals remain refusals, never empty output.

The server supports stdio or authenticated streamable HTTP. Its default network authentication requires a nonempty token file; the documented loopback-only development override is not a production configuration. No credentials appear in task payload examples.
