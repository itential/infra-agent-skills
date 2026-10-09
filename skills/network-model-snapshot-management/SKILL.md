---
name: network-model-snapshot-management
description: >-
  Create, list or delete stored network-model snapshots. Use for managing Batfish configuration snapshots for offline analysis. Covers Batfish through Pybatfish. Assumes a configured Pybatfish client and an authorized Batfish service connection.
---

# Network Model Snapshot Management

Create, list or delete stored network-model snapshots.

## When to use this skill

Use for managing Batfish configuration snapshots for offline analysis.

## Universal concepts

No common wire protocol is implied by this capability. Snapshot storage is separate from live device configuration. A snapshot name and its containing network identify the requested object.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This capability covers stored snapshot lifecycle, not live device changes or policy compliance.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes a configured Pybatfish client and an authorized Batfish service connection. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
