---
name: configuration-backup-query
description: >-
  List and read stored device configuration backups. Use for Auvik backup-history inspection and retrieval of a selected stored configuration. Covers Auvik API v1. Assumes authorized API access to the relevant tenant and configuration records.
---

# Configuration backup query

List and read stored device configuration backups.

## When to use this skill

Use for Auvik backup-history inspection and retrieval of a selected stored configuration.

## Universal concepts

No common wire protocol is implied by this capability. Stored backups are historical observations, not necessarily the current running device configuration.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No restore, new backup trigger, live configuration push or automatic sharing is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes authorized API access to the relevant tenant and configuration records. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
