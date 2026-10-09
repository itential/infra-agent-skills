# Cisco Catalyst SD-WAN Manager state queries

Retrieve fabric inventory, selected device observations, templates, policy configuration or alarms through the publisher community MCP server.

Sources: [publisher README](https://github.com/CiscoDevNet/catalyst-sdwan-mcp-community/blob/main/README.md), [tool schemas and dispatch](https://github.com/CiscoDevNet/catalyst-sdwan-mcp-community/blob/main/src/server.ts), [API client](https://github.com/CiscoDevNet/catalyst-sdwan-mcp-community/blob/main/src/services/vmanageApi.ts), current main, retrieved 2026-10-09. Literal bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Device evidence: List devices → Resolve device → Read selected device state.
- Template inspection: List templates → Read attachment or definition.
- Fabric records: Read controller/policy/alarms records → Report coverage.

### List devices

An optional model restriction selects fabric inventory. The successful response retains the manager's native data and identifiers, including system address and device type where returned. Transport or authentication failure remains a query failure; an empty native collection does not prove another tenant or manager has no devices.

### Resolve device

The detail read matches either the inventory UUID or system address and returns the matching device. A missing identifier or an explicit not-found object prevents further device-specific queries. The implementation does not convert every not-found object into a transport error, so successful MCP transport is not sufficient.

### Read selected device state

The resolved device scope selects the requested control connections/summary/statistics, OMP peers/routes/summary, BFD sessions/summary/transport-locator summary, BGP peers/routes/summary, interfaces, system status, ARP, application-routing statistics/SLA classes, flow observations, VPNs or transport locators. Each successful operation returns the manager's native JSON rather than a normalized health verdict. An API error remains its native HTTP status/body; absent data is not automatically a fault. The source exposes no common health threshold or exhaustive output schema.

### List templates

The requested device-template or feature-template collection returns identifiers for the next read. These are configuration objects; listing them does not attach or deploy a template. A list failure stops the dependent read.

### Read attachment or definition

A known device-template identifier selects its attached devices. A definition read additionally selects device or feature template type. Missing identifiers/type fail locally. Success is the native attachment/definition response for that selected type; no deployment-success inference is made from stored configuration.

### Read controller/policy/alarms records

The selected fabric operation reads controllers, reachable devices, WAN-edge inventory, policy lists/definitions/assemblies, or alarms. Optional policy type filters retain the platform's vocabulary. Alarms have an explicit result bound and no published continuation argument in this wrapper. Success is the native response for the requested operation; all API errors remain failures rather than zero results.

### Report coverage

The result identifies the manager, selected device/template/type and read operation, preserving native values and any result limit. The wrapper returns a single response per call and does not implement a general pagination loop. Its read-only tools do not establish complete coverage when the upstream API paginates.

## Patterns

- Routers are queried through the manager; this binding does not initiate direct router sessions.
- The current publisher names and inputs differ from the older community wrapper used in NetClaw.
- A template definition, policy definition and live device observation are different evidence.

## Known limitations

- **Publisher security defect:** the cited client disables TLS certificate validation for every HTTPS request. Its README's suggestion to use a signed certificate does not change that code behavior. A deployment must correct certificate verification before this binding is suitable for transmitting production credentials; this procedure does not endorse the insecure default.
- Raw running-configuration and recent event tools from the source NetClaw wrapper are absent from this publisher toolset and remain unconverted.
- There is no universal output schema, readiness score, rate-limit figure or pagination guarantee in these sources.
- Configuration mutation and software lifecycle operations are outside this read procedure.

## Tools

| Operation | Description | Category |
|---|---|---|
| List/resolve devices | Retrieve fabric identifiers and one device | Inventory |
| Read device state | Read selected protocol/interface/system/flow state | Observation |
| List templates | Discover device/feature template identifiers | Configuration read |
| Read template attachment/definition | Retrieve a template's stored definition or attached devices | Configuration read |
| Read fabric records | Retrieve controllers, policies, edge inventory or alarms | Read |

## Verification checklist

- The deployed client's TLS verification defect has been addressed before production use.
- Device/template identifiers were resolved in the intended manager.
- Both MCP errors and embedded not-found errors were checked.
- Native state and configuration are reported distinctly, with limits and incomplete coverage preserved.
