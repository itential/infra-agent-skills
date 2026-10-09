---
name: out-of-band-device-query
description: >-
  Read console-server inventory, ports, stored configuration, firmware and audit/job evidence. Use for scoped Lantronix Percepxion device, telemetry, firmware-comparison, stored-log and existing-job reads. Covers Lantronix Percepxion. Assumes a configured Lantronix Percepxion MCP connection and authorized credential provider.
---

# Out-of-Band Device Query

Read console-server inventory, ports, stored configuration, firmware and audit/job evidence.

## When to use this skill

Use for scoped Lantronix Percepxion device, telemetry, firmware-comparison, stored-log and existing-job reads.

## Universal concepts

No common wire protocol is implied by this capability. The console server and devices attached to its ports are distinct identities. Stored telemetry and job evidence retain their collection scope and native outcome.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No console commands, firmware update, configuration change, reboot, access-control edit or device lifecycle mutation is supported.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes a configured Lantronix Percepxion MCP connection and authorized credential provider. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
