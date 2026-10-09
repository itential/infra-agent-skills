---
name: social-post-management
description: >-
  Read mentions and maintain explicitly supplied social posts. Use for retrieving X mentions and recent post context, publishing supplied text posts or replies, and deleting an explicitly selected own post. Covers X. Assumes an authenticated X API client with the required user-context read/write permissions.
---

# Social post management

Read mentions and maintain explicitly supplied social posts.

## When to use this skill

Use for retrieving X mentions and recent post context, publishing supplied text posts or replies, and deleting an explicitly selected own post.

## Universal concepts

No common wire protocol is implied by this capability. A post identifier is distinct from author identity. Publication is an external communication; successful creation does not imply audience engagement.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No persona-based content generation, spam judgment, automatic heartbeat, recurring polling, price/quota assumptions or media-upload workflow is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated X API client with the required user-context read/write permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
