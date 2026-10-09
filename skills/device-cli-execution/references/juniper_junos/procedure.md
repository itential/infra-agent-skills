# Juniper Junos MCP: execute an approved command

Execute the supplied platform-documented operational command on an explicitly selected mapped router.

Sources: [Juniper Junos MCP README](https://github.com/Juniper/junos-mcp-server) and [published tool implementation](https://github.com/Juniper/junos-mcp-server/blob/main/jmcp.py), main retrieved 2026-10-09. Tool bindings appear in [endpoints.md](endpoints.md).

## 1. Resolve the device

The router-list operation returns the server's configured mapping with authentication secrets and private-key paths removed. The requested router name must match that mapping. Optional fact collection returns refreshed device facts.

Success: the intended router is present and its identity is unambiguous. A mapping error or connection error ends the attempt; it is not a device command result.

## 2. Execute the supplied command

The operational-command transport accepts the selected router and command. **If the command reloads, clears state, or otherwise affects the live system, stop and confirm with the operator before proceeding.** The publisher's command blocklist remains in force; matching a prohibited pattern causes rejection before command execution. An allowed command is not automatically safe.

Success: returned text contains the actual device response. The MCP implementation supplies router/command annotations and execution timing. Device-native command error text must still be evaluated against the supplied command documentation; successful tool delivery alone does not establish command success.

## 3. Report per-device outcomes

Batch mode executes the same command concurrently on explicitly named routers and returns per-router results, status and timing. The result retains failures for individual routers instead of declaring the batch successful because another device responded.

Success: every requested router has an observed outcome or an explicit failure. The report states any connection error, blocked command, missing router, timeout, or device-native command failure.

## Patterns

The configuration read operation returns expanded inherited configuration in set syntax. The historical difference operation compares running configuration with the selected rollback version; it is not a preview of a new candidate change.

## Known limitations

The transport does not establish a generic pass condition for arbitrary CLI output. The caller supplies documented commands and checks. The publisher recommends SSH keys for production and secured MCP exposure; unauthenticated network exposure can permit device access. Configuration output may contain sensitive material and is not safe to paste into public reports unchanged.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Junos MCP client | Resolves router mapping and invokes operational commands/fact reads | MCP transport |
| Junos SSH/NETCONF session | Publisher's underlying device connection | Device transport |

## Verification checklist

- Router names match the configured inventory.
- The command and its success criteria came from target-platform documentation.
- Any live-affecting command had its inline confirmation gate applied.
- Device-native errors and every per-router batch result remain visible.
