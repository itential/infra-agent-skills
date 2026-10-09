---
name: asset-lifecycle-query
description: >-
  Read reported asset lifecycle, support and warranty information. Use for Auvik device end-of-sale, maintenance, support and coverage queries. Covers Auvik API v1. Assumes an authenticated Auvik API client with access to the requested tenant.
---

# Asset lifecycle query

Read reported asset lifecycle, support and warranty information.

## When to use this skill

Use for Auvik device end-of-sale, maintenance, support and coverage queries.

## Universal concepts

No common wire protocol is implied by this capability. Lifecycle dates and coverage are reported records, not an automatic replacement or risk-priority decision.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No procurement recommendation, asset mutation or guaranteed vendor coverage is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Auvik API client with access to the requested tenant. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
