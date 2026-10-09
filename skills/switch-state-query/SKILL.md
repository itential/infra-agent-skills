---
name: switch-state-query
description: >-
  Read system, interface and VLAN state from a switch API. Use for collecting switch identity/software information, observed link state, VLAN records and documented related resources. Covers HPE Aruba Networking AOS-CX 10.13. Assumes an authenticated HTTPS REST client for the target switch and supported API version.
---

# Switch state query

Read system, interface and VLAN state from a switch API.

## When to use this skill

Use for collecting switch identity/software information, observed link state, VLAN records and documented related resources.

## Universal concepts

No common wire protocol is implied by this capability. Configured administrative state and observed operational state are separate evidence. A collection reference is not the same as a fully expanded record.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This skill does not change VLANs, save configuration, upgrade software, diagnose optical thresholds, or infer outage causes.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated HTTPS REST client for the target switch and supported API version. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
