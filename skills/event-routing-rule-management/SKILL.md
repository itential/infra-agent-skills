---
name: event-routing-rule-management
description: >-
  Event routing rule management. Use for inspecting PagerDuty event orchestrations and replacing or adding rules in their service-routing router. Covers PagerDuty. Assumes an authenticated PagerDuty REST API client with the operation-specific permissions.
---

# Event routing rule management

Event routing rule management.

## When to use this skill

Use for inspecting PagerDuty event orchestrations and replacing or adding rules in their service-routing router.

## Universal concepts

No common wire protocol is implied by this capability. Rule order and fallback behavior are part of a routing configuration. A successful save may carry warnings that limit effective behavior.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Router writes only; global and service orchestration inspection is included, but suppression or transformation edits are not.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated PagerDuty REST API client with the operation-specific permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
