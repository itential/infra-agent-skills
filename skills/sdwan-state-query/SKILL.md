---
name: sdwan-state-query
description: >-
  Retrieve scoped SD-WAN inventory, configuration, topology, or recorded state. Use for reading tenant sites and devices, their configuration and status, application definitions, or bounded event/topology queries. Covers Palo Alto Networks Prisma SD-WAN Unified SASE API and Cisco Catalyst SD-WAN Manager through the publisher MCP server. Assumes an authenticated platform API or MCP client with the required read permissions.
---

# SD-WAN state query

Retrieve scoped SD-WAN inventory, configuration, topology, or recorded state.

## When to use this skill

Use for reading tenant sites and devices, their configuration and status, application definitions, or bounded event/topology queries.

## Universal concepts

No common wire protocol is implied by this capability. Identifiers establish tenant, site and device scope. A configuration record, operational observation and event are different evidence types.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This skill reads existing state; it does not deploy policy, upgrade software, or derive a universal health or application-risk judgment.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated platform API or MCP client with the required read permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
