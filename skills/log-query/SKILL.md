---
name: log-query
description: >-
  Retrieve matching stored log events with their search scope and completeness. Use for read-only searches of retained logs. Covers Google Cloud Logging, Datadog, Elasticsearch, Splunk, Grafana Loki, AWS CloudWatch Logs, NetClaw syslog, and Fortinet FortiAnalyzer. Assumes an authenticated API/MCP client or console session for the selected log backend.
---

# Query stored logs

Retrieve matching stored log events with their search scope and completeness.

## When to use this skill

Use for read-only searches of retained logs. Supported platforms: Google Cloud Logging, Datadog, Elasticsearch, Splunk, Grafana Loki, AWS CloudWatch Logs, NetClaw syslog, and Fortinet FortiAnalyzer.

## Universal concepts

No common wire protocol is implied by this capability. Queries operate on the chosen store and filters. Returned events are evidence within that scope; time limits, result limits, and partial responses constrain conclusions.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This does not ingest logs, change retention, write saved searches, or infer an incident cause from a match alone.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API/MCP client or console session for the selected log backend. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
