---
name: standards-document-query
description: >-
  Locate an RFC and read its requested section with current publication context. Use for RFC number or keyword lookup and section-level protocol research. Covers RFC Editor. Assumes a browser or document client that can retrieve the official RFC Editor pages.
---

# Standards document query

Locate an RFC and read its requested section with current publication context.

## When to use this skill

Use for RFC number or keyword lookup and section-level protocol research.

## Universal concepts

No common wire protocol is implied by this capability. A published document identifier and its current status are different information. A lookup does not certify an implementation.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No third-party MCP package, automated compliance verdict or draft-to-standard equivalence is assumed.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes a browser or document client that can retrieve the official RFC Editor pages. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
