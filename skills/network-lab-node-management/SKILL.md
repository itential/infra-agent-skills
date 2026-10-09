---
name: network-lab-node-management
description: >-
  Create and inspect lab nodes and control their runtime state. Use for node creation, inventory, start/stop, supported suspension/reload or wipe, and console metadata. Covers GNS3 v2, Cisco CML, EVE-NG. Assumes an authenticated API or supported SDK client for the target lab platform.
---

# Network lab node management

Create and inspect lab nodes and control their runtime state.

## When to use this skill

Use for node creation, inventory, start/stop, supported suspension/reload or wipe, and console metadata.

## Universal concepts

No common wire protocol is implied by this capability. Node identity is scoped to a laboratory. A running simulation process does not prove the guest OS is ready.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Node types differ in supported actions. Device CLI configuration and software image acquisition are outside this capability.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API or supported SDK client for the target lab platform. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
