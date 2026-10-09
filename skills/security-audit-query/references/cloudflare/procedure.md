# Cloudflare security evidence query

Cloudflare API MCP retrieves account audit records, posture findings or an IP intelligence overview.

Sources: [Cloudflare API MCP](https://github.com/cloudflare/mcp/blob/main/README.md) and [publisher OpenAPI schema](https://github.com/cloudflare/api-schemas/blob/main/openapi.json), current main, retrieved 2026-10-09. The publisher's [audit migration reference](https://github.com/cloudflare/mcp-server-cloudflare/blob/main/apps/auditlogs/README.md) identifies Audit Logs v2 as the replacement. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Audit history: Discover contract → Query audit window → Continue audit cursor.
- Finding inspection: Discover contract → List posture findings → Read finding detail.
- IP lookup: Discover contract → Query IP overview.

## Discover contract

The API specification identifies the selected operation's permissions, filters and response. Success resolves its current contract under the requested account. A missing permission or unavailable product remains explicit. The legacy CASB MCP's current catalogue covers integrations/assets, so this procedure uses the native data-security posture API for findings instead of assuming old wrapper tool names.

## Query audit window

The audit query supplies both time bounds and any documented actor, action, resource or identifier filter. Success returns the matching audit records, a successful envelope and continuation metadata. A specific audit identifier is a filter on this operation; a separate invented detail route is not needed. Native validation and permission errors are retained.

## Continue audit cursor

The returned cursor continues the same audit query. Success retrieves the next records with their identities and timestamps. Paging ends according to the returned continuation state. A truncated MCP result is incomplete even if the API envelope indicates success.

## List posture findings

The collection query uses requested filters such as integration, severity, observation or vendor. Success returns matching findings and paging metadata. Invalid filters require correction from the schema; unauthenticated or forbidden responses require the configured access to be checked. An empty successful query means no matching visible findings, not universal absence of risk.

## Read finding detail

A selected finding identifier returns its native detail, integration, active/archived counts and any severity override. Success preserves the platform severity and evidence. Not found remains absent for that identifier; forbidden access is not treated as absence. No finding is ignored, archived or reclassified here.

## Query IP overview

An IPv4 or IPv6 lookup returns the native IP overview, including available location, ASN and threat-category information. Success is the returned overview, not a numeric threat score. The source wrapper's generic score promise is not established by this operation. Missing data or a native error remains explicit.

## Patterns

An account audit event is evidence of a recorded action, not proof of malicious intent. Platform severity and overrides remain separate fields. Source-specific field and permission assumptions are replaced by the current contract.

## Known limitations

No firewall/security-event GraphQL query, custom risk ranking or numeric IP threat score is implemented here. Audit retention and product access follow the account's actual platform contract. The general-purpose MCP can mutate data, but only these reads are in scope.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Discover contract | Resolve current operation schema | Read |
| Query audit / Continue cursor | Retrieve complete scoped audit events | Read |
| List findings / Read detail | Retrieve native posture evidence | Read |
| Query IP overview | Retrieve available indicator intelligence | Read |

## Verification checklist

- Account, window, filters and IDs match the request.
- Audit cursors and collection paging are exhausted or incompleteness is stated.
- Native severities, categories and errors are retained.
- No remediation or unsupported numeric-score claim is reported.
