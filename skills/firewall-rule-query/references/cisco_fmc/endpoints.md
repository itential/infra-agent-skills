# Cisco FMC rule-search bindings

Sources: [tool schema](https://github.com/CiscoDevNet/CiscoFMC-MCP-server-community/blob/main/sfw_mcp_fmc/server.py) and [search implementation](https://github.com/CiscoDevNet/CiscoFMC-MCP-server-community/blob/main/sfw_mcp_fmc/tools/search_access.py), main retrieved 2026-10-09.

| Operation | Literal MCP tool | Key inputs |
|---|---|---|
| Discover FMC | `list_fmc_profiles()` | Returns `mode`, `profiles`, and default profile where configured. |
| Search known access policy | `find_rules_by_ip_or_fqdn` | `query`, `access_policy_id`; optional `domain_uuid`, `fmc_profile`. |
| Resolve device assignment and search | `find_rules_for_target` | `query`, `target`; optional `indicator_type`, `rule_set`, `domain_uuid`, `fmc_profile`. |
| Search selected domain/policy | `search_access_rules` | `indicator`, `indicator_type`, `rule_set`, `scope`; optional policy/rule filters below. |

`indicator_type`: `auto`, `ip`, `subnet`, `fqdn`, `sgt`, `realm_user`, `realm_group`. `rule_set`: `access`, `prefilter`, `both`. `scope`: `fmc` or `policy`; policy scope requires `policy_id` or `policy_name`.

General search filters: `policy_name_contains`, `max_policies`, `rule_section`, `rule_action`, `enabled_only`, `rule_name_contains`, `max_results`, `domain_uuid`, `fmc_profile`. The current implementation constrains `max_results` to 1–500 and `max_policies` to 0–1000, with 0 meaning no explicit policy cap. Target search internally limits each policy search to 200 results; completeness must be checked.

The general response has `meta`, `items`, and `matched_objects`. Important metadata includes `policies_considered`, `policies_scanned`, `matched_rules_count`, `truncated`, and `prefilter`. Policy/target helper responses may be JSON-encoded strings and require decoding.

Error objects carry `error.category` and `error.message`. Categories include `INVALID_INDICATOR`, `VALIDATION`, `RESOLUTION`, `FMC_CLIENT`, and `UNEXPECTED`. Exact missing assignment messages are `No Access Policy assigned to this target.` and `No Prefilter Policy assigned to this target.` Such errors are not empty successful searches.
