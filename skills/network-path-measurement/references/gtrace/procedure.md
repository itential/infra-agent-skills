# gtrace local path measurement

Run a bounded local traceroute or MTR using the publisher MCP tools.

## Common Sequences

- Trace a target: **Resolve request** → **Trace** → **Report observations**.
- Repeated measurement: **Resolve request** → **Measure repeated cycles** → **Report observations**.

### Resolve request

The request identifies target, protocol, optional destination port, hop bound and probe settings. The publisher requires raw-socket privileges: macOS uses elevated execution, while Linux supports elevation or a preconfigured raw-socket capability. Missing privilege is an environment failure; this procedure does not grant it. Invalid duration/configuration or failed target resolution ends the measurement.

### Trace

Active probing affects the selected target/path: stop and confirm with the operator before proceeding. Tracing returns per-hop observations and available enrichment. ECMP flow variation and NAT detection are explicit options. Path-MTU discovery, when requested, supports ICMP/UDP only. An engine-creation or execution error is a failed test, not an unreachable-target finding.

### Measure repeated cycles

Before starting the requested repeated traffic: stop and confirm with the operator before proceeding. The MTR operation uses the specified cycle count, interval and timeout and returns native packet-loss and latency statistics. Invalid interval/configuration or execution failure remains an error. It is a bounded test, not a persistent monitoring deployment.

### Report observations

The result retains the originating host/vantage, target resolution, protocol, hop responses, available labels and native measurements. JSON mode yields structured content; text graph/table views are presentation modes. Enrichment or inferred path features are not substituted for observed forwarding state. No universal congestion or hardware-failure verdict is derived from one missing hop.

## Patterns

JSON output is independent of the text graph/table view. Optional enrichment queries have separate provider coverage; the local probe and its metadata can have different success states.

## Known limitations

No remote Globalping call is hidden inside this local procedure. ECMP/NAT/MTU observations depend on probe behavior and supported options; no completeness guarantee is made.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Trace | Send bounded path probes | Active network measurement |
| MTR | Repeat path measurements for selected cycles | Active network measurement |

## Verification checklist

- Target, vantage, protocol and bounds are retained.
- Required privileges are established without automatic changes.
- Tool errors and missing hop responses remain distinct.
- Native structured observations are preserved.

## Sources

- [gtrace publisher README](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/README.md). Retrieved 2026-10-09.
- [Tool schemas](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/internal/mcp/server.go). Retrieved 2026-10-09.
- [Tool error handling](https://github.com/hervehildenbrand/gtrace/blob/db04fd53e5a2a54c0fa0288543d619b9ece7d0c2/internal/mcp/handlers.go). Retrieved 2026-10-09.
