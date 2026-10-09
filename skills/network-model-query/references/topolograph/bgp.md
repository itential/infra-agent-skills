# Topolograph BGP model queries

Read the selected stored Topolograph model without changing network or model state.

## Common Sequences

- Route context: **Select epoch** → **Read speakers and routes**.
- Change comparison: **Select epoch** → **Read time-bounded changes**.
- Forwarding model: **Select epoch** → **Verify IGP binding** → **Resolve modeled route**.

### Select epoch

BGP graph discovery returns available collection epochs. The chosen BGP epoch is distinct from an IGP graph identifier. Publisher documentation requires Topolograph 2.69 or later for the BGP surface; missing version support is not evidence of an empty network. Pagination and epoch time are retained. Authentication, compatibility and transport failures end the query with the native failure.

### Read speakers and routes

Speaker/session lists return model roles, collection evidence and pagination. Route search can cover the full graph or one speaker's resolved RIB view. A prefix filter is exact for CIDR input; address input finds covering routes in longest-prefix order. Native RIB/evidence qualifiers accompany the rows. A router-specific query does not honor whole-graph source/table filters. The speaker summary supplies its RIB counts and advertised-route count; it is not a live-device counter.

### Read time-bounded changes

Point-in-time state reconstructs routes from stored events. Comparison returns added, withdrawn or changed rows, retaining prior values for changed routes. Cross-epoch comparison requires epochs from the same collector. Event timeline results preserve their interval and selected grouped or row representation. The relative lookback option overrides the explicit start time. Missing history is not proof that no route changed.

### Verify IGP binding

The binding list and selected binding report the relationship between the BGP epoch and an IGP graph, including matched identities and source coverage. VRF inventory belongs to the selected IGP graph and can be narrowed by router or distinguisher. A missing or incomplete binding remains a limitation; it is not synthesized from similar names.

### Resolve modeled route

Route resolution uses the IGP graph, start node, destination, explicit VPN selectors and desired evidence level. Its rows show modeled routing decisions including supported static/BGP/IGP/tunnel handoffs. Optional edge-cost changes are a what-if calculation, not a device update. Native incomplete/error results and evidence qualifiers accompany the path; this does not prove present packet delivery.

## Patterns

BGP epoch identity and IGP graph identity are carried independently through binding and route resolution. A later epoch can change the coverage or validity of a binding.

## Known limitations

No policy/session changes are included. The NetClaw VPN-router tool name is absent from the verified publisher interface; it remains unsupported rather than being aliased to another operation.

## Tools

Assumes the authenticated client described in [the bindings](bgp-endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Discover model | Resolve the requested graph and observation scope | Model read |
| Query model | Read topology, routes, events or a computed prediction | Model read |

## Verification checklist

- Both epoch and graph identities are explicit where applicable.
- RIB evidence, source coverage and pagination are preserved.
- Comparison uses valid same-collector history.
- Path predictions are not called live forwarding observations.

## Sources

- [Publisher MCP implementation](https://github.com/Topolograph/topolograph-mcp-server/blob/2a7c7e341ac14026d925aed900fdf110f5191246/mcp-server.py). Retrieved 2026-10-09.
- [Publisher compatibility and mode documentation](https://github.com/Topolograph/topolograph-mcp-server/blob/2a7c7e341ac14026d925aed900fdf110f5191246/README.md). Retrieved 2026-10-09.
