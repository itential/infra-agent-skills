---
name: monitoring-problem-query
description: >-
  Retrieve current or historical monitoring problems and their evidence. Use for read-only review of platform problem, alert or alarm records and available state/history evidence. Covers Zabbix, Auvik, and AWS CloudWatch. Assumes an authenticated API client for the selected monitoring platform.
---

# Query monitoring problems

Retrieve current or historical monitoring problems and their evidence.

## When to use this skill

Use for read-only review of platform problem, alert or alarm records and available state/history evidence. Supported platforms: Zabbix, Auvik, and AWS CloudWatch.

## Universal concepts

No common wire protocol is implied by this capability. Monitoring records describe the selected platform and scope. A reported alert state does not independently establish infrastructure recovery; an empty read differs from a failed read.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This does not acknowledge, suppress, close, or repair problems, or choose a business escalation policy.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API client for the selected monitoring platform. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
