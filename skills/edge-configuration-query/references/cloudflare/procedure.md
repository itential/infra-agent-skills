# Cloudflare configured-service query

Cloudflare API MCP discovers and executes documented reads for the selected edge-service resource.

Sources: [Cloudflare API MCP](https://github.com/cloudflare/mcp/blob/main/README.md) and [publisher OpenAPI schema](https://github.com/cloudflare/api-schemas/blob/main/openapi.json), current main, retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Configuration lookup: Identify scope → Inspect read contract → List records → Read selected record.
- Worker build inspection: Identify scope → Inspect read contract → List Workers → Read Worker settings → List Worker versions → List builds for selected versions → Read selected build.
- Tunnel connection inspection: Identify scope → Inspect read contract → List tunnels → Read selected tunnel → Read tunnel connections.

## Identify scope

The connection identity and requested account or zone determine the target. A zone list can identify the requested zone within that account. More than one match is not silently reduced to the first. Authentication or scope ambiguity prevents the data query; it does not produce an empty result.

## Inspect read contract

The API-specification search resolves the exact read operation from the companion table, including required identifiers, filters, paging and response fields. Successful discovery returns that contract. Missing permission, an unavailable endpoint or an incompatible schema is reported explicitly. The current recommended MCP supersedes the source's deprecated domain-server bindings.

## List records

The selected collection read returns records and its pagination metadata. Success requires the operation's successful response and complete paging for an all-records request. A truncation marker means incomplete output even when JSON remains parseable. Empty successful data is a valid empty result. Query errors retain their native details; narrowed filters or corrected input follow the documented contract, not guessed fields.

## Read selected record

A detail read uses the identifier obtained from the list or supplied by the operator. Success returns that record's identity and selected fields. DNS records remain configuration data; this does not perform a DNS resolution test. Ruleset detail returns its rules, and does not evaluate a hypothetical packet. Access applications and policies describe configured access controls, not an access-decision simulation. A missing object is reported as absent; permission errors do not mean absence.

## List Workers / Read Worker settings / List Worker versions

Worker discovery identifies script names. Settings reads return settings including bindings; version reads identify the versions used in the subsequent build lookup. Success retains the account and script identity for each result. Configuration and build metadata can contain sensitive application data; the requested fields are reported without copying credential-bearing values. A settings response is not a new deployment.

## List builds for selected versions / Read selected build

Build lookup uses the selected Worker version identifiers; the current API does not accept an invented script-name parameter on that operation. Detail reads identify the build by UUID and retain native status and outcome. A not-found build remains absent; unauthorized access requires the configured credential and scope to be checked. A successful query can return a failed, skipped, cancelled or terminated build; retrieval success does not change its outcome.

## List tunnels / Read selected tunnel / Read tunnel connections

Tunnel discovery and detail reads retain tunnel identity and the native inactive, degraded, healthy or down status. The connections read supplies the tunnel's recorded connectors. Success means the requested records were retrieved. It does not demonstrate application reachability through the tunnel. An unsuccessful read follows the operation's error schema.

## Patterns

The installed API specification is the binding authority. Source wrapper names, guessed server hosts and broad permission labels are not API contracts. Collection continuation differs by resource and follows the selected operation's metadata.

## Known limitations

No write operation is in scope, even when the general-purpose client can expose it. Service subscriptions and credential permissions determine availability. The source's WAF label is represented here by current rulesets; deprecated firewall-rule APIs are not presumed equivalent.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Identify scope / Inspect read contract | Identify account and exact API schema | Read |
| List records / Read selected record | Retrieve configuration collections/details | Read |
| Worker versions / Build reads | Retrieve Worker build evidence | Read |
| Tunnel connections | Retrieve recorded connection state | Read |

## Verification checklist

- Account/zone and identifiers match the request.
- Every operation is a documented read with valid parameters.
- Pagination and MCP truncation are accounted for.
- Native build and tunnel states are retained independently of query success.
