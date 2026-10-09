---
name: source-of-truth-query
description: >-
  Retrieve scoped infrastructure records from a source of truth. Use for NetBox device, interface, cable, site, IP address, prefix and VLAN reads, or Nautobot IP address and prefix reads/searches. Covers NetBox and Nautobot. Assumes an authenticated REST client for the selected instance.
---

# Source of Truth Query

Retrieve scoped infrastructure records from a source of truth.

## When to use this skill

Use for NetBox device, interface, cable, site, IP address, prefix and VLAN reads, or Nautobot IP address and prefix reads/searches.

## Universal concepts

No common wire protocol is implied by this capability. A stored inventory record describes the platform model; it is not a live observation of a device. Collection paging and object identity must be retained.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This capability does not reconcile live state, rank drift, modify records or open change tickets.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated REST client for the selected instance. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
