---
name: network-access-policy-query
description: >-
  Read authentication and authorization policy configuration. Use for Cisco ISE RADIUS network-access policy sets, authentication rules, authorization rules and matching global exceptions. Covers Cisco Identity Services Engine through its official MCP server. Assumes an authenticated ISE MCP client with network-access policy-read permissions.
---

# Network access policy query

Read authentication and authorization policy configuration.

## When to use this skill

Use for Cisco ISE RADIUS network-access policy sets, authentication rules, authorization rules and matching global exceptions.

## Universal concepts

No common wire protocol is implied by this capability. Configured policy is evidence of intended matching behavior. Missing hit counts and partial result coverage do not justify deleting a rule or asserting that no policy exists.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure reads policy; it does not change access controls, test an end-to-end packet flow, or assess business compliance.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated ISE MCP client with network-access policy-read permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
