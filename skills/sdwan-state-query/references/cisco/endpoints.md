# Cisco Catalyst SD-WAN publisher MCP bindings

Source: [tool registration/dispatch](https://github.com/CiscoDevNet/catalyst-sdwan-mcp-community/blob/main/src/server.ts) and [API client](https://github.com/CiscoDevNet/catalyst-sdwan-mcp-community/blob/main/src/services/vmanageApi.ts), main, retrieved 2026-10-09. The tool arguments below are MCP schema fields, not arbitrary HTTP query parameters.

| Operation | Tool names | Arguments |
|---|---|---|
| List devices | `list_devices` | Optional `model` string |
| Resolve device | `get_device_details` | Required `device_id` string, UUID or system IP |
| Fabric inventory | `list_reachable_devices`, `list_controllers`, `list_vedge_inventory` | None |
| Control state | `get_control_connections`, `get_control_summary`, `get_control_statistics` | Required `device_id` |
| OMP state | `get_omp_peers`, `get_omp_routes`, `get_omp_summary` | Required `device_id` |
| BFD state | `get_bfd_sessions`, `get_bfd_summary`, `get_bfd_tloc` | Required `device_id` |
| BGP state | `get_bgp_neighbors`, `get_bgp_routes`, `get_bgp_summary` | Required `device_id` |
| Device/system state | `get_device_interfaces`, `get_system_status`, `get_device_arp`, `get_device_vpn`, `get_device_tloc`, `get_bridge_table` | Required `device_id` |
| Application routing | `get_app_route_statistics`, `get_app_route_sla_class` | Required `device_id` |
| Flow/statistics | `get_cflowd_flows`, `get_cflowd_statistics`, `get_app_log_flows`, `get_app_log_flow_count`, `get_sdwan_stats` | Required `device_id` |
| List templates | `list_device_templates`, `list_feature_templates` | None |
| Template attachment | `get_attached_devices` | Required `template_id` string |
| Template definition | `get_template_definition` | Required `template_id` and `template_type` = `device` or `feature` |
| Policy lists | `list_policy_lists` | Optional `list_type` string |
| Policy definitions | `list_policy_definitions` | Optional `definition_type` string |
| Policy assemblies | `list_policies` | None |
| Alarms | `list_alarms` | Optional numeric `limit`, defaults 100; zero also falls through to default in implementation |

Responses encode native API JSON in MCP text content. Exceptions return `isError: true` and `Error: <message>`. Device detail has an additional non-exception result `{ "error": "Device not found", "device_id": "<requested-id>" }`.

Exact local failures include `device_id is required`, `template_id is required`, `template_id and template_type required`, and `Unknown tool: <name>`. Authentication failures include `JWT login response missing token`, `JWT authentication failed: <status> <body>`, `Session authentication failed: invalid credentials`, and `Failed to extract JSESSIONID from response`. Non-success API responses become `vManage API error <status>: <body>`.

Security binding defect: `new https.Agent({ rejectUnauthorized: false })` is used by the cited implementation. The assumed deployment must correct that behavior for production use; a valid server certificate alone does not enable verification.
