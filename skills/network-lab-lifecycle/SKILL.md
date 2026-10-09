---
name: network-lab-lifecycle
description: >-
  Create, inspect, start or stop, copy, and remove a network laboratory using the selected platform. Use for lab or project lifecycle operations, with each platform’s supported copy and import/export modes. Covers GNS3 v2, Cisco CML, EVE-NG, and Containerlab. Assumes an authenticated lab API/SDK client or authorized Containerlab CLI and an approved supplied topology.
---

# Network lab lifecycle

Create, inspect, start or stop, copy, and remove a network laboratory using the selected platform.

## When to use this skill

Use for lab or project lifecycle operations, with each platform’s supported copy and import/export modes. Supported platforms: GNS3 v2, Cisco CML, EVE-NG, and Containerlab.

## Universal concepts

No common wire protocol is implied by this capability. A laboratory contains platform-owned simulation resources. Lifecycle state and operation completion are different observations.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Only operations explicitly listed in the platform procedure are covered. Lab lifecycle does not establish guest protocol convergence.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated lab API/SDK client or authorized Containerlab CLI and an approved supplied topology. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
