---
name: offline-packet-analysis
description: >-
  Inspect an existing packet capture and return decoded traffic, session or signature evidence. Use for offline packet decoding, protocol/conversation summaries, session pivots and IDS signature review. Covers Wireshark TShark, Zeek, Suricata. Assumes the selected analyzer is installed and an authorized local capture plus any required rules/configuration are available.
---

# Offline packet analysis

Inspect an existing packet capture and return decoded traffic, session or signature evidence.

## When to use this skill

Use for offline packet decoding, protocol/conversation summaries, session pivots and IDS signature review.

## Universal concepts

No common wire protocol is implied by this capability. The result describes traffic visible in the input capture under the analyzer’s configuration. Missing evidence is not proof that activity never occurred.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This capability does not capture live traffic, change a sensor, block traffic or declare a compromise. Analyzer output and limitations remain platform-specific.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes the selected analyzer is installed and an authorized local capture plus any required rules/configuration are available. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
