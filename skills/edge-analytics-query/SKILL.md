---
name: edge-analytics-query
description: >-
  Retrieve scoped DNS, HTTP, Worker and Internet traffic analytics. Use for Cloudflare DNS aggregate/time series and response-time metrics, zone HTTP daily aggregates, Worker analytics and Radar HTTP trends. Covers Cloudflare API MCP. Assumes an authorized Cloudflare API MCP client and the requested account, zone and time scope.
---

# Edge Analytics Query

Retrieve scoped DNS, HTTP, Worker and Internet traffic analytics.

## When to use this skill

Use for Cloudflare DNS aggregate/time series and response-time metrics, zone HTTP daily aggregates, Worker analytics and Radar HTTP trends.

## Universal concepts

No common wire protocol is implied by this capability. Time window, metric units and aggregation are part of the result. An aggregate does not identify an individual request.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

DNS Analytics is marked for future deprecation by the publisher. Retention and dataset access are platform-specific; no performance threshold or optimization policy is inferred.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authorized Cloudflare API MCP client and the requested account, zone and time scope. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
