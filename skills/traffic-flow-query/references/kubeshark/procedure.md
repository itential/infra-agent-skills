# Kubeshark L4 flow query

Read transport-flow observations from the publisher Hub API.

## Common Sequences

- Scoped flow inspection: **Select scope** → **Read flows**.
- Cluster summary: **Select scope** → **Read summary**.

### Select scope

The existing Hub and its access controls determine visible traffic. Authenticated deployments require the MCP-use capability; a forbidden response is an authorization failure. An expired direct-connection token requires renewed authentication, not a blank inventory. L4 flow reads do not require raw packet capture or L7 dissection.

### Read flows

Requested namespace, Pod, Service, IP, protocol, aggregation and result limit select the observation. The response includes peer identities, counters and optional handshake timing. The result's truncation flag is retained; a limited response is not the whole cluster. TCP handshake percentiles are in microseconds and are separate for client/server observations. They are not application response latency.

### Read summary

The summary supplies flow totals, protocol counts, observed bytes/packets, ranked peers and namespace relationships. The documented summary has no required filter parameters; it must not be described as inheriting a previous scoped flow query. Missing traffic leads to a check of observation coverage and peer names, not an assertion that communication is impossible. Transport or service errors leave the query incomplete.

## Patterns

The flow collector observes socket activity through eBPF. A summary and a scoped flow response can legitimately have different coverage. The publisher offers example latency interpretations, but this query procedure reports measurements without imposing an environment-independent SLA.

## Known limitations

No exhaustive API error catalogue or stable historical-retention guarantee is published in the cited L4 page. Capture availability and application payload dissection are separate features. Authentication and tool availability depend on deployment.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Read flows | Retrieve scoped L4 observations | Traffic read |
| Read summary | Retrieve cluster connectivity aggregates | Traffic read |

## Verification checklist

- Scope, aggregation and any result limit are reported.
- Truncation remains explicit.
- Handshake units and peer perspective are preserved.
- Summary scope is not silently narrowed.

## Sources

- [Kubeshark L4 tools](https://docs.kubeshark.com/en/mcp/l4_tools). Retrieved 2026-10-09.
- [Kubeshark MCP installation](https://docs.kubeshark.com/en/mcp/cli). Retrieved 2026-10-09.
- [Kubeshark MCP access controls](https://docs.kubeshark.com/en/mcp). Retrieved 2026-10-09.
