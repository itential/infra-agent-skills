---
name: trace-span-query
description: >-
  Retrieve indexed trace spans for a supplied query and time interval. Use for searching Datadog APM indexed spans and collecting span, parent and trace identifiers with their returned attributes. Covers Datadog. Assumes an authenticated Datadog API client with APM read permission for the selected site.
---

# Trace span query

Retrieve indexed trace spans for a supplied query and time interval.

## When to use this skill

Use for searching Datadog APM indexed spans and collecting span, parent and trace identifiers with their returned attributes.

## Universal concepts

No common wire protocol is implied by this capability. A query returns retained observable data, which may be incomplete. Span relationships and timestamps are evidence, not a universal root-cause verdict.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No service catalogue, trace waterfall completeness guarantee, service performance summary, or remediation is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Datadog API client with APM read permission for the selected site. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
