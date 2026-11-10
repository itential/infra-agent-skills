# Wireless Network Management — Platform Index

One row per supported wireless-management platform. Each platform directory holds its own
`procedure.md` (capability language, per the REST convention) and `endpoints.md` (literal wiring).

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| Cisco Meraki | `meraki/` | SSID provisioning (configure a numeric slot 0-14 — no create/delete op exists), update, disable | **No create-SSID endpoint at all** — same PUT call for create/update/disable. Cross-checked against a real, delivered Itential production build (`projects/meraki-ssid-provisioning/`), which live-verified two facts beyond the vendor docs: `8021x-radius` hard-requires a RADIUS server, and the PUT response doesn't always echo `vlanId` even when applied. |
| HPE Aruba Networking Central | `aruba-central/` | SSID profile create, edit, disable, delete on ArubaOS 10 and Instant AP groups (VLAN/forwarding, security, access rules); WLAN listing, detail, and throughput monitoring | Reads use the New Central REST API; the write operations are bound to the caller's provisioning tool (no REST route is documented). The Instant AP SSID limit is documented inconsistently (6 vs 14). MultiZone SSIDs need the advanced AP licence; on foundation-licence APs their tunnels go down. |
| Cisco Catalyst Center | `catalyst-center/` | Create and provision an SSID (fabric or non-fabric, one call), fabric SSID-to-VLAN mapping | Asynchronous — every write returns a task/execution identifier that must be polled to confirm actual completion. The VLAN-mapping call is destructive on omission (an unlisted VLAN's existing mappings are cleared), the opposite of typical partial-update semantics. |

**Cross-vendor asymmetry:** Meraki and Catalyst Center document a write API. Aruba Central documents
no REST route for SSID writes, so its write operations bind to the caller's provisioning tool; the
procedure is the same either way.
