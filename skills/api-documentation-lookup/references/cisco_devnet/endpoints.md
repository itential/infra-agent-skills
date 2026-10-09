# Cisco DevNet Content Search MCP bindings

Source: [publisher README](https://github.com/CiscoDevNet/devnet-content-search-mcp/blob/main/README.md), current main, retrieved 2026-10-09.

Hosted MCP endpoint: `https://devnet.cisco.com/v1/foundation-search-mcp/mcp`. An authenticated MCP client supplies access through its configured Cisco DevNet authentication.

| Operation | Tool | Arguments |
|---|---|---|
| Search Meraki documentation | `Meraki-API-Doc-Search` | Required string `keyword`; optional boolean `return_api_only`; optional `top_k` (default 3, maximum 10) |
| Search Catalyst Center documentation | `CatalystCenter-API-Doc-Search` | Required string `keyword`; optional boolean `return_api_only`, `top_k`; count bounds/default are not specified by the cited README |
| Resolve Meraki operation ID | `Meraki-API-OperationId-Search` | Required string `operation_id` |

The MCP result includes `content`, `structuredContent.result[]`, and `isError`. Documentation records can include `name`, `description`, `content`, `products`, `tags`, `categories`. API records add `api_path`, `api_method`, `api_operation_id`, `openapi_specification` (JSON encoded as a string), and `documentation_url`. Fields describe retrieved documentation, not a controller operation's live result.

Recognizable publisher errors: missing keyword = `Error: 'keyword' is a required property`; throttling = `Error: Rate limit exceeded. Please wait before sending another request`; unavailable service = `Error: Search Service is Unavailable`. Authentication/connection failure details remain those returned by the configured client. No numerical retry policy is documented.
