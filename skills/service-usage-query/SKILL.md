---
name: service-usage-query
description: >-
  Read a platform's reported usage over an explicit date interval. Use for Auvik client-wide or device-specific billing usage retrieval. Covers Auvik API v1. Assumes authenticated access to the requested Auvik client usage data.
---

# Service usage query

Read a platform's reported usage over an explicit date interval.

## When to use this skill

Use for Auvik client-wide or device-specific billing usage retrieval.

## Universal concepts

No common wire protocol is implied by this capability. Reported usage and invoice totals are distinct records. Scope and dates are part of the result.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No cost forecast, invoice approval or device-billing change is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes authenticated access to the requested Auvik client usage data. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
