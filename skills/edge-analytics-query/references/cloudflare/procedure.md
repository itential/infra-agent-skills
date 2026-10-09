# Cloudflare analytics query

Cloudflare API MCP returns analytics for a specified product, scope and time window.

Sources: [Cloudflare API MCP](https://github.com/cloudflare/mcp/blob/main/README.md) and [publisher OpenAPI schema](https://github.com/cloudflare/api-schemas/blob/main/openapi.json), current main, retrieved 2026-10-09. DNS metric meanings also follow [Analytics API properties](https://developers.cloudflare.com/dns/reference/analytics-api-properties/), retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- DNS counts or latency: Discover metric contract → Query DNS aggregate or time series → Check completeness.
- Worker analytics: Discover metric contract → Discover Worker fields → Query Worker calculations → Check completeness.
- HTTP traffic: Discover metric contract → Query zone daily totals or Radar time series → Check completeness.

## Discover metric contract

Specification/documentation lookup identifies the operation, metric fields, scope, accepted time format and response. Success is a verified query contract. An unavailable dataset, expired retention window or permission failure remains explicit; there is no fallback to fabricated traffic. DNS response-time metrics use milliseconds. DNS totals and uncached/stale counts are counts, not percentages.

## Query DNS aggregate or time series

The selected query identifies the zone, metrics, dimensions, filters and time range. The aggregate result includes values, totals, query context and data lag. The time-series result adds time intervals. Success requires the successful envelope and the requested metric ordering; metric values are associated with that ordering. A query/permission error is reported through its native error envelope. The publisher announces future deprecation of this DNS API; if removed, this binding stops pending a documented replacement.

## Discover Worker fields

The field-key and field-value reads identify the available telemetry fields and valid filter values for the selected time scope. Successful discovery prevents assuming a custom log field exists. Unknown fields are corrected against those results before constructing calculations.

## Query Worker calculations

A temporary, nonpersisting query selects the Worker through discovered fields, a millisecond time window, calculations and any groupings. Success returns calculations in the query result with the native successful envelope. The source requires a query identifier even for an ad-hoc query; its current schema determines that value. Count may omit a field; other calculations require an existing field and its documented type. Invalid requests are corrected from the validation detail; unauthorized or forbidden responses require appropriate access. Rate limiting follows returned guidance without an invented fixed retry schedule. Unsupported chart/compare combinations are not retried unchanged.

## Query zone daily totals or Radar time series

Zone daily HTTP analytics use the publisher's documented GraphQL dataset and retain date, requests, bytes and cached bytes for the selected zone. GraphQL errors remain failures even if the transport response succeeds. The resulting daily aggregates are distinct from request logs.

Radar returns an Internet-level HTTP time series with its own normalization, units, confidence and update metadata. Success retains those properties and the requested geography/ASN/time filters. A normalized Radar series is not a count of requests to the operator's own zone. Invalid input follows the returned validation detail.

## Check completeness

Returned limits, data lag, sampling/normalization metadata and any truncation marker remain visible. An API-success response with truncated MCP output is incomplete. The result states the actual window and metrics rather than implying full historical coverage.

## Patterns

Workers telemetry and Radar use different time formats. A missing field is not zero. DNS time-series intervals and metric arrays are paired using the returned query context.

## Known limitations

This procedure does not search firewall events or HTTP request logs, submit URL scans, tune edge settings or make remediation decisions. The zone HTTP binding is specifically the documented daily dataset, not every GraphQL dataset.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Discover metric contract | Resolve API/dataset schema | Read |
| Query DNS analytics | Retrieve aggregate or time-grouped metrics | Read |
| Discover Worker fields / Query calculations | Retrieve scoped Worker telemetry | Read |
| Query zone totals / Radar series | Retrieve daily zone or global traffic aggregates | Read |

## Verification checklist

- Product, account/zone, time range, units and dimensions match the request.
- Worker fields and query parameters match the current schema.
- Errors, data lag, normalization and truncated output remain visible.
- Aggregate and global data are not described as individual zone requests.
