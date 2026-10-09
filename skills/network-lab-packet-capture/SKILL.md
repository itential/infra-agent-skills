---
name: network-lab-packet-capture
description: >-
  Collect a packet capture from a selected network lab link. Use for starting and stopping link captures and retrieving the resulting PCAP. Covers GNS3 v2, Cisco CML. Assumes an authenticated API or supported SDK client for the target lab platform.
---

# Network lab packet capture

Collect a packet capture from a selected network lab link.

## When to use this skill

Use for starting and stopping link captures and retrieving the resulting PCAP.

## Universal concepts

No common wire protocol is implied by this capability. The link and capture scope must be identified. An empty capture is distinct from a failed download.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Packet interpretation, traffic generation, and production traffic capture are outside this capability.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API or supported SDK client for the target lab platform. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
