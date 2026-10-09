---
name: hardware-state-query
description: >-
  Read out-of-band system, chassis, manager, firmware and event state. Use for Redfish power-state, component-health, sensor, firmware-inventory and hardware-log inspection. Covers DMTF Redfish services. Assumes an authenticated TLS-verifying Redfish client and an explicitly identified management endpoint.
---

# Hardware state query

Read out-of-band system, chassis, manager, firmware and event state.

## When to use this skill

Use for Redfish power-state, component-health, sensor, firmware-inventory and hardware-log inspection.

## Universal concepts

No common wire protocol is implied by this capability. Redfish is the shared management protocol. A management resource reports its own state; power, health and operating-system availability are distinct observations.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Service implementations expose different schema versions and resource subsets. No power action, firmware update, log clearing or operating-system health proof is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated TLS-verifying Redfish client and an explicitly identified management endpoint. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
