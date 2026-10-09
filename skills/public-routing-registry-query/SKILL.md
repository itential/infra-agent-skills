---
name: public-routing-registry-query
description: >-
  Read public routing, registration, peering and measurement-infrastructure evidence. Use for ASN or prefix registration and routing observations, RPKI validation, peering presence and Atlas probe/anchor inventory. Covers RIPEstat, PeeringDB and RIPE Atlas. Assumes an HTTPS API client; PeeringDB authentication is needed for restricted data.
---

# Public Routing Registry Query

Read public routing, registration, peering and measurement-infrastructure evidence.

## When to use this skill

Use for ASN or prefix registration and routing observations, RPKI validation, peering presence and Atlas probe/anchor inventory.

## Universal concepts

No common wire protocol is implied by this capability. Registration, observed routing and measurement-node inventory are different evidence sources. Their returned identity, timestamps and scope must remain visible.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No route changes, active measurement creation, abuse reporting, peering recommendation or incident attribution is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an HTTPS API client; PeeringDB authentication is needed for restricted data. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
