---
name: network-model-configuration
description: >-
  Apply one transactional change to model-defined network configuration. Use for updating, replacing, or deleting explicitly selected configuration paths in one transaction. Covers OpenConfig gNMI-compatible targets. Assumes an authenticated gNMI client, TLS connection, the target-supported schema, and an approved change payload.
---

# Network model configuration

Apply one transactional change to model-defined network configuration.

## When to use this skill

Use for updating, replacing, or deleting explicitly selected configuration paths in one transaction.

## Universal concepts

No common wire protocol is implied by this capability. The gNMI protocol defines transaction boundaries and operation ordering. Actual paths, value types and constraints come from the target model.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure covers delete, replace and update in one request. It excludes union-replace extensions, business approval systems, and automatic rollback of later operational effects.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated gNMI client, TLS connection, the target-supported schema, and an approved change payload. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
