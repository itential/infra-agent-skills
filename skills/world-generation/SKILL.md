---
name: world-generation
description: >-
  Create a generated 3D world from an explicitly supplied text prompt and retrieve its result. Use for World Labs Marble text-to-world submission and asynchronous result lookup. Covers World Labs World API. Assumes an authenticated World API client with an approved prompt/model and available API credits.
---

# World generation

Create a generated 3D world from an explicitly supplied text prompt and retrieve its result.

## When to use this skill

Use for World Labs Marble text-to-world submission and asynchronous result lookup.

## Universal concepts

No common wire protocol is implied by this capability. A generation job can be accepted and later fail. A generated scene is an artifact, not evidence of physical network geometry.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No topology discovery, factual diagram guarantee, image upload, credit purchase, permission widening or world deletion is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated World API client with an approved prompt/model and available API credits. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
