# Cisco Meraki query bindings

Source: [official MCP README](https://github.com/CiscoDevNet/cisco-meraki-mcp-official), beta/main, retrieved 2026-10-09.

| Operation | Literal tool binding | Inputs and result |
|---|---|---|
| Discover capability | `semantic_search(query, top_k)` | Natural-language query; ranked `capability_id` results. `top_k=5` is the publisher's example, not an operational requirement. |
| Execute selected capability | `execute_api(capability_id, parameters)` | Identifier returned by search, with the selected operation's required parameter object; live Dashboard API result. |

Publisher example: `semantic_search(query="list wireless SSIDs", top_k=5)` discovers `getNetworkWirelessSsids`; execution uses `parameters={"networkId":"<network-id>"}`. Other capabilities and parameter names come from discovery, not inference from this example.

Hosted endpoint: `https://mcp.meraki.com/mcp`; authentication header: `Authorization: Bearer <dashboard-api-key>`. A configured local stdio deployment is also supported. No actual credentials belong in reports or committed examples.

The publisher documents HTTP `429 Too Many Requests` handling with exponential backoff in the server. Its README does not enumerate stable MCP error strings or all Dashboard response schemas. Any additional error body remains operation-specific evidence.
