---
name: incident-service-management
description: >-
  Incident service management. Use for listing, inspecting, creating and updating PagerDuty incident services. Covers PagerDuty. Assumes an authenticated PagerDuty REST API client with the operation-specific permissions.
---

# Incident service management

Incident service management.

## When to use this skill

Use for listing, inspecting, creating and updating PagerDuty incident services.

## Universal concepts

No common wire protocol is implied by this capability. A service associates incident handling with a platform escalation policy. Its status has vendor-defined meaning.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Core service properties only; integration provisioning and deprecated alert grouping settings are excluded.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated PagerDuty REST API client with the operation-specific permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
