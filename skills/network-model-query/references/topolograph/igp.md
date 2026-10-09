# Topolograph IGP snapshot queries

Read the selected stored Topolograph model without changing network or model state.

## Common Sequences

- Inventory/path: **Select graph** → **Read topology** → **Compute requested path**.
- Change history: **Select graph** → **Read monitored events**.
- Failure scenario: **Select graph** → **Read topology** → **Simulate edge failure**.

### Select graph

Graph discovery filters protocol/area/name and returns monitoring flags and pagination. The selected identifier and observation time accompany all results. A watcher-derived graph and a currently live watcher are different properties. Authentication/transport failure is a failed query, not missing topology. Graph status returns its own ok, warning, critical or no-monitoring-data classification; this is not a device-health verdict.

### Read topology

The selected graph supplies networks, nodes, edges and LSPs. Complete pagination precedes a count. Network queries use exact router/system identity. Parallel links require their returned stable edge identity. LSP results retain placement, cost and blocking constraints: a disconnected graph, incompatible constraints, unreachable strict hop and absent endpoint are separate findings. Multiple blocking constraints may act together; no configuration change follows automatically.

### Compute requested path

Ordinary shortest-path queries return path and cost for the selected source/destination. Tunnel-aware forwarding supports only one destination; a signalled tunnel without autoroute does not automatically replace ordinary forwarding. Constrained-path calculation evaluates requested bandwidth, affinities, shared-risk groups, priority and supported IS-IS level without creating a tunnel. An empty path/null cost with a reason is a successful no-placement answer. Unsupported level calculation requires compatible stored data; YAML level selection is unsupported. Missing graph is a failed lookup.

### Read monitored events

Only watcher-derived graphs support event history. A manually uploaded graph is reported as unmonitored, not as having no changes. Network events distinguish network up/down and cost changes; transitions involving the documented down sentinel retain that meaning. Adjacency events and node/host timeline waves are separate outputs. Timeline recovery applies only within the queried interval. A wave's bounds can select its underlying events. All pages and the actual requested time interval accompany the result.

### Simulate edge failure

The selected graph and explicit failed-edge pairs produce predicted connectivity, disconnected groups and modeled path redistribution. No link is disabled. Returned percentages describe model path changes, not measured traffic throughput. A backend error retains its graph identity and native diagnostic code.

## Patterns

Each sequence keeps one explicit graph identity. Node/host event waves do not stand in for every raw network or adjacency event. Predicted paths are labeled as model results.

## Known limitations

No upload, LSP write, live-device validation or node-failure API is included. Snapshot age and watcher coverage constrain conclusions. Exact backend error details remain authoritative.

## Tools

Assumes the authenticated client described in [the bindings](igp-endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover model | Resolve the requested graph and observation scope | Model read |
| Query model | Read topology, routes, events or a computed prediction | Model read |

## Verification checklist

- Graph identity, age and monitoring state are retained.
- Counts include all requested pages.
- No-placement and failed lookup remain distinct.
- Simulations are identified as predictions.
- Event queries use monitored graphs and explicit intervals.

## Sources

- [Publisher MCP implementation](https://github.com/Topolograph/topolograph-mcp-server/blob/2a7c7e341ac14026d925aed900fdf110f5191246/mcp-server.py). Retrieved 2026-10-09.
- [Publisher compatibility and mode documentation](https://github.com/Topolograph/topolograph-mcp-server/blob/2a7c7e341ac14026d925aed900fdf110f5191246/README.md). Retrieved 2026-10-09.
