---
name: network-path-measurement
description: >-
  Collect local traceroute or MTR observations for an explicit target. Use for gtrace local path tracing, repeated-hop measurements and requested MPLS/ECMP/NAT observations. Covers gtrace publisher MCP. Assumes an installed gtrace MCP client with the operating-system raw-socket privileges required for active tests.
---

# Network path measurement

Collect local traceroute or MTR observations for an explicit target.

## When to use this skill

Use for gtrace local path tracing, repeated-hop measurements and requested MPLS/ECMP/NAT observations.

## Universal concepts

No common wire protocol is implied by this capability. Probe responses describe the selected protocol and vantage point. Unanswered probes do not independently establish a failed forwarding device.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No automatic device configuration, universal loss threshold or proof of physical topology is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an installed gtrace MCP client with the operating-system raw-socket privileges required for active tests. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
