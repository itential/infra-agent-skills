---
name: collaboration-context-query
description: >-
  Retrieve visible collaboration profiles and conversation evidence. Use for reading Slack user profiles, presence and Do Not Disturb state, listing conversations, retrieving history/threads and searching visible messages. Covers Slack. Assumes an authenticated Slack API client with the relevant read scopes and token type.
---

# Collaboration context query

Retrieve visible collaboration profiles and conversation evidence.

## When to use this skill

Use for reading Slack user profiles, presence and Do Not Disturb state, listing conversations, retrieving history/threads and searching visible messages.

## Universal concepts

No common wire protocol is implied by this capability. Visibility depends on the caller. Presence, profile text and message history do not establish on-call responsibility or permission to contact a person.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Read-only Slack operations; no escalation policy, persona adjustment, DND override or presence mutation is supplied.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Slack API client with the relevant read scopes and token type. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
