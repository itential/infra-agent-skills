# IPAM Allocation — Platform Index

One row per supported IPAM platform. Each platform directory holds its own `procedure.md` (the full
step-by-step) plus wire-level `endpoints.md` where applicable.

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| NetBox | `netbox/` | Create aggregate/prefix, allocate a child prefix, allocate an IP — under the IPAM app only | REST API. Migrated from `automation-skills`' `netbox_ipam_prefix_allocation` skill; re-verified current against NetBox 4.5/4.6 docs before migrating. |
| Infoblox NIOS | `infoblox/` | Network/subnet carve-out from a network container, IP reservation — via WAPI `next_available_network`/`next_available_ip` | REST-like WAPI. Distinct from `dns-record-management/infoblox/`, which covers DNS records only — this file is IPAM-only. Field names for the nested-function form differ across WAPI versions; confirm against the target Grid Master. |
| SolarWinds | `solarwinds/` | Get first available IP, reserve/finish/cancel an IP reservation, create a subnet | **SOAP/verb-invocation (SWIS), not REST** — the one platform in this category with a fundamentally different call mechanism (`Invoke-SwisVerb`, not HTTP methods). Reservations have a default 10-minute expiry window — a real commit-gate pattern, not an immediate allocate. |
| Nautobot | `nautobot/` | List/allocate a child prefix from a parent prefix; list/allocate the next free IP in a prefix — IPAM app only | REST API. Namespace-based model (Nautobot 2.x). Allocation-call details come from a secondary source (generated schema) and are marked unverified; exhaustion behavior is not documented. Distinct from NetBox; the object models differ. |
| Micetro (Men and Mice) | `micetro/` | List available address blocks (optional temporary claim), create a range, get next free address | REST API. Address space only — Micetro's DNS and DHCP features are not covered here and never merged with `dns-record-management/` or `dhcp-scope-management/`. Most call details come from a secondary source (generated definition) and are marked unverified. |
| phpIPAM | `phpipam/` | Create a subnet in a section, carve the first free child subnet of a mask from a parent, allocate the first free IP or create a chosen IP, read subnet usage, find a subnet by CIDR — subnets and addresses controllers only | REST API, each request under an API-app path segment. Allocation is immediate on the write call (no reservation step). Response behavior for an exhausted pool is not documented — `phpipam/procedure.md` marks it unknown. Deleting a subnet cascades to its addresses; deletion is out of scope. |

There is no single wire standard grounding IPAM across vendors the way RFC 1035 grounds DNS — each
platform's allocation model (NetBox's aggregate/prefix hierarchy, Infoblox's network-container carve-out,
SolarWinds' reserve-then-finish flow) is a product design decision, not a shared spec. `SKILL.md`
therefore states shared IPAM vocabulary (parent/child address-space hierarchy, allocation vs.
reservation, pool exhaustion) rather than RFC-derived rules.

**A genuinely different call mechanism, found adding SolarWinds:** every other platform in this index
(and in `dns-record-management`) is REST/HTTP. SolarWinds IPAM is SOAP-style verb invocation
(`Invoke-SwisVerb <namespace> <method> <args>`) — there's no GET/POST/PUT/DELETE distinction to map
against. `SKILL.md`'s "Tools" section states this per-platform rather than assuming REST universally,
and `solarwinds/procedure.md` says so explicitly up front rather than forcing REST-shaped language onto
a non-REST API.

Only two vendors in this index document an explicit time-boxed hold (SolarWinds reservations, Micetro temporary claims); the other platforms allocate immediately on the allocate call. `SKILL.md`'s "allocation and reservation are not always the same" concept named only SolarWinds, so it was reworded to include Micetro's optional temporary claim; no other shared concept needed correcting.
