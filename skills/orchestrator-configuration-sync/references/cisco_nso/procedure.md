# Cisco NSO device-to-CDB synchronization

Import one device's current configuration into NSO and report the resulting device synchronization state.

Sources: [NSO 6.5 lifecycle operations](https://nso-docs.cisco.com/guides/nso-6.5/operation-and-usage/operations/lifecycle-operations), [publisher MCP registration](https://github.com/NSO-developer/cisco-nso-mcp-server/blob/main/cisco_nso_mcp_server/server.py), [device implementation](https://github.com/NSO-developer/cisco-nso-mcp-server/blob/main/cisco_nso_mcp_server/services/devices.py), retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

1. **Check the selected device.** The current synchronization read identifies the native result for the explicit NSO device name. A missing-name or API error stops the sequence as a failed check; it is not a synchronization mismatch.
2. **Import current device configuration.** This operation overwrites the stored NSO copy and commits that change immediately: stop and confirm with the operator before proceeding. The publisher synchronization helper takes the device name and returns the native action result. Any embedded error is failure. A timeout leaves the result uncertain; a new state check is needed before deciding whether another import is warranted.
3. **Check the resulting synchronization state.** The same device check reports the post-import result. The result retains the native action result and native check result; a continuing mismatch or check error is unresolved. This check does not establish service consistency.

## Patterns

- The import direction is device to NSO CDB. No device configuration push belongs to this operation.
- Cisco documents that importing device changes can leave services inconsistent with CDB. Service consistency/redeployment requires the applicable service procedure and is not silently added to the import.
- NSO has richer native dry-run and locking options, but this MCP wrapper exposes only the device name. It does not provide those controls merely because NSO supports them.

## Known limitations

- Imported configuration is immediately committed to NSO; no separate save step or universal rollback guarantee is exposed here.
- Driver-specific synchronization checks do not necessarily produce full differences.
- Service check/redeploy and native import dry-run/lock options are outside this wrapper's schema. A need for those controls requires a separately documented NSO binding.
- The publisher defaults include local unencrypted HTTP and sample administrator credentials. The assumed authenticated deployment must supply appropriate transport and credentials.

## Tools

| Operation | Description | Category |
|---|---|---|
| Check device synchronization | Read the device's current synchronization result | Validation |
| Import device configuration | Replace the NSO copy with current device configuration | Mutating action |

## Verification checklist

- The approved direction and target name match the action.
- Confirmation occurred before overwriting CDB.
- Both the import action and post-import check results are reported, with failures retained.
- Device synchronization was not reported as proof of service consistency.
