---
name: digital-experience-query
description: >-
  Retrieve application experience scores, trends and associated alert evidence. Use for reading a monitored application score or trend, or inspecting an ongoing experience alert and affected devices. Covers Zscaler ZDX. Assumes an authenticated Zscaler OneAPI MCP client with ZDX reporting and alert read tools enabled.
---

# Digital experience query

Retrieve application experience scores, trends and associated alert evidence.

## When to use this skill

Use for reading a monitored application score or trend, or inspecting an ongoing experience alert and affected devices.

## Universal concepts

No common wire protocol is implied by this capability. Experience observations belong to an application or alert, an observation interval and selected scope. A score alone does not identify the cause of degradation.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This skill does not start deep-trace capture, change monitoring, or infer an organization-specific severity from a numeric score.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Zscaler OneAPI MCP client with ZDX reporting and alert read tools enabled. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
