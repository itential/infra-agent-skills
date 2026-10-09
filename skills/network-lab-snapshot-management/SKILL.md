---
name: network-lab-snapshot-management
description: >-
  Create, list, restore, or delete a lab snapshot. Use for GNS3 project snapshot lifecycle operations. Covers GNS3 v2. Assumes an authenticated API or supported SDK client for the target lab platform.
---

# Network lab snapshot management

Create, list, restore, or delete a lab snapshot.

## When to use this skill

Use for GNS3 project snapshot lifecycle operations.

## Universal concepts

No common wire protocol is implied by this capability. A snapshot is associated with a project and has its own identity. Restore and deletion alter persisted state.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Snapshot contents and runtime consistency are platform-specific; no cross-platform or memory-state portability is assumed.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API or supported SDK client for the target lab platform. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
