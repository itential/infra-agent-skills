---
name: network-service-discovery
description: >-
  Discover hosts and scan explicitly selected ports or services within an approved target scope. Use for Nmap host discovery, TCP/UDP port scans, version/OS identification and explicitly selected NSE checks. Covers Nmap. Assumes Nmap is installed, required raw-packet privileges are available for the chosen scan, and target/port/script scope has operator approval.
---

# Network service discovery

Discover hosts and scan explicitly selected ports or services within an approved target scope.

## When to use this skill

Use for Nmap host discovery, TCP/UDP port scans, version/OS identification and explicitly selected NSE checks.

## Universal concepts

No common wire protocol is implied by this capability. Scanning describes observations from a particular vantage point. An unresolved or filtered result is not proof that a service is absent.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

The procedure does not provide a CIDR allowlist, bypass network controls, choose an arbitrary vulnerability campaign, or automatically authorize all scripts.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes Nmap is installed, required raw-packet privileges are available for the chosen scan, and target/port/script scope has operator approval. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
