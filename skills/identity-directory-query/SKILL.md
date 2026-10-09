---
name: identity-directory-query
description: >-
  Retrieve directory identities, memberships and supported access metadata. Use for ZIdentity user/group and membership reads, or AWS IAM user/group/role metadata, policies and an existing credential report. Covers Zscaler ZIdentity and AWS IAM. Assumes an authenticated supported API/MCP client with the selected directory read permissions.
---

# Identity directory query

Retrieve directory identities, memberships and supported access metadata.

## When to use this skill

Use for ZIdentity user/group and membership reads, or AWS IAM user/group/role metadata, policies and an existing credential report. Supported platforms: Zscaler ZIdentity and AWS IAM.

## Universal concepts

No common wire protocol is implied by this capability. An identity is selected by a returned identifier. Partial name matches may identify several records; membership data belongs to the selected identity.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This skill does not create identities, change access, configure identity providers, or claim a complete directory from one page.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated supported API/MCP client with the selected directory read permissions. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
