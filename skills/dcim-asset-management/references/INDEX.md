# DCIM Asset Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| NetTerrain (Graphical Networks) | `netterrain/` | Create/read/update/delete a device asset, including rack-unit mount and dismount; create/read/update/delete a rack container | WAPI v1 REST interface; bearer-token auth required for writes, basic auth is vendor-restricted to read-only calls; device/rack records are typed specializations of a broader generic "node" object |

**NetBox boundary:** NetBox ships both a DCIM module (racks, devices, power) and an IPAM module. If NetBox
is listed here, it covers only the DCIM object model; its IPAM coverage stays in `ipam-allocation`
(`netbox/`) and is cross-referenced from this row's Notes instead of duplicated.
