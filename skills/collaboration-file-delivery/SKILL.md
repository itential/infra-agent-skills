---
name: collaboration-file-delivery
description: >-
  Upload and share an existing file in a collaboration conversation. Use for uploading an existing report, diagram, audio file or other permitted file to a Slack channel or thread. Covers Slack. Assumes an authenticated Slack API client with files:write and a resolved destination.
---

# Collaboration file delivery

Upload and share an existing file in a collaboration conversation.

## When to use this skill

Use for uploading an existing report, diagram, audio file or other permitted file to a Slack channel or thread.

## Universal concepts

No common wire protocol is implied by this capability. Uploading bytes and publishing a file are distinct completion states. Acceptance does not establish that a human opened the file.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No report authoring, speech synthesis, recurring delivery or automatic recipient selection is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Slack API client with files:write and a resolved destination. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
