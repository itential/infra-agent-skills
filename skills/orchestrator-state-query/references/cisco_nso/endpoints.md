# Cisco NSO MCP query bindings

Source: [server registration](https://github.com/NSO-developer/cisco-nso-mcp-server/blob/main/cisco_nso_mcp_server/server.py), publisher main, retrieved 2026-10-09.

| Operation | MCP name | Tool arguments |
|---|---|---|
| Read device groups | `get_device_groups` | `{}`; optional unused `params` |
| Read driver identifiers | `get_device_ned_ids` | `{}`; optional unused `params` |
| Read device platform | `get_device_platform` | `{"params":{"device_name":"<device-name>"}}` |
| Read device configuration | `get_device_config` | `{"params":{"device_name":"<device-name>"}}` |
| Read device state | `get_device_state` | `{"params":{"device_name":"<device-name>"}}` |
| Check device synchronization | `check_device_sync` | `{"params":{"device_name":"<device-name>"}}` |
| Discover service types | `get_service_types` | `{}`; optional unused `params` |
| Read service instances | `get_services` | `{"params":{"service_type":"<namespace:service-type>"}}` |

Results preserve native NSO/helper data. Failures are objects containing `status: "error"` and `error_message`; some include empty `services`, `service_types`, `device_groups` or `device_ned_ids` arrays. Exact missing-field errors are `Missing required parameter: device_name` and `Missing required parameter: service_type`; an empty device name can produce `Device name is required`. No universal success envelope is implemented.
