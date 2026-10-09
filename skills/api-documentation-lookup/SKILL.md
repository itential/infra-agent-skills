---
name: api-documentation-lookup
description: >-
  Retrieve publisher API documentation for a requested operation. Use for Cisco Meraki and Catalyst Center API keyword searches, and exact Meraki operation-ID lookup. Covers Cisco DevNet Content Search MCP. Assumes an authenticated Cisco DevNet Content Search MCP client.
---

# API documentation lookup

Retrieve publisher API documentation for a requested operation.

## When to use this skill

Use for Cisco Meraki and Catalyst Center API keyword searches, and exact Meraki operation-ID lookup.

## Universal concepts

No common wire protocol is implied by this capability. A search result is documentation evidence, not execution of the documented operation. Product, operation identifier and API version bound the applicability of returned material.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure retrieves documentation only; it does not authenticate to a network controller or execute a returned API operation.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Cisco DevNet Content Search MCP client. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
