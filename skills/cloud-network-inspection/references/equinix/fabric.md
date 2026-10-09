# Equinix Fabric configuration and routing query

Equinix Fabric MCP reads interconnect resources, routing/filter relationships and telemetry configuration for a selected provider scope.

Source: [Fabric MCP Tools](https://docs.equinix.com/equinix-api/mcp-servers/fabric-mcp-server/), public preview, retrieved 2026-10-09. Bindings are in [fabric-endpoints.md](fabric-endpoints.md).

## Common Sequences

- Interconnect inventory: Discover contract and scope → Read infrastructure → Read service context → Check query outcome.
- Routing investigation: Discover contract and scope → Read infrastructure → Read routing → Read filter/aggregation associations → Check query outcome.
- Telemetry configuration: Discover contract and scope → Read streams → Read stream assets/subscriptions/alerts → Check query outcome.

## Read infrastructure

Connection, port, router, network and IP-block searches return provider records within the chosen filters. Port VLAN and metro reads add their documented detail. Success preserves resource UUIDs and native status; configured capacity or a provisioning state is not a forwarding test. Router-command result lookup reads existing command results and does not initiate a new measurement.

## Read service context

Service profile list/detail/metro reads identify advertised services, and router-package/pricing searches return current provider catalogue information. These reads do not order resources or establish a fixed price for a future order. Service-token retrieval is excluded because the source identifies it as access material; no token values are required for this inventory result.

## Read routing

Route searches distinguish advertised, received and active route views. Routing-protocol reads and prior protocol-action status reads preserve connection identity and native protocol state. Reading one side does not establish the far-side session or cloud route state. The route-refresh action is excluded even though the catalogue assigns it Viewer, because it requests a provider action rather than retrieving existing evidence.

## Read filter/aggregation associations

Filter/aggregation collections, individual rules, attached connections and change-history reads identify the selected routing policy and its relationships. Success retains attachment direction and identifiers when returned. Missing relationship data remains unknown; a matching display name is not a substitute for identity.

## Read streams / Read stream assets/subscriptions/alerts

Stream list/detail, attached asset list/detail, Network Edge stream-device detail, subscriptions and alert-rule reads describe telemetry configuration. Success returns the specified stream and related records. A configured subscription does not prove successful downstream delivery.

## Discover contract and scope

The configured client identifies the account/project and requested metro or resource identifier. Live tool discovery supplies exact inputs, paging and response schemas; the public preview catalogue does not publish a stable complete field dictionary. Success is an available read tool with a verified scope. A missing tool remains unavailable, rather than being invoked with guessed arguments.

## Check query outcome

A successful call returns the operation's native resource data, including its identifiers and status. All requested pages are retrieved using the tool's own continuation contract, or the result is marked partial. A complete empty result is distinct from an expired authorization, denied permission, unavailable resource or failed request. The publisher does not enumerate stable errors for every MCP method; returned errors require the linked product API's guidance and are not converted into empty inventory.

## Patterns

Effective access is the intersection of the user's Customer Portal roles and the connection's selected permission level. Viewer permits observation, while additional granted permissions do not authorize extra operations in this read-only procedure. The same names for project/metro discovery appear in both product catalogues; the live schema determines their returned scope, without an invented product selector.

## Known limitations

The MCP service is public preview, so names and response formats can change. The publisher exposes no delete tools at any permission level. Provider state does not establish guest-device routing health or end-to-end traffic delivery. No business-specific compliance ranking or automatic remediation is performed.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Read infrastructure | Query connections, ports, routers, networks and IP blocks | Read |
| Read service context | Query profiles, metro availability, packages and prices | Read |
| Read routing | Query routes/protocols and existing action results | Read |
| Read policy associations | Query route filters, aggregations, rules and history | Read |
| Read telemetry configuration | Query streams and their relationships | Read |

## Verification checklist

- Account/project/metro/resource scope and native identifiers are retained.
- Native status, route view and policy relationships are reported without reachability assumptions.
- Paging and source-specific errors are visible.
- No ordering, creation, update, refresh, attach, reset or delete operation was performed.
