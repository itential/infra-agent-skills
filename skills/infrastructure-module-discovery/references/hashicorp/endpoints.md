# Terraform Registry MCP bindings

Source: [HashiCorp Terraform MCP reference](https://developer.hashicorp.com/terraform/mcp-server/reference), retrieved 2026-10-09.

The client uses MCP `tools/list` and the returned `inputSchema` before `tools/call`. This reference specifies tool names but does not publish every parameter schema; those inputs are explicitly version-dependent and must come from the connected publisher server.

| Operation | Tool bindings |
|---|---|
| Search provider documentation | `search_providers`; optional `get_provider_capabilities` |
| Read component documentation | `get_provider_details` |
| Search modules | `search_modules`; private: `search_private_modules` |
| Read module documentation | `get_module_details`; private: `get_private_module_details` |
| Read latest version | `get_latest_provider_version`, `get_latest_module_version` |
| Private provider discovery/details | `search_private_providers`, `get_private_provider_details` |

Public discovery uses the `registry` toolset. Private discovery uses `registry-private` and configured `TFE_TOKEN`/`TFE_ADDRESS`. No credentials belong in artifact reports. Source-wrapper names `list_provider_versions` and `list_module_versions` are not asserted to be publisher tools.
