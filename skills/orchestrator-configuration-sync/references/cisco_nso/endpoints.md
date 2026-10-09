# Cisco NSO synchronization MCP bindings

Source: [publisher server](https://github.com/NSO-developer/cisco-nso-mcp-server/blob/main/cisco_nso_mcp_server/server.py), main, retrieved 2026-10-09.

| Operation | Tool | Arguments |
|---|---|---|
| Check device synchronization | `check_device_sync` | `{"params":{"device_name":"<device-name>"}}` |
| Import device configuration | `sync_from_device` | `{"params":{"device_name":"<device-name>"}}` |

The tools retain the native helper response rather than defining a universal success envelope. Missing parameters produce `status: "error"` with `error_message: "Missing required parameter: device_name"`; other failures use the same error status and underlying message. An empty name produces `Device name is required` within error handling. The import tool is explicitly annotated `readOnlyHint: false`. No `dry_run`, lock timeout, service type or redeploy argument exists in this wrapper.
