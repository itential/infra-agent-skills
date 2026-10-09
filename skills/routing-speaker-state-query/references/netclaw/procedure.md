# NetClaw existing-speaker evidence

Read BGP peers and local routes from the already-configured NetClaw protocol MCP, with restricted use of its aggregate and GRE observations.

## Common Sequences

- BGP evidence: **Read BGP peers** → **Read BGP routes**, retaining the response source of both reads.
- Local runtime evidence: **Read local summary** → **Read GRE observations**, with the limitations below.

### Read BGP peers

The tool first reads the existing mesh daemon; if that read is unavailable it falls back to its in-process speaker. Success is a peer collection with count and response source. Native peer state is retained. A fallback result does not establish that the daemon has no peers. The daemon branch derives an AS value from a learned path where available; a missing derived value is not evidence of an absent configured peer AS.

### Read BGP routes

The route read returns its local route collection, optional prefix selection, count and response source. Success preserves that source and each returned route. The daemon branch uses exact prefix equality; the in-process branch uses its route lookup method, so prefix filtering is not assumed identical across modes. In-process community output is hard-coded empty in the inspected connector; an empty value cannot establish that the route has no communities.

Unconfigured BGP returns the native configuration error rather than an empty successful RIB. Transport failures can be hidden by fallback; inconsistent sources across peer/RIB reads therefore remain separate observations.

### Read local summary

The summary reads the in-process speaker, not the daemon-preferred BGP view. Success is the reported local configuration flags and any available subresults, including subcomponent errors. At the pinned revision the OSPF initializer passes an incompatible constructor argument to its OSPF speaker and catches the resulting failure. Its unconfigured summary is not evidence that an external OSPF process or router has no adjacency. OSPF neighbor/LSDB reads are consequently not supported by this reference.

The summary attempts JSON decoding of GRE output even when the serializer may use another format. A decode error is a summary limitation, not a GRE failure diagnosis.

### Read GRE observations

The tool collects local tunnel/address command output, filters lines containing GRE and returns those lines with a count. Success is limited to those observations. Exceptions return an error. The implementation does not inspect command return codes; empty output therefore cannot establish that the host has no tunnels or that commands succeeded. No tunnel setup or connectivity conclusion follows from this read.

## Patterns

The server can serialize data with its session/delta GCF encoder and falls back to JSON only when encoding fails. A compatible decoder with the correct session context is required; unreadable output remains unavailable evidence. Local summary and daemon-based reads intentionally cannot be normalized into one authoritative snapshot.

## Known limitations

All mutations are blocked from this conversion. The daemon injection path drops path/local-preference arguments; failed daemon mutations fall back to another speaker, making effects ambiguous. The in-process connector changes a separate dictionary rather than the route store read by its query path. The OSPF cost wrapper ignores its interface selector except for echoing it. These behaviors do not support the source skill's route-advertisement or reconvergence success claims.

This reference documents NetClaw's own publisher-maintained runtime, not a standard protocol-management API. Source: [protocol server](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/protocol-mcp/server.py), [BGP connector](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/protocol-mcp/connectors/bgp_connector.py), [OSPF speaker](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/protocol-mcp/ospfv3/speaker.py), retrieved 2026-10-09. Bindings: [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Read BGP peers | Read daemon-preferred peer state with origin | Read |
| Read BGP routes | Read local routes with origin | Read |
| Read local summary | Read restricted in-process runtime evidence | Read |
| Read GRE observations | Read local GRE-related output lines | Read |

## Verification checklist

- The runtime already exists; no protocol setup or mutation occurred.
- Every BGP result retains daemon/in-process origin.
- Unconfigured, unreadable and incomplete data remain explicit.
- Hard-coded empty values or unchecked shell output are not treated as absence.
- No route advertisement, OSPF convergence or remote-device claim is inferred.
