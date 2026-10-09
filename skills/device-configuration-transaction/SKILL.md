---
name: device-configuration-transaction
description: >-
  Load, validate and commit an approved device configuration through a supported configuration session. Use for reviewing an intended configuration, checking its candidate difference, and committing the approved change. Covers Juniper Junos MCP. Assumes an authenticated Junos MCP client, mapped router access, and an approved configuration payload or template.
---

# Device configuration transaction

Load, validate and commit an approved device configuration through a supported configuration session.

## When to use this skill

Use for reviewing an intended configuration, checking its candidate difference, and committing the approved change.

## Universal concepts

No common wire protocol is implied by this capability. A rendered payload, a validated candidate, and a committed configuration are different outcomes. A transport failure may leave the final state uncertain.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure does not design configuration, choose a business rollback trigger, or guarantee atomic behavior across devices.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Junos MCP client, mapped router access, and an approved configuration payload or template. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
