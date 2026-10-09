---
name: routing-speaker-state-query
description: >-
  Read an existing routing speaker's local protocol evidence. Use for NetClaw BGP peer/RIB reads and limited local protocol/GRE status inspection. Covers NetClaw protocol MCP at the pinned source revision. Assumes an already-configured NetClaw protocol MCP runtime and compatible response decoder.
---

# Routing Speaker State Query

Read an existing routing speaker's local protocol evidence.

## When to use this skill

Use for NetClaw BGP peer/RIB reads and limited local protocol/GRE status inspection.

## Universal concepts

No common wire protocol is implied by this capability. A speaker's local observation is distinct from a remote router's state. The response origin is part of the evidence.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No speaker installation, peering establishment or route/metric mutation is supported. Known source defects restrict OSPF and aggregate-status interpretation.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an already-configured NetClaw protocol MCP runtime and compatible response decoder. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
