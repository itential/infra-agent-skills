---
name: network-model-query
description: >-
  Query a collected network model for inventory, protocol state, assertions and forwarding paths. Use for scoped model queries, summaries and evidence-backed connectivity or consistency analysis. Covers IP Fabric, SuzieQ, Topolograph, Batfish, and Forward Networks. Assumes the selected API/MCP/SDK connection or CLI is configured against an existing network model or collection.
---

# Network Model Query

Query a collected network model for inventory, protocol state, assertions and forwarding paths.

## When to use this skill

Use for scoped model queries, summaries and evidence-backed connectivity or consistency analysis. Supported platforms: IP Fabric, SuzieQ, Topolograph, Batfish, and Forward Networks.

## Universal concepts

No common wire protocol is implied by this capability. The selected snapshot or collection time is part of the answer. A model result is distinct from a live packet test.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Collection, device configuration and arbitrary API mutation are outside scope. Each platform defines its own findings and completeness.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes the selected API/MCP/SDK connection or CLI is configured against an existing network model or collection. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
