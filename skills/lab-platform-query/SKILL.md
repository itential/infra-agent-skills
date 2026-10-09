---
name: lab-platform-query
description: >-
  Read laboratory controller health, resource statistics, licensing and node definitions. Use for Cisco CML platform inspection before or during lab use. Covers Cisco CML. Assumes an authenticated Cisco CML SDK client with permission to inspect the controller.
---

# Lab platform query

Read laboratory controller health, resource statistics, licensing and node definitions.

## When to use this skill

Use for Cisco CML platform inspection before or during lab use.

## Universal concepts

No common wire protocol is implied by this capability. Controller observations and guest readiness are different results. Resource and licensing data retain their native platform meaning.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No capacity guarantee, stale-lab deletion, licensing mutation or fixed per-node resource rule is supplied.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Cisco CML SDK client with permission to inspect the controller. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
