# Cloudflare analytics bindings

Sources: [Cloudflare API MCP](https://github.com/cloudflare/mcp/blob/main/README.md) and [publisher OpenAPI schema](https://github.com/cloudflare/api-schemas/blob/main/openapi.json), current main, retrieved 2026-10-09.

## Connection and discovery

The configured Cloudflare API MCP endpoint is `https://mcp.cloudflare.com/mcp`; OAuth or a scoped API token supplies authentication. The publisher currently does not support tokens with client-IP filtering on this MCP service. `whoami` takes no arguments. `search({code})` evaluates JavaScript against `spec.paths`; operation parameters, request bodies, security requirements and response schemas are inspected before invocation. `execute({code, account_id?})` evaluates an async JavaScript function using `cloudflare.request({method, path, body?, ...})`. The selected schema and deployed tool contract define optional request members. Single-account tokens can resolve account identity automatically; multi-account requests identify the account explicitly.

The paths below are literal Cloudflare API routes consumed by `cloudflare.request`; direct REST clients use `https://api.cloudflare.com/client/v4` as their base, except GraphQL uses its complete URL `https://api.cloudflare.com/client/v4/graphql` without adding the prefix twice. Query parameters are encoded according to the inspected operation. Most JSON reads return HTTP 200 with `success=true`, `result`, and any documented `result_info`; errors must be retained. A `--- TRUNCATED ---` marker means the MCP result was shortened and is incomplete. The publisher caps results by default; narrower queries or endpoint pagination avoid treating a truncated response as complete.

| Operation | Binding | Inputs / result |
|---|---|---|
| DNS aggregate | `GET /zones/{zone_id}/dns_analytics/report` | `metrics`, `dimensions`, `since`, `until`, `limit`, `sort`, `filters`; result `data`, `totals`, `data_lag`, `query`, `rows` |
| DNS time series | `GET /zones/{zone_id}/dns_analytics/report/bytime` | Same parameters plus `time_delta`; result adds `time_intervals` |
| Worker field keys / values | `POST /accounts/{account_id}/workers/observability/telemetry/keys`; `POST /accounts/{account_id}/workers/observability/telemetry/values` | Read-query body from current schema; values depend on selected field |
| Worker calculations | `POST /accounts/{account_id}/workers/observability/telemetry/query` | Required `queryId`, `timeframe` with `from`/`to` Unix milliseconds; ad-hoc `parameters`, `view=calculations`, `dry=true`; exact identifier contract from inspected schema |
| Zone daily HTTP totals | `POST /client/v4/graphql` via MCP | GraphQL `viewer.zones(filter: {zoneTag}).httpRequests1dGroups(limit, orderBy:[date_ASC])`; select `dimensions.date` and `sum.requests`, `sum.bytes`, `sum.cachedBytes`; a valid query uses the current GraphQL schema |
| Radar HTTP trend | `GET /radar/http/timeseries` | `dateRange` or `dateStart`/`dateEnd`; optional `asn`, `location`, `continent`, `aggInterval`, `normalization`, `format` |

The shown GraphQL binding retrieves bounded daily buckets. A requested date filter must be verified against the current dataset schema; no unverified filter field is supplied here. Returned dates define the actual reported window.

DNS metrics include `queryCount`, `uncachedCount`, `staleCount`, `responseTimeAvg`, `responseTimeMedian`, `responseTime90th`, `responseTime99th`; response times are milliseconds. ISO 8601 `since`/`until` specify its window. The publisher's DNS property guide defines filter operators and valid dimensions; deprecated API availability is not guaranteed.

Workers `timeframe.from` must precede `to`. `parameters` supplies calculations, filters and groupings from field discovery. Count accepts no key; other calculations use `key` and its `keyType`. `chartType=distribution` with `compare=true` is invalid. Documented failures include `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `429 Too many requests`; other returned errors remain visible. Radar returns its normalization and unit metadata; `normalization` accepts `PERCENTAGE_CHANGE` or `MIN0_MAX`.
