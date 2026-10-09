# Equinix Network Edge visibility

Equinix Fabric MCP reads the selected Network Edge devices and their account, project, metro, device-type and ACL associations.

Source: [Network Edge Tools](https://docs.equinix.com/equinix-api/mcp-servers/ne-mcp-tools/), public preview, retrieved 2026-10-09. Bindings are in [network-edge-endpoints.md](network-edge-endpoints.md).

## Common Sequences

- Device inventory: Discover contract and scope → Read project/account/metro catalogue → Read devices → Check query outcome.
- ACL association: Discover contract and scope → Read devices → Read ACL/template associations → Check query outcome.

## Read project/account/metro catalogue

Project and account reads identify visible scope; metro and device-type reads show the provider's available locations and platform types. Success returns the selected catalogue with stable identifiers. Availability in a catalogue is not a provisioning action or a guarantee of available capacity for a particular order.

## Read devices

Device reads retrieve visible virtual-device records or a selected UUID's details according to the live schema. Success retains device UUID, location and native provider state. An empty scoped query is not a tenant-wide absence claim.

## Read ACL/template associations

The device ACL read and template catalogue/detail reads identify the configured association and its entries. Success preserves the specific device/template identifiers. A permitted prefix in that model does not establish every intervening hop's behavior or actual connectivity.

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
| Discover contract and scope | Resolve available tool and account/project context | Read |
| Read catalogues | Retrieve visible accounts/projects/metros/device types | Read |
| Read devices | Retrieve virtual-device inventory/details | Read |
| Read ACL/template associations | Retrieve provider ACL configuration | Read |

## Verification checklist

- Scope and stable resource identifiers match the request.
- Pagination is complete or the limitation is stated.
- Empty results, authorization failures and query errors remain distinct.
- Provider configuration is not reported as a packet test or guest health check.
