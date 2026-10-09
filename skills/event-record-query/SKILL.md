---
name: event-record-query
description: >-
  Read stored protocol-event records and native counts. Use for NetClaw SNMP trap queries, exact-record details and type/source counts. Covers NetClaw SNMP trap receiver. Assumes an existing receiver MCP connection with an initialized local store.
---

# Event record query

Read stored protocol-event records and native counts.

## When to use this skill

Use for NetClaw SNMP trap queries, exact-record details and type/source counts.

## Universal concepts

No common wire protocol is implied by this capability. Collected events describe received records, not a complete inventory of events that occurred.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No trap remediation, SNMPv3 authenticated decoding, device reconfiguration or automatic severity inference is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an existing receiver MCP connection with an initialized local store. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
