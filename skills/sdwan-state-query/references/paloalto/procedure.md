# Prisma SD-WAN: query tenant state

Retrieve explicitly scoped records through the Unified SASE SD-WAN API.

Sources: [Unified API prerequisites](https://pan.dev/sdwan/api/), [SASE authentication](https://pan.dev/sase/docs/getstarted/), and [publisher Unified OpenAPI](https://github.com/PaloAltoNetworks/pan.dev/blob/master/openapi-specs/sdwan/unified/open_api_unified.json), version Latest with individual operation versions in [endpoints.md](endpoints.md), retrieved 2026-10-09.

## Common Sequences

- Device/configuration query: Initialize profile → Discover scope → Read selected resource → Report result.
- Topology/event query: Initialize profile → Discover scope → Query topology or events → Report result.
- Application catalogue: Initialize profile → Read application definitions → Report result.

## Initialize profile

The service-account token is scoped to the intended tenant service group and the account has assigned roles. Immediately after token creation, the documented profile read initializes SD-WAN access. The publisher states that later SD-WAN calls otherwise return forbidden status.

Success: the profile operation succeeds for the intended authenticated scope. A forbidden response requires checking profile initialization and service-account roles; a token alone does not grant product access.

## Discover scope

Site, element and machine lists provide real resource identifiers. Elements include their site association, model, serial and software-version fields. These returned relationships select the site and element for dependent reads; names are not substituted into identifier fields.

Success: the requested identity and parent relationship are established. A machine lookup can report missing machines or invalid tenant/region association; those remain distinct errors. The published machine schema includes token and console-passphrase fields: raw machine responses can expose secrets and must not be reproduced in public reports.

## Read selected resource

The selected dependent query reads element interfaces, BGP peer configuration, static routes, site WAN interfaces, security zones, or path-policy sets. Element status describes its controller/cloud connection state. The software-status operation returns up to five upgrade records initiated by the tenant user.

Success: the API returns the requested record or item list. A missing element-status response is reported as status unavailable for that identifier. BGP configuration alone does not establish that a session is up. The status schema does not establish CPU/memory measurements, and software-upgrade history is not a catalogue of available upgrades.

## Read application definitions

The application-definition read returns the tenant's configured definitions, including identifiers, display names, categories, parent/override relationships and supported engine information where present.

Success: the requested definition is selected from actual returned records. NetClaw's example low/medium/high risk field and SaaS/on-premise/custom type enumeration are not supported by the cited response schema and are not inferred.

## Query topology or events

Topology queries use the requested topology type and documented scope filters. A successful result returns topology data for that scope. Invalid JSON, extra attributes, invalid topology options or a topology rebuild are native failures; a rebuild-in-progress result is not an empty topology. The API supplies no retry interval for that condition here.

Event queries carry explicit start/end timestamps, filters and result limits. The requested time interpretation distinguishes event occurrence from database creation. A returned cursor obtains the next page using the same query scope. Standing-event filtering is explicit; acknowledgment and suppression are separate filters, not proof that an event has cleared.

Success: the query returns the documented response and each requested page has a known outcome. Invalid-request errors require corrected parameters. A partial page sequence stays partial.

## Report result

The result states tenant scope, selected IDs, resource type, query/time filters and returned native states. It preserves API errors and any limits on completeness. The documented success response is HTTP success plus the expected JSON record/items; it is not a network-wide health verdict.

## Patterns

Several read queries use a request body. HTTP method alone therefore does not classify a request as a configuration change. API versions differ per resource family; replacing all versions with one guessed global number is invalid.

## Known limitations

The machine-list success schema combines an item-list definition with an unrelated query reference; this inconsistency in the publisher schema is flagged here. Its undocumented fields are not treated as mandatory response guarantees. Collection-wide paging for simple list operations is not described by the selected OpenAPI operations; no hidden automatic paging is claimed.

Site YAML export, CPU/memory metrics, upgrade-availability decisions and the community MCP wrapper's automatic refresh/name resolution are outside this procedure. No fixed token lifetime or generic API rate limit is invented.

## Tools

| Operation | Description | Category |
|---|---|---|
| Initialize profile | Establish SD-WAN service context for the token | API query |
| Discover scope | Read sites, elements or machines | API query |
| Read resource | Retrieve selected configuration, status or application definition | API query |
| Query topology/events | Retrieve filtered topology or event records | API query |

## Verification checklist

- Profile initialization and tenant role scope were established.
- Site/element identifiers came from discovered records.
- Query results retain their native status and event meaning.
- Secret-bearing machine fields are excluded from public reporting.
- Time filters, cursors and limits qualify the reported coverage.
