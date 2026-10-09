---
name: traffic-snapshot-management
description: >-
  Create, inspect, export and remove a retained traffic snapshot. Use for Kubeshark raw-capture snapshot lifecycle and filtered PCAP export. Covers Kubeshark. Assumes authorized API access to an existing Kubeshark Hub with raw capture already enabled.
---

# Traffic snapshot management

Create, inspect, export and remove a retained traffic snapshot.

## When to use this skill

Use for Kubeshark raw-capture snapshot lifecycle and filtered PCAP export.

## Universal concepts

No common wire protocol is implied by this capability. A snapshot covers retained observations over a selected interval. Creation acceptance and completed artifact availability are different states.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Raw-capture installation/enablement, TLS-decryption guarantees, cloud upload and delayed indexing are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes authorized API access to an existing Kubeshark Hub with raw capture already enabled. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
