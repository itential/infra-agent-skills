---
name: network-tenant-creation
description: >-
  Create an empty network policy tenant. Use for creating an explicitly named empty Cisco ACI tenant and verifying its managed object. Covers Cisco ACI APIC. Assumes an authenticated HTTPS APIC client and the deployed release model reference.
---

# Network tenant creation

Create an empty network policy tenant.

## When to use this skill

Use for creating an explicitly named empty Cisco ACI tenant and verifying its managed object.

## Universal concepts

No common wire protocol is implied by this capability. The tenant name and administrative context identify the object. A persisted tenant record does not establish application reachability or complete its child network policy.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure creates the empty tenant only; VRFs, bridge domains, subnets, EPGs, contracts and automatic rollback are outside its scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated HTTPS APIC client and the deployed release model reference. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
