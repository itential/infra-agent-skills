---
name: ip-address-enrichment
description: >-
  Retrieve ASN, geolocation and reverse-DNS metadata for an IP address. Use for gtrace lookup of IPv4/IPv6 registry/network, geographic and PTR context. Covers gtrace publisher MCP. Assumes an installed gtrace MCP client and network access to its lookup providers/resolver.
---

# IP address enrichment

Retrieve ASN, geolocation and reverse-DNS metadata for an IP address.

## When to use this skill

Use for gtrace lookup of IPv4/IPv6 registry/network, geographic and PTR context.

## Universal concepts

No common wire protocol is implied by this capability. Lookup metadata is distinct from live device state. Missing metadata does not prove that an address is unused.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No ownership verification, precise physical-location guarantee, maliciousness score or active reachability test is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an installed gtrace MCP client and network access to its lookup providers/resolver. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
