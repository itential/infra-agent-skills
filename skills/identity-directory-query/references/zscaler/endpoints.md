# ZIdentity query bindings

Sources: [users](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zid/users.py), [groups](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zid/groups.py), master retrieved 2026-10-09.

| Operation | MCP tool | Input fields |
|---|---|---|
| Find user | `zid_search_users` | `name`; optional `offset`, `limit`. |
| List users | `zid_list_users` | Optional `login_name`, `display_name`, `primary_email`, exact `domain_name`, exact `idp_name`, `offset`, `limit`. |
| Find group | `zid_search_groups` | `name`; optional `offset`, `limit`. |
| List groups | `zid_list_groups` | Optional partial `name`, `exclude_dynamic_groups`, `offset`, `limit`. |
| Read user/group | `zid_get_user` / `zid_get_group` | `user_id` / `group_id`, string. |
| Read user's groups | `zid_get_user_groups` | `user_id`; optional `offset`, `limit`. |
| Read group's users | `zid_get_group_users` | `group_id`; optional `offset`, `limit`. |

`offset` is an integer of at least 0 and `limit` is 1–1000. Search/list filters are case-insensitive partial matches except the explicitly exact filters above. The publisher's current registered MCP input schema determines transport argument wrapping; these are model field names, not a separate SDK object.

Tools return one dictionary or a list of dictionaries. Input failures use `ValueError`; SDK errors become `RuntimeError` with the relevant operation and upstream error. No fixed numeric retry or rate limit is published in these tool references.
