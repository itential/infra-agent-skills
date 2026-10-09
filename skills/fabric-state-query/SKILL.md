---
name: fabric-state-query
description: >-
  Retrieve EVPN/VXLAN fabric forwarding observations. Use for Nexus 9000 NVE/VNI, EVPN BGP, MAC/IP and Ethernet-segment state reads. Covers Cisco Nexus 9000 NX-OS 10.4 and 10.6 as scoped in the vendor procedure. Assumes an authenticated NX-OS CLI session on the selected fabric device.
---

# Fabric state query

Retrieve EVPN/VXLAN fabric forwarding observations.

## When to use this skill

Use for Nexus 9000 NVE/VNI, EVPN BGP, MAC/IP and Ethernet-segment state reads.

## Universal concepts

No common wire protocol is implied by this capability. An observation retains its device, address-family, VNI and forwarding context. A returned protocol or table state does not independently prove end-to-end application reachability.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No configuration, automatic remediation, universal health score, NetBox reconciliation or complete underlay diagnosis is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated NX-OS CLI session on the selected fabric device. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
