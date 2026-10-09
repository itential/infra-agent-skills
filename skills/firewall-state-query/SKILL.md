---
name: firewall-state-query
description: >-
  Retrieve observed firewall device state. Use for FortiGate system, interfaces, IPv4 routes, HA and separate IPsec phase observations, or Panorama managed-firewall discovery and system information. Covers Fortinet FortiOS 7.6 CLI and Palo Alto Networks Panorama XML API. Assumes an authenticated vendor CLI or API client for the selected device and administrative scope.
---

# Firewall state query

Retrieve observed firewall device state.

## When to use this skill

Use for FortiGate system, interfaces, IPv4 routes, HA and separate IPsec phase observations, or Panorama managed-firewall discovery and system information.

## Universal concepts

No common wire protocol is implied by this capability. Device observations describe the responding device and query context. Unavailable observations are not substituted with intended controller configuration.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This read procedure does not compare FortiManager policy, alter tunnels, clear sessions or infer a universal root cause.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated vendor CLI or API client for the selected device and administrative scope. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
