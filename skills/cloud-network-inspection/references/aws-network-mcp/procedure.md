# AWS Network Inspection via the AWS Network MCP Server

Read AWS VPC, Transit Gateway, Cloud WAN, VPN, and Network Firewall configuration plus existing flow-log evidence through the AWS Network MCP server.

Sources: AWS Labs MCP documentation, AWS Network MCP Server reference page and README (retrieved 2026-10-26). Tool names and parameters are in [endpoints.md](endpoints.md).

This procedure is diagnostic-shaped and read-only: it reads state and maps it to evidence, so it has no confirmation gates. The server's documented permission set holds no action that creates or modifies a network resource.

## Common Sequences

- Inventory: Confirm tools and scope, Read VPC and ENI, Read transit and hybrid network, Read firewall configuration.
- Connectivity evidence for a source and destination: Confirm tools and scope, Read path methodology, Locate endpoints, Read the configuration that applies, Read traffic evidence.
- Cloud WAN what-if: Confirm tools and scope, Read transit and hybrid network (Cloud WAN), Simulate route change.

## Confirm tools and scope

Fix the AWS profile (or profiles, for cross-account reads) and region before the first call, and read each needed tool's input schema from the connected server; the documentation publishes none. If a needed tool is absent, that operation is unsupported: report it, do not improvise. Credentials that fail or lack permission leave that scope unobserved, which is not evidence of an outage.

## Read path methodology

For a connectivity question, call the server's methodology tool first; its documentation says to call it before anything else. Use its returned sequence to choose which later reads apply. It guides what to read and does not replace the endpoints the requester supplied.

## Locate endpoints

Look up the network interface for an IP address (the search can span regions), then read the interface's detail for its security groups, network ACLs, and routing context. Carry the returned account, region, and interface identifiers into later reads. No match means no match in the searched scope, not that the address is unused.

## Read VPC and ENI

List VPCs in the region, then read the chosen VPC's network details. Success is a returned object whose identity matches the request, with reported states kept as given.

## Read transit and hybrid network

- Transit Gateway: list gateways, read one gateway's details, read routes for one route table or all route tables, list peerings, and detect attached inspection firewalls. Route reads require the gateway to be registered with AWS Network Manager; without registration they fail, which does not mean routes are missing.
- Cloud WAN: list core networks, read core network details and attachment details, read routes for one segment or all segments, list and read peerings, and detect inspection groups.
- Site-to-Site VPN: list connections in the region.

Configuration reads are not a packet-delivery test.

## Read firewall configuration

List AWS Network Firewalls in the region, then read the chosen firewall's stateless and stateful rules. Inspection detection (above) reports attachment, not that a given flow was inspected.

## Read traffic evidence

Query VPC, Transit Gateway, or Network Firewall flow logs, or fetch Cloud WAN topology and routing events. Flow-log tools work only where logs are delivered to CloudWatch Logs; logs delivered to S3 or Kinesis Data Firehose are unreachable by them. When a flow-log query returns nothing, check the logging destination, the time window, whether the traffic occurred, and the caller's permission to run log queries before concluding anything. These queries run through CloudWatch Logs Insights, which is billed and subject to concurrency quotas (Unverified: amounts); keep the time range and log group set as narrow as the request allows. A failed or partial query stays reported as such; it is never converted into "no drops" or "no changes".

## Simulate route change

Submit a proposed Cloud WAN change for one region and report the modeled impact. Only one region is simulated per call. Inputs and any caveats in the answer come from the tool's schema and output; changes the tool cannot model remain unverified. Unverified: whether the tool ever applies a change; the server's documented permission set lists no write action, so treat the result as a model only, and stop and confirm with the operator before relying on it for a live change decision.

## Patterns

- Use separate profiles when Transit Gateway and Cloud WAN resources live in different accounts.
- Region-scoped list tools see only their region; the IP lookup is the one documented multi-region search.
- Configuration, observed logs, and simulation are three kinds of evidence; label each.

## Known limitations

- Per-tool input schemas, response formats, error strings, rate limits, and quotas are not documented. On throttling or an unexplained failure, back off, honor any retry hint, and report the native error with the scope it applied to.
- The server runs only on the same host as the MCP client.
- No resource modification and no compliance or health verdict.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read path methodology | Fetch the troubleshooting sequence | Discovery |
| Locate endpoints / Read configuration | Read scoped network object state | Read |
| Read traffic evidence | Query existing flow and event logs | Query |
| Simulate route change | Model a one-region Cloud WAN change | Analysis |

## Verification checklist

- Each reported object names its account or profile and region.
- Configuration, observed logs, and simulation results are kept separate.
- Missing permissions, Network Manager registration, or CloudWatch Logs delivery are listed as limitations, not as empty results.
- No health or compliance verdict is stated.
