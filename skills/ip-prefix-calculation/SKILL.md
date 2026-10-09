---
name: ip-prefix-calculation
description: >-
  Calculate IPv4/IPv6 network boundaries, membership and subnet subdivisions. Use for CIDR validation, address counts, masks, containment/overlap and explicitly requested prefix splitting. Covers Python ipaddress. Assumes a Python 3 runtime with the standard-library ipaddress module.
---

# IP prefix calculation

Calculate IPv4/IPv6 network boundaries, membership and subnet subdivisions.

## When to use this skill

Use for CIDR validation, address counts, masks, containment/overlap and explicitly requested prefix splitting.

## Universal concepts

No common wire protocol is implied by this capability. Address-family and prefix length determine the network range. Arithmetic calculation does not allocate or configure an address.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No company addressing plan, IPAM reservation, device configuration, or universal usable-address subtraction is implied.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes a Python 3 runtime with the standard-library ipaddress module. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
