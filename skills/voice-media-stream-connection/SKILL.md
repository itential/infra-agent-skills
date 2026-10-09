---
name: voice-media-stream-connection
description: >-
  Connect an existing voice call to an authorized bidirectional media endpoint. Use for connecting Twilio Programmable Voice calls to a prepared WebSocket media server and observing the stream lifecycle. Covers Twilio. Assumes an existing Twilio voice application, a prepared authenticated callback handler and an authorized secure WebSocket server.
---

# Voice media stream connection

Connect an existing voice call to an authorized bidirectional media endpoint.

## When to use this skill

Use for connecting Twilio Programmable Voice calls to a prepared WebSocket media server and observing the stream lifecycle.

## Universal concepts

No common wire protocol is implied by this capability. Call media contains live conversation content. Stream connection and audio playback acknowledgements do not authorize downstream infrastructure changes.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This covers transport only, not transcription, agent reasoning, caller identity authentication, or network-command execution.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an existing Twilio voice application, a prepared authenticated callback handler and an authorized secure WebSocket server. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
