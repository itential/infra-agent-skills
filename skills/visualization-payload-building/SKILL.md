---
name: visualization-payload-building
description: >-
  Build a structured visualization envelope from supplied content and source metadata. Use for creating a NetClaw A2UI JSON payload for one supported visualization component. Covers NetClaw Canvas envelope builder. Assumes the pinned NetClaw JavaScript modules are installed in a compatible local module runtime.
---

# Visualization payload building

Build a structured visualization envelope from supplied content and source metadata.

## When to use this skill

Use for creating a NetClaw A2UI JSON payload for one supported visualization component.

## Universal concepts

No common wire protocol is implied by this capability. The envelope describes content and provenance; constructing it does not display a user interface or validate the source data.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No live collection, inferred health score, automatic incident workflow, persistent audit service, or claim of Canvas client compatibility is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes the pinned NetClaw JavaScript modules are installed in a compatible local module runtime. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
