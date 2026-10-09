---
name: orchestrator-configuration-sync
description: >-
  Refresh an orchestrator's stored device configuration from the device. Use for Cisco NSO device-to-CDB synchronization and its resulting device synchronization status. Covers Cisco NSO through its publisher MCP server. Assumes an authenticated NSO MCP client authorized to read devices and modify NSO CDB.
---

# Orchestrator configuration synchronization

Refresh an orchestrator's stored device configuration from the device.

## When to use this skill

Use for Cisco NSO device-to-CDB synchronization and its resulting device synchronization status.

## Universal concepts

No common wire protocol is implied by this capability. Synchronization direction determines which state is overwritten. A successful device synchronization does not prove every service remains consistent.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure imports device configuration into NSO; it does not push CDB configuration to devices or redeploy services.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated NSO MCP client authorized to read devices and modify NSO CDB. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
