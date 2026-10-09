---
name: oncall-schedule-management
description: >-
  On-call schedule management. Use for querying PagerDuty on-call entries and escalation policies, and creating, updating or overriding legacy V2 schedules. Covers PagerDuty. Assumes an authenticated PagerDuty REST API client with the operation-specific permissions.
---

# On-call schedule management

On-call schedule management.

## When to use this skill

Use for querying PagerDuty on-call entries and escalation policies, and creating, updating or overriding legacy V2 schedules.

## Universal concepts

No common wire protocol is implied by this capability. Coverage is evaluated for an explicit interval and time zone. A schedule and an escalation policy are separate resources.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Only legacy V2 layered schedules are covered; V3 shift-based schedules require a different procedure.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated PagerDuty REST API client with the operation-specific permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
