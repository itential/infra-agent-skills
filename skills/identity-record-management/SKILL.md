---
name: identity-record-management
description: >-
  Create, inspect, update or delete platform users and groups. Use for Cisco CML user/group records and explicit group membership changes. Covers Cisco CML. Assumes an authenticated Cisco CML SDK client with authority for the selected user/group operation.
---

# Identity record management

Create, inspect, update or delete platform users and groups.

## When to use this skill

Use for Cisco CML user/group records and explicit group membership changes.

## Universal concepts

No common wire protocol is implied by this capability. Identity records have platform-scoped identifiers. Account and membership changes can alter access.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This does not choose privileges, an onboarding policy, license entitlements or a credential-delivery channel.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Cisco CML SDK client with authority for the selected user/group operation. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
