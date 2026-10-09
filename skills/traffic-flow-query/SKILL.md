---
name: traffic-flow-query
description: >-
  Read observed transport flows and traffic summaries. Use for Kubeshark flow and handshake evidence, or retained NetClaw IPFIX decoded flows and template/statistic reads. Covers Kubeshark and NetClaw IPFIX. Assumes an authorized client to an existing Kubeshark Hub or NetClaw IPFIX receiver with retained data.
---

# Traffic flow query

Read observed transport flows and traffic summaries.

## When to use this skill

Use for Kubeshark flow and handshake evidence, or retained NetClaw IPFIX decoded flows and template/statistic reads. Supported platforms: Kubeshark and NetClaw IPFIX.

## Universal concepts

No common wire protocol is implied by this capability. Observed flows describe collected traffic, not all possible connections. Truncation and observation coverage affect completeness.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No packet-capture enablement, universal latency threshold, application-payload inspection or proof of root cause is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authorized client to an existing Kubeshark Hub or NetClaw IPFIX receiver with retained data. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
