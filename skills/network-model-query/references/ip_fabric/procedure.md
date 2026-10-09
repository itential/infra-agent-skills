# IP Fabric snapshot query

IP Fabric MCP reads a selected network snapshot and returns its native health findings, path data or inventory query results.

Source: [IP Fabric MCP Server](https://docs.ipfabric.io/latest/IP_Fabric_Settings/integration/mcp/), current documentation, retrieved 2026-10-09. Bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Network health: Assess health → Review snapshot findings.
- Connectivity evidence: Resolve snapshot → Trace path → Render path (when requested) → Review snapshot findings.
- Other model data: Discover query → Inspect query contract → Execute read query → Review snapshot findings.

## Assess health

The health operation returns findings about snapshot freshness, intent verification, inventory, routing neighbors and path checks. Success is the native assessment and its available evidence. Severity labels belong to the platform; no new universal scoring system is added. Authentication failures follow the error handling below.

## Resolve snapshot

A path query identifies the snapshot, not merely a device pair. If the platform reports the documented missing-snapshot condition, the snapshot inventory is obtained through the discovery sequence and a loaded snapshot is selected. The publisher also documents its latest-snapshot selector. An unavailable snapshot prevents a path result; another snapshot is not silently substituted.

## Trace path

The selected unicast, host-to-gateway or multicast operation receives its required endpoints, snapshot and grouping, together with applicable VRF and transport details. Success is structured path data for that context. Unicast transport defaults to ICMP when omitted; requested TCP/UDP context is explicit. A failed lookup remains failed, not evidence that traffic is denied. Optional graph layout is omitted by default.

## Render path

The corresponding diagram operation uses the same path inputs and returns a PNG. Success is a returned image for the same snapshot and endpoints. A diagram does not replace the structured evidence when the request requires hop-level details.

## Discover query

Natural-language endpoint search locates candidate operations for inventory, routing or other collected data. Success identifies a candidate API operation; this is not yet a completed data query.

## Inspect query contract

The endpoint-detail operation returns parameters and response schema. Only an operation documented as reading data is in scope, including a read query that the platform transports using a non-GET method. The details determine exact filter fields and pagination; unavailable details leave the query unverified rather than guessed.

## Execute read query

The invocation operation runs the selected read with its documented parameters. Success matches that operation's response schema and pagination contract. An authentication failure requires checking the configured token, revocation and role permissions. A not-found connection failure requires checking the configured endpoint and whether MCP is enabled. Other API errors retain the returned details and require endpoint-specific guidance; there is no published universal retry count here.

## Review snapshot findings

The result records snapshot identity, freshness evidence, endpoint/VRF/protocol context where relevant, and native findings. Incomplete collection or pagination remains visible. No result from a stored snapshot is described as a live packet observation.

## Patterns

The token's role controls every request; connecting to MCP does not bypass IP Fabric authorization. Discovery, detail and invocation are separate operations, preventing a guessed endpoint contract.

## Known limitations

The operator must already have accepted the publisher's MCP terms and enabled the server; this procedure does neither. Generic invocation can expose mutation operations, which are outside this read-only capability. Native query-specific error and pagination contracts are discovered at execution time.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Assess health | Obtain native snapshot findings | Read |
| Trace path | Query unicast, gateway or multicast forwarding model | Read |
| Render path | Obtain corresponding path PNG | Read |
| Discover query / Inspect query contract | Resolve an approved read operation | Read |
| Execute read query | Retrieve selected model data | Read |

## Verification checklist

- The snapshot exists and its freshness is reported.
- Path inputs and diagram context match the request.
- Discovered query parameters and paging follow the returned contract.
- Native errors, collection gaps and authorization limits are retained.
