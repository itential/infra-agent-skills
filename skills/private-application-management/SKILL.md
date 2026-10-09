---
name: private-application-management
description: >-
  Read, create, update, or delete a private application segment. Use for Zscaler ZPA standard application segment records, their existing group references and port/domain scope. Covers Zscaler Private Access through the publisher MCP server. Assumes an authenticated Zscaler MCP client with the required read tools and explicitly enabled write tools.
---

# Private application management

Read, create, update, or delete a private application segment.

## When to use this skill

Use for Zscaler ZPA standard application segment records, their existing group references and port/domain scope.

## Universal concepts

No common wire protocol is implied by this capability. The requested application scope and existing group identifiers determine the object being managed. Record persistence alone does not establish successful end-user connectivity.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure covers standard segments, not Browser Access/PRA segments, access policies, connector provisioning, or group lifecycle.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Zscaler MCP client with the required read tools and explicitly enabled write tools. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
