---
name: voice-call-placement
description: >-
  Place and observe an explicitly requested outbound voice call. Use for calling a supplied recipient through Twilio Programmable Voice with supplied spoken content and monitoring native call status. Covers Twilio. Assumes an authenticated Twilio API client, authorized calling identity and any configured callback receiver.
---

# Voice call placement

Place and observe an explicitly requested outbound voice call.

## When to use this skill

Use for calling a supplied recipient through Twilio Programmable Voice with supplied spoken content and monitoring native call status.

## Universal concepts

No common wire protocol is implied by this capability. A created call resource records an attempt; platform terminal state is separate from a human acknowledging the content.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No recurring scheduler, emergency classification, quiet-hour policy, SMS fallback, or automatic redial is supplied.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Twilio API client, authorized calling identity and any configured callback receiver. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
