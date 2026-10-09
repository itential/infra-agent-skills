# Cisco CML users and groups: bindings

Authenticated `virl2_client.ClientLibrary` is `client`.

| Operation | SDK binding |
|---|---|
| List/read users | `client.user_management.users()`; `get_user(user_id)` |
| Create user | `client.user_management.create_user(username, pwd, fullname=..., description=..., email=..., admin=..., groups=...)` |
| Update user | `client.user_management.update_user(user_id, fullname=..., description=..., email=..., admin=..., groups=...)` |
| Delete user | `client.user_management.delete_user(user_id)` |
| List/read groups | `client.group_management.groups()`; `get_group(group_id)` |
| Create group | `client.group_management.create_group(name, description=..., members=...)` |
| Update group | `client.group_management.update_group(group_id, name=..., description=..., members=...)` |
| Delete group | `client.group_management.delete_group(group_id)` |

Ellipses mean only caller-selected values, not literal payload values. `groups` and `members` contain returned platform IDs. No undocumented password dictionary is supplied. Client/server compatibility and existing TLS-verifying authentication are prerequisites.

## Sources

- [Cisco user SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/user.py). Retrieved 2026-10-09.
- [Cisco group SDK](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/models/group.py). Retrieved 2026-10-09.
- [Cisco client initialization](https://github.com/CiscoDevNet/virl2-client/blob/7ac2c924ccbdc02264578a95327f8a1363172076/virl2_client/virl2_client.py). Retrieved 2026-10-09.
