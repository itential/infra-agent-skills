---
name: network-scan-comparison
description: >-
  Compare two saved network scan results. Use for Ndiff comparison of Nmap XML files for host/port state, service, OS and script-output differences. Covers Nmap Ndiff. Assumes Ndiff is installed and two authorized Nmap XML result files already exist.
---

# Network scan comparison

Compare two saved network scan results.

## When to use this skill

Use for Ndiff comparison of Nmap XML files for host/port state, service, OS and script-output differences.

## Universal concepts

No common wire protocol is implied by this capability. A difference describes the two observations; it does not establish the cause of a change. Comparable scan scope matters.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure does not rescan targets, modify infrastructure or provide NetClaw scan-ID storage.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes Ndiff is installed and two authorized Nmap XML result files already exist. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
