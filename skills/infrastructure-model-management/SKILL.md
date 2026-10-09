---
name: infrastructure-model-management
description: >-
  Query infrastructure objects and prepare a branch-isolated model change for review. Use for schema discovery, object reads/searches, scalar or relationship changes, deletion and proposed-change creation. Covers OpsMill Infrahub MCP. Assumes an authenticated Infrahub MCP client with the required read or write permissions.
---

# Infrastructure Model Management

Query infrastructure objects and prepare a branch-isolated model change for review.

## When to use this skill

Use for schema discovery, object reads/searches, scalar or relationship changes, deletion and proposed-change creation.

## Universal concepts

No common wire protocol is implied by this capability. Object kinds and valid fields come from the selected platform schema. A proposed change and an applied change are different outcomes.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure ends at creation of a proposed change; merging, schema administration and deployment to devices are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Infrahub MCP client with the required read or write permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
