# Globalping public-target measurement: bindings

API base: `https://api.globalping.io`. Optional authentication uses a Bearer token through the existing client. Non-browser clients identify themselves with User-Agent and use supported compressed responses.

| Operation | Binding | Request/result |
|---|---|---|
| Probe inventory | `GET /v1/probes` | Currently online probes and metadata |
| Limits | `GET /v1/limits` | Current user/IP allowance |
| Create | `POST /v1/measurements` | JSON `type`, `target`, optional `locations`, `limit`, `measurementOptions`, `timeout`, `inProgressUpdates`; 202 plus ID and Location |
| Retrieve | `GET /v1/measurements/{id}` | `status`, `probesCount`, `results`; conditional `If-None-Match` supported |

Types: `ping`, `traceroute`, `mtr`, `dns`, `http`. Native running state is `in-progress` (hyphen), final current enum `finished`. Locations accept an array of location objects or a prior measurement ID. Location fields include `country`, `city`, `asn`, `network`, `tags`, `magic`; `+` combines fuzzy conditions with AND. Global `limit` and location `limit` are mutually exclusive.

Ping options include `packets`, `protocol`, `port`, `ipVersion`; DNS uses `query.type`, `resolver`, `protocol`, `port`, `trace`; HTTP uses `request.method`, `request.path`, `request.query`, optional headers, protocol/port/resolver. Option enums and bounds are those of the selected type in the cited OpenAPI schema, not MCP-wrapper parameter names. The probe-side `timeout` range is 5–30 seconds; publisher clients allow at least ten additional seconds for communication/finalization.

Errors: 400 invalid input; 422 unsuitable probe selection; 429 quota/credit/polling limit; 404 unknown result ID. `error.type` values documented include `rate_limit_exceeded`, `insufficient_credits`, `too_many_requests`, `not_found`. A polling 429 supplies `Retry-After`. Per-test `failureSource` may be `target`, `resolver`, `internal` and is experimental. Secrets are not measurement headers or report values.

## Sources

- [Globalping OpenAPI 1.0.0](https://api.globalping.io/v1/spec.yaml). Retrieved 2026-10-09.
