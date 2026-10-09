# Cisco RADKit: execute a remote device command

Discover an enrolled device and run the supplied platform-documented command through the Cisco RADKit MCP connector.

Source: [Cisco RADKit MCP community connector README](https://github.com/CiscoDevNet/radkit-mcp-server-community), publisher-hosted example project/main, retrieved 2026-10-09. Bindings appear in [endpoints.md](endpoints.md).

## 1. Discover the target

The inventory operation returns enrolled device names. The attribute operation returns the selected device's connection capabilities and attributes. The authorized service and exact enrolled device name establish scope.

Success: the requested device exists in that service inventory and exposes the required access mechanism. Missing or inaccessible inventory is not a device-health verdict.

## 2. Execute the approved command

The command operation sends the supplied command through RADKit, with explicit timeout and output-length settings when required. **For a configuration, reload, clearing, or other live-affecting command, stop and confirm with the operator before proceeding.** The configured user's RADKit permissions constrain what the command can do; the connector is not universally read-only.

Success: the operation returns the device response. The structured command variant includes status and truncation information, while the raw variant returns text. Truncated output is reported as incomplete. The caller's platform-specific command documentation supplies the success condition and native error handling.

## 3. Preserve the outcome

The result names the service and device, exact command, response, status and any truncation. A connection failure or timeout is not interpreted as an empty successful result. The README supplies no universal retry interval or guarantee about the outcome of a mutation whose response was lost; that case remains unknown pending device-specific inspection.

## Patterns

Inventory and attribute discovery precede execution. Structured output is preferable when truncation and status need explicit handling. Remote access does not imply the queried device is reachable by a direct local connection.

## Known limitations

Cisco labels this connector example/proof-of-concept code. The documented implementation lacks MCP client authentication; a network-reachable client can invoke its tools. Default local stdio avoids that listener, and any network deployment requires the publisher's authentication, TLS and access-control safeguards. This procedure assumes an already secured deployment.

The connector also offers SNMP polling, which is not command execution and is outside this procedure. The command transport does not define platform-independent configuration rollback or output interpretation.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| RADKit MCP client | Discovers enrolled devices and submits command requests | MCP transport |
| RADKit device session | Carries commands to the enrolled device | Remote device transport |

## Verification checklist

- The selected service and device match discovered inventory.
- The supplied command is documented for that device platform.
- Live-affecting commands carry operator confirmation.
- Status, device error text and truncation are preserved in the outcome.
