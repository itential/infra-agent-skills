---
name: network-access-diagnosis
description: >-
  Explain an observed network authentication or authorization result using platform evidence. Use for Cisco ISE session presence, applied posture/profile, matched policy, authentication failure and per-step latency investigations. Covers Cisco Identity Services Engine through its official MCP server. Assumes an authenticated ISE MCP client with MnT credentials and policy-read access.
---

# Network access diagnosis

Explain an observed network authentication or authorization result using platform evidence.

## When to use this skill

Use for Cisco ISE session presence, applied posture/profile, matched policy, authentication failure and per-step latency investigations.

This is diagnostic-shaped: the result is an evidence-backed finding from the documented decision tree, rather than a changed record.

## Universal concepts

No common wire protocol is implied by this capability. An absent result is bounded by the queried source, scope and retention window. A session outcome and a configured policy are distinct evidence.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No endpoint quarantine, policy edits, credential changes, or automatic risk classification are included. Counts and samples retain their documented coverage.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated ISE MCP client with MnT credentials and policy-read access. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
