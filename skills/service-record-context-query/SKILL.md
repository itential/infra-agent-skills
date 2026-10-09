---
name: service-record-context-query
description: >-
  Retrieve linked service-management tickets and assets without changing records. Use for ticket and asset lookup, linked-record context, ticket actions, and ticket-type discovery. Covers Halo REST API. Assumes an authenticated API client and the target installation’s API details and version are available.
---

# Service Record Context Query

Retrieve linked service-management tickets and assets without changing records.

## When to use this skill

Use for ticket and asset lookup, linked-record context, ticket actions, and ticket-type discovery.

## Universal concepts

No common wire protocol is implied by this capability. Returned records retain their platform identities and relationships; a truncated result is not a complete inventory.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No ticket creation, approval, closure, asset mutation, or operational policy decisions. The verified Halo documentation is version 2.85.1; current tenant compatibility must be established before use.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API client and the target installation’s API details and version are available. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
