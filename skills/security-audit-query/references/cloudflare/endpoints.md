# Cloudflare security evidence bindings

Sources: [Cloudflare API MCP](https://github.com/cloudflare/mcp/blob/main/README.md) and [publisher OpenAPI schema](https://github.com/cloudflare/api-schemas/blob/main/openapi.json), current main, retrieved 2026-10-09.

## Connection and discovery

The configured Cloudflare API MCP endpoint is `https://mcp.cloudflare.com/mcp`; OAuth or a scoped API token supplies authentication. The publisher currently does not support tokens with client-IP filtering on this MCP service. `whoami` takes no arguments. `search({code})` evaluates JavaScript against `spec.paths`; operation parameters, request bodies, security requirements and response schemas are inspected before invocation. `execute({code, account_id?})` evaluates an async JavaScript function using `cloudflare.request({method, path, body?, ...})`. The selected schema and deployed tool contract define optional request members. Single-account tokens can resolve account identity automatically; multi-account requests identify the account explicitly.

The paths below are literal Cloudflare API routes consumed by `cloudflare.request`; direct REST clients use `https://api.cloudflare.com/client/v4` as their base. Query parameters are encoded according to the inspected operation. Most JSON reads return HTTP 200 with `success=true`, `result`, and any documented `result_info`; errors must be retained. A `--- TRUNCATED ---` marker means the MCP result was shortened and is incomplete. The publisher caps results by default; narrower queries or endpoint pagination avoid treating a truncated response as complete.

| Operation | Binding | Inputs / output |
|---|---|---|
| Audit events, including ID lookup | `GET /accounts/{account_id}/logs/audit` | Required `since`, `before`; optional `audit_log_id`, actor/action/resource filters, `direction`, `limit`, `cursor`; response `result_info.cursor` |
| Posture findings | `GET /accounts/{account_id}/data-security/posture/findings` | Optional `integration_id`, `severity`, `observation`, `vendor`, `search`, `ignored`, paging parameters from schema |
| Finding detail | `GET /accounts/{account_id}/data-security/posture/findings/{finding_id}` | Account/finding IDs; native detail and integration |
| IP overview | `GET /accounts/{account_id}/intel/ip` | Required address expressed as `ipv4` or `ipv6` query parameter |

Posture collection documents `400`, `401`, `403`; detail also documents `404`. Audit/IP APIs document their `4XX` envelope. Current posture severities are `Critical`, `High`, `Medium`, `Low`; these are platform values, not thresholds defined by this skill. Audit result count is schema-defined as a string; it is not assumed to be an integer. Exact filters and pagination members are inspected before use.
