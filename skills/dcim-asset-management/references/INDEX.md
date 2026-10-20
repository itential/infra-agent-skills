# DCIM Asset Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full step-by-step),
plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| NetTerrain (Graphical Networks) | `netterrain/` | Create/read/update/delete a device asset, including rack-unit mount and dismount; create/read/update/delete a rack container | WAPI v1 REST interface; bearer-token auth required for writes, basic auth is vendor-restricted to read-only calls; device/rack records are typed specializations of a broader generic "node" object |
| NetBox | `netbox/` | Create/read/update/delete a device record (including rack, position, face) and a rack record | REST API; related objects by id or identifying attributes; bulk writes are all-or-none; IPAM side lives in `ipam-allocation` (`netbox/`) |
| Nautobot | `nautobot/` | Create/read/update/delete a device record (including rack, position, face) and a rack record | REST API; UUID identifiers; device-name uniqueness is instance-configured; Nautobot IPAM is out of scope here |

**NetBox boundary:** NetBox ships both a DCIM module (racks, devices, power) and an IPAM module. This
skill covers only NetBox's DCIM object model; its IPAM coverage stays in `ipam-allocation` (`netbox/`)
and is cross-referenced from this row's Notes instead of duplicated.
