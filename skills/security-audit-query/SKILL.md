---
name: security-audit-query
description: >-
  Read security audit events, posture findings and indicator intelligence. Use for Cloudflare account audit events, posture findings and IP intelligence, or AWS CloudTrail regional event history. Covers Cloudflare API MCP and AWS CloudTrail. Assumes an authenticated API/MCP client with the selected account and regional read permissions.
---

# Security Audit Query

Read security audit events, posture findings and indicator intelligence.

## When to use this skill

Use for Cloudflare account audit events, posture findings and IP intelligence, or AWS CloudTrail regional event history. Supported platforms: Cloudflare API MCP and AWS CloudTrail.

## Universal concepts

No common wire protocol is implied by this capability. Platform findings and categories are retained as returned. A successful lookup is distinct from a clean security assessment.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No remediations, finding-state changes or universal security scores are generated. Firewall event querying is outside this version.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API/MCP client with the selected account and regional read permissions. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
