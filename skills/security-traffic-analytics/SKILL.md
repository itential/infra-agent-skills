---
name: security-traffic-analytics
description: >-
  Retrieve a bounded historical traffic or threat aggregate. Use for reading historical traffic totals, location breakdowns, protocol mix, or threat category/class aggregates. Covers Zscaler Z-Insights. Assumes an authenticated Zscaler OneAPI MCP client with Z-Insights web-traffic tools enabled.
---

# Security traffic analytics

Retrieve a bounded historical traffic or threat aggregate.

## When to use this skill

Use for reading historical traffic totals, location breakdowns, protocol mix, or threat category/class aggregates.

## Universal concepts

No common wire protocol is implied by this capability. Aggregate values belong to a stated measurement unit, grouping, filters and time interval. A total is not an individual event record.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This skill does not provide live incident feeds, file sandbox reports, IP reputation, or a universal organizational risk score.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Zscaler OneAPI MCP client with Z-Insights web-traffic tools enabled. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
