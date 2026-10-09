# Cisco Meraki: query a controller record

Retrieve the requested Dashboard information through Cisco's read-only MCP catalogue.

Source: [Cisco Meraki MCP Server README](https://github.com/CiscoDevNet/cisco-meraki-mcp-official), beta/main, retrieved 2026-10-09. This procedure uses the publisher's documented search/select/execute workflow; NetClaw's empirical operation counts and sandbox results are not API guarantees.

## 1. Identify the accessible scope

The configured Dashboard identity supplies the organization and network access. Cisco recommends an identity with read-only Dashboard permissions: the MCP blocks writes, but a read-write API key could still authorize direct API calls outside it. The selected hosted service supports the Meraki.com environment; other Meraki environments require the local server.

Success: the configured service and identity correspond to the requested organization. Key errors require checking whether Dashboard API access and the relevant organization/network permissions are enabled. An unavailable server is a connection failure, not an empty inventory.

## 2. Discover the requested read operation

The catalogue search receives the requested resource and scope in ordinary language. Its ranked results supply capability identifiers and the inputs for the selected capability. The chosen operation must describe the requested read: examples include network SSIDs, switch ports, appliance settings, device availability, configuration history, or organization inventory.

Success: a matching capability and its required parameters are available. A missing match leaves the requested operation unsupported by this catalogue; it does not prove the resource is absent. The current catalogue is authoritative rather than remembered SDK method names.

## 3. Retrieve the record

The execution operation receives the selected identifier and parameters from discovery. If required organization, network, or device identifiers are unknown, the same discovery-and-execution sequence first obtains those parent records. The server validates the selected capability and invokes the Dashboard SDK.

Success: the tool returns the live Dashboard API response for the selected parameters. Authentication or permission failures remain failures, not empty data. The publisher documents automatic exponential backoff for API throttling. No fixed retry count or guaranteed completion time is documented here.

## 4. Report the returned scope

The result includes the queried organization/network/device identifiers, requested time range where applicable, returned data, and any error. Pagination follows the selected capability's documented contract; this README does not guarantee collection-wide automatic pagination, so an unverified page is reported as a page. A successfully returned empty list describes only that query.

## Patterns

The same search/select/execute sequence applies across Dashboard product families. Reading existing diagnostic results does not authorize starting a diagnostic action. Search ranking is a discovery aid, not a statement that the first result matches the request.

## Known limitations

The publisher marks this server as beta; schemas and supported capabilities can change. OAuth is not supported by this documented release. No universal health threshold, causal inference, firewall implicit-rule interpretation, or complete inventory claim is supplied by this generic retrieval procedure. Product-specific interpretation requires the corresponding Dashboard operation documentation.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover capability | Find a matching supported read and its parameters | MCP discovery |
| Execute selected capability | Retrieve its Dashboard response | MCP query |

Bindings appear in [endpoints.md](endpoints.md).

## Verification checklist

- The selected capability came from the connected publisher catalogue.
- Required parent identifiers and filters match the intended scope.
- A returned response is distinguished from authentication, transport, or parameter failure.
- Time and pagination scope remain visible in the result.
