---
name: telemetry-receiver-management
description: >-
  Start, inspect or stop a selected telemetry receiver. Use for NetClaw syslog, SNMP trap or IPFIX/NetFlow listener lifecycle. Covers NetClaw publisher receiver servers. Assumes an installed authorized receiver MCP server and an operator-selected bind address/port.
---

# Telemetry receiver management

Start, inspect or stop a selected telemetry receiver.

## When to use this skill

Use for NetClaw syslog, SNMP trap or IPFIX/NetFlow listener lifecycle.

## Universal concepts

No common wire protocol is implied by this capability. A running listener and successful data collection are different states. Stopping collection can lose observations.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No device exporter configuration, automatic public exposure, complete telemetry guarantee or agent audit-policy setup is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an installed authorized receiver MCP server and an operator-selected bind address/port. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
