# FWRule MCP bindings

Source: [publisher README](https://github.com/AutomateIP/fwrule-mcp/blob/main/README.md), retrieved 2026-10-09. A configured local MCP client supplies the connection; no firewall API credentials are needed for offline analysis.

| Operation | Tool | Inputs |
|---|---|---|
| Discover formats | `list_supported_vendors` | No arguments |
| Parse policy | `parse_policy` | `vendor`, `ruleset_payload`; optional `os_version`, `context_objects` |
| Analyze native candidate | `analyze_firewall_rule_overlap` | `vendor`, `ruleset_payload`, `candidate_rule_payload`; optional `os_version`, `context_objects`, `candidate_position` |
| Analyze normalized candidate | `analyze_firewall_rule_overlap` | `existing_rules` as a JSON string containing an array, `candidate_rule` as a JSON string containing one object; optional `candidate_position` |

`candidate_position` is one-based. Normalized objects use `id`, `position`, `enabled`, `action`, `source_zones`, `destination_zones`, `source_addresses`, `destination_addresses`, `services` (objects with `protocol` and `ports`), and `applications`.

| Canonical vendor | Publisher input format | Publisher version scope |
|---|---|---|
| `panos` | XML configuration | PAN-OS/Panorama 9.x–11.x |
| `asa` | Running configuration text | ASA 9.x+ |
| `ftd` | FMC JSON export | FTD 6.x–7.x |
| `ios` | Running configuration text | IOS/IOS-XE 12.x–17.x |
| `iosxr` | Running configuration text | IOS-XR 6.x+ |
| `checkpoint` | Access rulebase JSON | R80.x–R82.x |
| `juniper` | Set-format configuration | SRX 19.x+ |
| `junos` | Set-format configuration | MX/PTX/QFX 18.x+ |
| `sros` | MD-CLI info/flat configuration | SR OS 20.x+ |
| `fortios` | Full configuration text | FortiOS/FortiGate 6.x–7.x |

The cited README gives no exhaustive machine-readable error/result schema. A deployed tool schema and its returned findings govern result fields; absent fields are not inferred.
