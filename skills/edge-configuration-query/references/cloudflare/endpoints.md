# Cloudflare configuration bindings

Sources: [Cloudflare API MCP](https://github.com/cloudflare/mcp/blob/main/README.md) and [publisher OpenAPI schema](https://github.com/cloudflare/api-schemas/blob/main/openapi.json), current main, retrieved 2026-10-09.

## Connection and discovery

The configured Cloudflare API MCP endpoint is `https://mcp.cloudflare.com/mcp`; OAuth or a scoped API token supplies authentication. The publisher currently does not support tokens with client-IP filtering on this MCP service. `whoami` takes no arguments. `search({code})` evaluates JavaScript against `spec.paths`; operation parameters, request bodies, security requirements and response schemas are inspected before invocation. `execute({code, account_id?})` evaluates an async JavaScript function using `cloudflare.request({method, path, body?, ...})`. The selected schema and deployed tool contract define optional request members. Single-account tokens can resolve account identity automatically; multi-account requests identify the account explicitly.

The paths below are literal Cloudflare API routes consumed by `cloudflare.request`; direct REST clients use `https://api.cloudflare.com/client/v4` as their base. Query parameters are encoded according to the inspected operation. Most JSON reads return HTTP 200 with `success=true`, `result`, and any documented `result_info`; errors must be retained. A `--- TRUNCATED ---` marker means the MCP result was shortened and is incomplete. The publisher caps results by default; narrower queries or endpoint pagination avoid treating a truncated response as complete.

| Read operation | Binding | Required scope / result detail |
|---|---|---|
| Zones / Zone | `GET /zones`; `GET /zones/{zone_id}` | Zone list filters include account and name; detail uses zone ID |
| DNS records | `GET /zones/{zone_id}/dns_records` | Zone ID; documented record filters and paging |
| Workers | `GET /accounts/{account_id}/workers/scripts` | Account ID; script collection |
| Worker settings | `GET /accounts/{account_id}/workers/scripts/{script_name}/settings` | Script name; result includes bindings and compatibility settings |
| Worker versions | `GET /accounts/{account_id}/workers/scripts/{script_name}/versions` | Optional `page`, `per_page`, `deployable`; result items |
| Builds by version | `GET /accounts/{account_id}/builds/builds` | Required query `version_ids` in the current schema |
| Build detail | `GET /accounts/{account_id}/builds/builds/{build_uuid}` | Build UUID; native `status` and `build_outcome` |
| Access applications / Application | `GET /accounts/{account_id}/access/apps`; `GET /accounts/{account_id}/access/apps/{app_id}` | Account/application IDs |
| Application policies / Policy | `GET /accounts/{account_id}/access/apps/{app_id}/policies`; `GET /accounts/{account_id}/access/apps/{app_id}/policies/{policy_id}` | Account, application and policy IDs |
| Tunnels / Tunnel | `GET /accounts/{account_id}/cfd_tunnel`; `GET /accounts/{account_id}/cfd_tunnel/{tunnel_id}` | `status` filter: `inactive`, `degraded`, `healthy`, `down`; list uses `page`, `per_page` |
| Tunnel connections | `GET /accounts/{account_id}/cfd_tunnel/{tunnel_id}/connections` | Account/tunnel IDs |
| Zone rulesets / Ruleset | `GET /zones/{zone_id}/rulesets`; `GET /zones/{zone_id}/rulesets/{ruleset_id}` | Zone/ruleset IDs; detail includes rules |

Build detail documents `401` and `404`; most configuration APIs document their JSON `4XX` failure envelope. The read contract supplies resource-specific error codes instead of assuming one universal list. Build outcomes include `success`, `fail`, `skipped`, `cancelled`, `terminated`.
