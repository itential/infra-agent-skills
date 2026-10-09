# ZIA cloud firewall MCP bindings

Source: [cloud firewall tools](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zia/cloud_firewall_rules.py), [rule helpers](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/common/zia_helpers.py), [activation tools](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zia/activation.py), [confirmation protocol](https://github.com/zscaler/zscaler-mcp-server/blob/master/docs/guides/mcp-protocol.md), master, retrieved 2026-10-09.

| Operation | Tool | Inputs / result |
|---|---|---|
| List rules | `zia_list_cloud_firewall_rules` | Optional `search` string; rule collection |
| Read rule | `zia_get_cloud_firewall_rule` | String `rule_id`; rule record |
| Create rule | `zia_create_cloud_firewall_rule` | Required `name`, `action`; optional fields below; created rule |
| Update rule | `zia_update_cloud_firewall_rule` | Required `rule_id`; intended replacement fields below; updated rule |
| Delete rule | `zia_delete_cloud_firewall_rule` | `rule_id`; final `success: true` and message after confirmation |
| Activate configuration | `zia_activate_configuration` | No arguments; activation record with `status` |
| Read activation status | `zia_get_activation_status` | No arguments; activation record with `status` |

Create/update common inputs: `name`, `action`, `description` strings; `enabled` boolean; `order` positive integer; `rank` integer 0–7; `advanced` dictionary using SDK snake_case. Create defaults are `enabled: true`, `order: 1`, `rank: 7`. Rank zero is highest and seven lowest; order is one-based. Action examples in the schema are `ALLOW`, `BLOCK_DROP`, `BLOCK_RESET`, not an exhaustive enumeration.

Verified advanced keys include `src_ips`, `dest_addresses`, `source_countries`, `dest_countries`, `dest_ip_groups`, `dest_ipv6_groups`, `departments`, `devices`, `device_groups`, `groups`, `labels`, `locations`, `location_groups`, `nw_applications`, `nw_application_groups`, `nw_services`, `nw_service_groups`, `time_windows`, `users`, `workload_groups`, `enable_full_logging`. Value types and allowed object references require the installed SDK schema; the wrapper accepts a dictionary and does not establish every downstream constraint.

Rule/API failures are operation-specific exceptions carrying the SDK error. Locally rejected order/rank values do not produce a rule write. The activation model has a string `status` but no full enum or timeout; status names must not be fabricated.

The native delete flow obtains an operator decision through elicitation. Without elicitation, the initial result contains `DESTRUCTIVE OPERATION - CONFIRMATION REQUIRED`; an approved retry retains identical arguments and supplies `kwargs={"confirmation_token": "<returned-token>"}`. Invalid, expired or spent fallback tokens fail. A token is a binding mechanism, not evidence of human approval.
