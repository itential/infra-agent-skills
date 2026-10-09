# Equinix Network Edge MCP bindings

Source: [Network Edge Tools](https://docs.equinix.com/equinix-api/mcp-servers/ne-mcp-tools/), retrieved 2026-10-09. The configured OAuth client connects to `https://mcp.equinix.com/fabric`; Network Edge does not use a second MCP endpoint. All listed methods require Viewer access. `tools/list` supplies exact parameters and paging.

| Operation | Tool |
|---|---|
| Devices / selected virtual device | `list_devices` |
| Metros | `list_metros` |
| Device types | `list_device_types` |
| Accounts by metro | `list_accounts` |
| Device ACL | `list_acls` |
| ACL templates / selected template | `list_aclTemplates` |
| Visible projects | `list_project` |

The catalogue links individual tools to their native API references but does not give a full parameter/error schema. No undocumented create, update or delete method is assumed.
