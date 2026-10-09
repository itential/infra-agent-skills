---
name: firewall-rule-query
description: >-
  Read scoped policy rules and search their network or identity references. Use for read-only rule inspection within an explicit policy, device assignment, or management domain. Covers Cisco Secure Firewall FMC and Check Point Quantum Management. Assumes an authenticated publisher MCP connector and authorized access to the requested management domain.
---

# Firewall rule query

Read scoped policy rules and search their network or identity references.

## When to use this skill

Use for read-only rule inspection within an explicit policy, device assignment, or management domain.

## Universal concepts

No common wire protocol is implied by this capability. Rule search is evidence about configured policy objects and their references. A matching rule does not by itself establish the observed result of a live packet flow.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure does not create, reorder, deploy, or delete rules, and does not infer effective reachability from a search match.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated publisher MCP connector and authorized access to the requested management domain. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
