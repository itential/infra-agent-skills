---
name: incident-record-management
description: >-
  Create, inspect, and update incident records using the selected platform. Use for PagerDuty incident lifecycle, alert reads, note retrieval/creation, responder requests and incident merges, or Datadog incident list/detail/create/update operations. Covers PagerDuty and Datadog. Assumes an authenticated platform API client with operation-specific permissions.
---

# Incident record management

Create, inspect, and update incident records using the selected platform.

## When to use this skill

Use for PagerDuty incident lifecycle, alert reads, note retrieval/creation, responder requests and incident merges, or Datadog incident list/detail/create/update operations. Supported platforms: PagerDuty and Datadog.

## Universal concepts

No common wire protocol is implied by this capability. An incident record has platform-defined identity and state. Record resolution does not independently prove that infrastructure recovered.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No organizational severity thresholds, escalation decisions, or infrastructure remediation are supplied. Each platform reference defines supported operations.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated platform API client with operation-specific permissions. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
