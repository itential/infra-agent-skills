---
name: meeting-asset-query
description: >-
  Search historical meetings and retrieve their available recorded assets. Use for authorized Zoom meeting search, asset inventory, recording listing, and recording-resource retrieval. Covers Zoom Meetings MCP. Assumes an OAuth-authorized Zoom Meetings MCP client that can discover the server’s current tool schemas.
---

# Meeting asset query

Search historical meetings and retrieve their available recorded assets.

## When to use this skill

Use for authorized Zoom meeting search, asset inventory, recording listing, and recording-resource retrieval.

## Universal concepts

No common wire protocol is implied by this capability. Available results depend on the caller’s permissions and whether the meeting has the requested assets. A search hit is not proof that a particular historical event occurred.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Read-only; no live meeting interception, network correlation, meeting CRUD, bulk export, or NetClaw routing. Input/output schemas are discovered from the authenticated publisher server, not copied from a community wrapper.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an OAuth-authorized Zoom Meetings MCP client that can discover the server’s current tool schemas. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
