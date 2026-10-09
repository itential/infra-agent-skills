---
name: metric-query
description: >-
  Retrieve scoped metric samples and their collection metadata. Use for read-only instant or historical metric queries, result interpretation, and discovery where the selected platform procedure supports it. Covers Prometheus, Zabbix, Google Cloud Monitoring, Datadog, Auvik, Grafana Prometheus, AWS CloudWatch, and Docker. Assumes the selected authenticated API/MCP client or authorized Docker CLI is available.
---

# Query metric history

Retrieve scoped metric samples and their collection metadata.

## When to use this skill

Use for read-only instant or historical metric queries, result interpretation, and discovery where the selected platform procedure supports it. Supported platforms: Prometheus, Zabbix, Google Cloud Monitoring, Datadog, Auvik, Grafana Prometheus, AWS CloudWatch, and Docker.

## Universal concepts

No common wire protocol is implied by this capability. A query identifies a source and the available collection or time scope. Units, timestamps, aggregation and incomplete results retain their platform meaning. Empty data does not establish infrastructure health.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This retrieves observations; it does not set alert thresholds, predict capacity, or change monitoring configuration.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes the selected authenticated API/MCP client or authorized Docker CLI is available. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
