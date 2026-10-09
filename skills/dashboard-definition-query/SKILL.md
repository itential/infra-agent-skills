---
name: dashboard-definition-query
description: >-
  Find dashboards and read their definitions, summaries and panel queries. Use for Grafana dashboard discovery and inspection by UID. Covers Grafana publisher MCP server. Assumes an authenticated Grafana MCP client with dashboard and folder read permissions.
---

# Dashboard definition query

Find dashboards and read their definitions, summaries and panel queries.

## When to use this skill

Use for Grafana dashboard discovery and inspection by UID.

## Universal concepts

No common wire protocol is implied by this capability. A dashboard definition describes visualization/query configuration; reading it does not execute its queries or establish current service health.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No dashboard writes, alert edits, annotation delivery or automatic incident creation is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Grafana MCP client with dashboard and folder read permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
