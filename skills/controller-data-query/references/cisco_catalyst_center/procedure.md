# Cisco Catalyst Center: query a controller record

Retrieve a scoped controller record through a release-matched Cisco MCP catalogue.

Source: [Catalyst Center MCP Server README](https://github.com/cisco-en-programmability/catc-mcp-oss), main and release-selection guidance, retrieved 2026-10-09.

## 1. Select the controller and catalogue

The publisher requires the server release branch to match the Catalyst Center release. The configured identity controls authorization. The server's readiness check verifies credential configuration only; it does not contact Catalyst Center or prove the credentials work.

Success: the connected tool catalogue belongs to the intended controller release and its identity has the required read permission. Missing server configuration is resolved before a controller query. Authentication or connectivity remains unverified until an actual operation succeeds.

## 2. Discover a read operation

The client discovers the generated tools and examines the selected tool's input schema and documented purpose. The requested scope may be inventory, sites, client or device health, wireless experience, software, compliance, or events. Parent identifiers are resolved through matching read tools before the dependent query.

Success: a generated operation matches the requested read, with its required identifiers and time filters known. The official server does not enforce read-only behavior and may expose configuration-changing tools; those operations are outside this procedure. NetClaw's grouped dispatchers and catalogue counts are not properties of this server.

## 3. Query and retain the native result

The selected read tool executes with the account's Catalyst Center permissions. The client supplies parameters using that tool's release-specific schema and retains the returned records and native errors.

Success: the selected operation returns its documented record or list. Permission rejection, bad parameters, and transport failure do not establish absence. The README does not define common retry rules, numeric rate limits, pagination, or a single outcome envelope; those remain specific to the generated operation and its versioned API documentation. A result requiring such undocumented behavior remains explicitly incomplete until that operation's guidance is available.

## Patterns

Device-health and wireless investigation examples first resolve a site and then retrieve records for that scope. Software/compliance results are observations; their priority is an operator decision, not a generic procedure default.

## Known limitations

The server adds no extra authorization layer. Its local MCP endpoint has no inbound authentication in the published example; Cisco requires private exposure or external network controls and authentication. The README includes examples disabling certificate verification but advises keeping verification enabled for trusted certificates. This procedure assumes the existing connection meets those safeguards.

A successful empty response describes the chosen appliance, account, filters, and record type. It does not establish that no devices exist outside that controller scope. Controller observations are not a direct device measurement.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover generated tools | Obtain the release-specific catalogue and input schemas | MCP discovery |
| Query selected controller record | Execute a documented read operation | MCP query |

Bindings appear in [endpoints.md](endpoints.md).

## Verification checklist

- The catalogue release matches the target controller.
- The selected operation is documented as a read.
- Required identifiers and time filters came from the request or parent reads.
- The native response and any uncertainty about completeness are preserved.
