# AWS network evidence collection

Inspect a selected cloud network or follow the publisher's path-tracing workflow through configuration and observed traffic.

Source: current [AWS Network MCP reference](https://awslabs.github.io/mcp/servers/aws-network-mcp-server) and its [publisher README](https://github.com/awslabs/mcp/blob/main/src/aws-network-mcp-server/README.md), retrieved 2026-10-09. Tool bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Network inventory: Discover tool schemas → Read VPC/ENI → Read transit/hybrid network → Read firewall configuration.
- Connectivity evidence: Discover tool schemas → Read path methodology → Locate endpoints → Read applicable network configuration → Read traffic evidence.
- Cloud WAN proposal: Discover tool schemas → Read Cloud WAN → Simulate route change.

## Discover tool schemas

The approved publisher server advertises its current tool definitions and inputs. The selected operation uses those schemas and explicit account/profile/region scope. Absent tools or required inputs leave that operation unsupported, not an empty infrastructure result. Authentication/IAM failures are reported for the failed scope; they do not establish network outage.

## Read path methodology

The publisher's troubleshooting tool supplies the service-specific sequence for the requested path before endpoint inspection. It is evidence-selection guidance; recommendations do not authorize changes or replace operator-supplied endpoints.

## Locate endpoints

IP lookup locates ENIs and supports multi-region searches. ENI detail then supplies attached security groups, network ACLs and routing context. The returned account, region, ENI and network identifiers become selectors for later reads. No match means no visible match in the searched scope, not proof the address is unused.

## Read VPC/ENI

VPC inventory selects a VPC; its detail operation returns subnets, routes and gateway/security context. ENI detail establishes its network attachment. Completion is a returned object with the intended identity, preserving each reported state and diagnostic.

## Read transit/hybrid network

Transit Gateway inspection reads a discovered gateway, its route tables/routes, peerings, and inspection attachments. The route tools require registration with Network Manager; missing registration blocks those queries rather than proving missing routes. Cloud WAN inspection reads a core network's segments/policy/attachments, selected or all routes, peerings and inspection groups. Site-to-Site VPN inventory returns connection/tunnel state. Successful configuration reads are not a packet-delivery test.

## Read firewall configuration

Firewall inventory selects the firewall; rule retrieval returns its stateless/stateful rule information. Inspection detection reports configured inspection relationships. It does not establish that every requested packet was inspected successfully.

## Read traffic evidence

VPC, Transit Gateway and Network Firewall flow-log queries require logs enabled and sent to CloudWatch Logs. No-flow-log diagnostics require checking logging destination, requested interval, traffic occurrence and query permissions. Cloud WAN event-log retrieval supplies routing/topology events. Query failure or incomplete output is retained; it is not converted into 'no drops' or 'no changes'.

## Simulate route change

The Cloud WAN simulator evaluates the supplied proposal for a single region and returns modeled impact. Simulation does not submit a policy change. Its supported inputs and returned qualifications come from the current tool schema; unsupported changes remain unverified.

## Patterns

Profiles can select different accounts, including separate profiles for cross-service resources. Multi-region IP discovery differs from a region-scoped inventory call. The publisher's shorthand 'Describe/Get/List only' is not literal for log retrieval: its permissions also include starting and retrieving CloudWatch queries.

## Known limitations

The publisher does not specify a stable exhaustive error-code/retry contract for these MCP wrappers. Native tool diagnostics and partial results remain visible. S3/Firehose-only flow logs are not covered by these flow-log tools. No failure triggers infrastructure modification.

## Tools

| Operation | Description | Category |
|---|---|---|
| Discover tools/path methodology | Reads the current interface and documented investigation sequence | Discovery |
| Locate endpoints/read configuration | Collects scoped network object state | Read |
| Read traffic evidence | Retrieves existing flow/event data | Query |
| Simulate route change | Models one-region Cloud WAN impact | Analysis |

## Verification checklist

- Every object is attributed to the queried account/profile and region.
- Configuration, observed logs, and simulation results are distinguished.
- Missing permissions, Network Manager registration, or flow logs remain limitations.
- The result does not claim a universal health or compliance verdict.
