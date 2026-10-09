# Catalyst Center query bindings

Source: [official MCP README](https://github.com/cisco-en-programmability/catc-mcp-oss), main, retrieved 2026-10-09.

The publisher generates tools per `release/<M.N.P.Q>`. Exact names and input schemas must be obtained from that running release's MCP catalogue. The client uses standard MCP tool discovery (`tools/list`) and invocation (`tools/call`, with the discovered `name` and `arguments`). No NetClaw `catc_find` or `catc_<group>` wrapper is assumed.

| Binding | Meaning |
|---|---|
| `http://localhost:7001/v1/mcp` | Publisher's local streamable HTTP example; configured deployments may use stdio or externally secured HTTPS. |
| `GET /v1/health` | Checks the MCP server process. |
| `GET /v1/readiness` | Checks required controller configuration, without querying the controller. |
| `CATALYST_CENTER_HOST`, `CATALYST_CENTER_USERNAME`, `CATALYST_CENTER_PASSWORD` | Server-side target and authentication configuration. Secrets are not task payloads. |
| `CATALYST_CENTER_VERIFY_SSL=true` | Publisher-recommended certificate verification for a trusted controller certificate. |

The README does not publish one stable cross-release operation schema or error envelope. Literal controller routes, pagination fields, and success criteria must come from the selected generated tool's versioned API definition before invocation; this file does not invent them.
