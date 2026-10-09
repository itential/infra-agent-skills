---
name: address-service-query
description: >-
  Read bounded DNS, DHCP and address-inventory record collections. Use for inspection of DNS A/AAAA/CNAME/PTR/TXT records, IPv4 networks, DHCP ranges and fixed addresses. Covers Infoblox NIOS WAPI. Assumes an authenticated HTTPS WAPI client and verified target protocol version.
---

# Address Service Query

Read bounded DNS, DHCP and address-inventory record collections.

## When to use this skill

Use for inspection of DNS A/AAAA/CNAME/PTR/TXT records, IPv4 networks, DHCP ranges and fixed addresses.

## Universal concepts

No common wire protocol is implied by this capability. Stored records describe configured address services; they do not establish successful live resolution or client lease delivery. Bounded collections retain their coverage limit.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Read-only collection inspection. No allocation, mutation, full-inventory completion, lease history, DNS zone administration or cross-platform reconciliation.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated HTTPS WAPI client and verified target protocol version. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
