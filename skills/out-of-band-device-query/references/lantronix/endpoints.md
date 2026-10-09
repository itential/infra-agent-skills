# Lantronix Percepxion MCP bindings

These are tool inputs for the official publisher MCP at commit `533fdc981f0457043e948204db216e2b8a4076f5`. The configured client supplies the platform URL and credential-provider context.

Most operations return `{"ok":true,"data":...}` with optional `status_code`; errors return `ok:false`, `error`, optional `status_code` and `details`. Values in error details can be sensitive. Every scoped tool below accepts `organization_id` where its schema lists it; `tenant_id` is a deprecated alias. Use the exact live schema if the installed revision differs.

| Operation | MCP tool and verified inputs |
|---|---|
| Session | `login_with_env()` |
| Organizations | `list_organizations(search_query="*", limit=100, offset=0, sort="name", order="asc")` |
| Device inventory | `get_device_list(search_query="*", limit=25, offset=0, sort="device_name", order="asc", organization_id=...)` |
| Device detail | `get_device_details(device_id=..., serial_num=..., organization_id=...)`; at least one identity required |
| Organization devices | `get_devices_by_organization(organization_id=..., limit=100)`; no offset |
| Ports | `list_device_ports(device_id=..., limit=100, offset=0, organization_id=...)`; implementation uses device ID as a port search string |
| Full telemetry | `get_security_telemetry(device_id=..., selected=True, organization_id=...)` |
| Config | `get_device_config(device_id=..., organization_id=...)`; `selected` ignored |
| Firmware status | `get_device_firmware_status(device_id=..., organization_id=...)` |
| Firmware comparison | `firmware_compliance_report(expected_firmware_version=..., search_query="*", model_filter=..., limit=1000, organization_id=...)`; first page only |
| Catalogs | `list_firmware_content`, `list_smart_groups`: `search_query`, `limit`, `offset`, `organization_id`; `list_templates` also accepts optional `device_id` |
| Existing syslogs | `get_device_syslogs(device_id=..., limit=10)`; no organization argument |
| Access-log query | `query_device_access_log(device_id=..., log_level="info", limit=200, offset=0)`; no free-text `query` argument |
| Access-log download | `download_device_access_log(device_id=..., log_level="info")` |
| Detailed audit | `investigate_audit_logs(search_string=..., from_date=..., to_date=..., usernames=[...], limit=50, offset=0, sort="timestamp", order="desc", organization_id=...)` |
| User audit | `investigate_user_audit_logs(user_filter=..., limit=50, offset=0, sort="username", order="asc", organization_id=...)`; no dates |
| Job search | `search_job_groups(search_string=..., job_type="command", subtype=..., limit=50, offset=0, organization_id=...)`; not `query` |
| Job detail | `get_job_group(job_group_id=..., organization_id=...)` |
| CLI output read | `get_cli_command_output(job_group_id=..., device_id=..., organization_id=...)` |
| Per-device results | `get_job_results_by_device(job_group_id=..., result_type="clicmd", search_query=..., limit=50, offset=0, organization_id=...)` |

Paged list limits are clamped to 1–1000 where implemented; offsets are nonnegative. Syslog file query has only a lower limit bound. The firmware comparison reports `searched_total`, `evaluated_total`, `compliance_percent`, counts and lists of non-compliant/unknown devices; its exact equality test does not select a suitable version.

## Verified route corrections and native conditions

- The implemented user config read is `POST /v1/telemetry/config/edit`; the tool table still lists `.../config/view`. The device-authenticated `.../config/get` is unsuitable for the user token and is associated with `Invalid device token size`.
- CLI output uses `POST /v1/telemetry/result/search` with `type:"clicmd"`, group and device IDs. The publisher explicitly identifies this as absent from its public API specification. `total_results=0` is not command completion.
- `_api_post` wraps successful payloads under `data`; `get_port_telemetry` inspects top-level `status_record` and returns no `ok` field. It is deliberately excluded in favor of the full telemetry tool.
- HTTP 401 clears the session and returns `Unauthorized or token expired. Run login_with_env again.` Other HTTP errors retain status/body through the failure wrapper.
- Missing identity: `Provide either device_id or serial_num.` Missing firmware device: `Device not found.` Organization-required errors identify the project-admin scope problem rather than implying absent inventory.
- A successful login lacking either `token` or `csrf_token` is an error; its attached raw payload may include sensitive session data and must not be copied into a report.

Sources: publisher [tool guide](https://github.com/Lantronix/percepxion-mcp-server/blob/533fdc981f0457043e948204db216e2b8a4076f5/docs/tools.md), [server](https://github.com/Lantronix/percepxion-mcp-server/blob/533fdc981f0457043e948204db216e2b8a4076f5/src/percepxion_mcp/server.py), [client](https://github.com/Lantronix/percepxion-mcp-server/blob/533fdc981f0457043e948204db216e2b8a4076f5/src/percepxion_mcp/client.py), retrieved 2026-10-09.
