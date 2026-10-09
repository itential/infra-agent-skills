---
name: network-validation
description: >-
  Run a selected network test catalogue and preserve its native test results. Use for executing a supplied inventory and test catalogue to check network readiness or a requested state. Covers Arista EOS with ANTA. Assumes the ANTA CLI is installed and authenticated access to the selected EOS devices is available.
---

# Network validation

Run a selected network test catalogue and preserve its native test results.

## When to use this skill

Use for executing a supplied inventory and test catalogue to check network readiness or a requested state.

## Universal concepts

No common wire protocol is implied by this capability. A test result is meaningful only for the selected devices, tests, inputs, and run. Skipped or errored checks do not establish a passing result.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure does not invent acceptance thresholds or generate a business-specific test catalogue. Test support depends on the installed framework and device release.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes the ANTA CLI is installed and authenticated access to the selected EOS devices is available. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
