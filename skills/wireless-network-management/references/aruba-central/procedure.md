# HPE Aruba Networking Central — WLAN SSID Provisioning and Monitoring Procedure

Create, change, disable, delete, and read WLAN/SSID profiles on access points managed by HPE Aruba
Networking Central. Each operation below names the outcome, the constraints, and the checks, and is
carried out through whichever provisioning or inventory tool the caller has for Central; `endpoints.md`
holds the bindings. Assumes an authenticated session or OAuth 2.0 client for the target account is
available.

Sources: Aruba Central User Guide (ArubaOS 10 AP and Instant AP WLAN chapters, API FAQ) and the HPE
Support Center article "Aruba Central - How to Configure WLAN SSID Profile", retrieved 2026-11-10.

## Operational procedure

### Common Sequences

**Provision a new SSID on a configuration group:**
1. Check Preconditions (group, AP generation, SSID count, forwarding mode, licence).
2. Create the SSID Profile (name, bands).
3. Set VLAN and forwarding.
4. Set Security.
5. Set Access Rules (not for open networks).
6. Review the summary and save, then Verify the SSID.

**Change a live SSID:** Read it first (Get a Specific WLAN), then Edit an SSID Profile, then Verify.

**Take an SSID out of service:** Disable an SSID (keeps the profile, drops clients) or Delete an SSID
Profile (removes it). Prefer disable unless removal is the stated goal.

**Audit or health check (no change):** Get a List of WLANs, then Get a Specific WLAN or Get Throughput
Trend.

### Preconditions

- Profiles are scoped to a configuration group, not to an individual AP. Select a group that
  contains at least one AP; every AP in the group inherits the profile and advertises it.
- Identify the AP generation of the group. ArubaOS 10 groups use the per-SSID wizard described below
  (General, VLANs, Security, Access, Summary). Instant AP groups use a Networks page with
  Employee/Voice/Guest usage types; see Instant AP groups under Patterns.
- Count the group's existing SSIDs against the limit before creating one. The User Guide states up
  to 14 SSIDs per AP, 16 with Extended SSID enabled (System > General). The HPE article for Instant AP
  groups states 6 networks, 16 with Extended SSID. Those two Instant AP figures conflict. Unverified:
  which applies to the target group. Not documented: the error returned when the limit is exceeded;
  stop and report it rather than retrying. More than 16 SSIDs in one zone with the extended-zone
  option off is documented as an error.
- Choose the forwarding mode: bridge (client traffic terminates at the AP and is bridged onto the
  local VLAN), tunnel (traffic goes to an Aruba gateway cluster), or mixed. Tunnel and mixed need a
  primary gateway cluster; a secondary cluster is optional and acts as failover.
- Check the AP licence tier before using different primary clusters for different SSIDs in one group
  (MultiZone; up to 5 clusters and 12 gateways). That needs the advanced licence. On a
  foundation-licence AP, the tunnels on that AP go down when such a configuration is applied. **Stop
  and confirm with the operator before saving a MultiZone SSID in a group that has foundation-licence
  APs, unless standing instructions already authorise it.** Failover between a primary and a secondary
  cluster is fine on foundation.

### Create an SSID Profile

Enter the SSID name and choose the bands: 2.4 GHz, 5 GHz, and 6 GHz (6 GHz only takes effect on
6 GHz-capable APs). Optional advanced settings sit on the same page (broadcast/multicast filtering,
DTIM interval 1–10 beacons default 1, multicast and dynamic multicast optimisation, transmit and
beacon rates, airtime and per-radio bandwidth limits, 802.11n/ac enablement).

Confirm success: the profile appears in the group's Wireless SSIDs table.

### Set VLAN and Forwarding

Choose bridge, tunnel, or mixed. Client VLAN assignment is static (one VLAN ID, optionally picked
by a named VLAN that maps a name to an ID) or dynamic (VLAN derived from the server or from
assignment rules). A dynamic rule matches an attribute with `equals` or `not-equals` against a string
and assigns a VLAN; up to eight rules per SSID. In mixed mode each rule also says whether matching
clients are bridged or tunnelled.

- VLAN 1 is the AP's own native VLAN for the underlay and cannot carry an overlay (tunnel) SSID.
- A VLAN pool (many clients in one subnet) is configured on the gateway side, not in the SSID.

### Set Security

Four security levels; the choice gates which fields apply.

| Level | Key management options | Required for it to work |
|---|---|---|
| Enterprise | WPA2-Enterprise, WPA-Enterprise, both, dynamic WEP with 802.1X, WPA3-Enterprise (CNSA, CCM 128, GCM 256) | A RADIUS server (primary, optional secondary) |
| Personal | WPA2-Personal, WPA-Personal, both, WPA3-Personal, DPP, static WEP, MPSK AES, MPSK Local | Passphrase for the WPA/WPA2/WPA3 options; auth servers for MPSK AES; an MPSK Local profile for MPSK Local |
| Visitors (captive portal) | External captive portal or Cloud Guest | A splash-page profile (external: host/IP, URL, port, HTTPS flag, failure behaviour deny or allow internet) |
| Open | Open or Enhanced Open | Nothing; no access-rule support |

- Passphrase: 8–63 ASCII characters or 64 hex characters. It is only accepted for the WPA/WPA2/WPA3
  personal options; WEP takes a 26-hex-digit key and sizes from drop-downs.
- Enterprise with WPA2 or both and 802.1X: turn on opportunistic key caching (OKC) so roaming
  clients reuse the cached key. OKC is available only at the Enterprise level.
- MAC authentication, if used, can precede 802.1X; a reauthentication interval above zero forces
  periodic re-authentication and is accepted only when MAC authentication is on. Denylisting takes a
  maximum-failures value of 1–10. DHCP enforcement blocks clients that did not obtain an address
  from DHCP.
- Create the RADIUS, LDAP, or dynamic-authorisation server first when none exists; the SSID
  references servers by selection.
- A guest network is typically unencrypted but can carry encryption settings; confirm which is
  intended before saving.

Confirm success: the Security tab saves without a validation error and the summary shows the chosen
level and key management.

### Set Access Rules

Not applicable to open networks. Choose role-based (user roles with per-role rules and a role
assignment rule), network-based (one rule set for everyone; the default rule allows any traffic to
any destination), or unrestricted. Up to 64 access rules per profile. A rule has a service
(network, application, or custom TCP/UDP/Ethernet/other with ports), an action (allow, deny,
destination NAT, source NAT; NAT only with the network service), a destination (any, a server, all
but a server, a network, all but a network, a domain, an AP-local address, or an alias), and options
(802.1 priority 0–7, denylist the client, classify media, disable scanning, DSCP 0–63, log).

A network-based profile keeps the allow-all default unless it is replaced; for guest or restricted
SSIDs, review it before saving.

### Review and Save

The Summary step shows the profile's settings. Saving applies the profile to the group's APs. No
preview or dry run is documented.

### Edit an SSID Profile

Open the profile in the group's Wireless SSIDs table, change it, and save. The display name can also
be renamed in place in the table. **Stop and confirm with the operator before changing security,
VLAN, forwarding, or bands on an SSID serving clients, unless standing instructions already
authorise it.**

- For an existing SSID whose personal key management was changed (for example to WPA2+WPA), re-select
  the intended option before saving; otherwise the change may not take effect.
- On APs running ArubaOS 10.4 or earlier, the configuration pushed to the APs can remain the old
  value even after selecting the new key management. Not documented: how to read the value on a device; treat the change as unconfirmed and report it.

### Disable an SSID

The disconnect action disables the network, so connected clients are dropped, and keeps the profile
(on Instant AP groups the equivalent is the Disable SSID setting). **Stop and confirm with the
operator before disabling an SSID with connected clients, unless standing instructions already
authorise it.**

### Delete an SSID Profile

Removes the profile from the group; the profile removal is confirmed before it applies. **Stop and confirm with the
operator before deleting; the profile is removed and its clients lose the network.**
Recreating needs the full settings again; read them with Get a Specific WLAN first. Unverified:
whether that read returns every setting.

### Verify the SSID

Use Get a List of WLANs (filtered by `site-id` or AP `serial-number` as needed) and confirm the
entry's `status` is `ENABLED` and its security level and VLAN match what was saved. Assumption: the
monitoring view reflects a saved change; the documentation gives no propagation time, so re-check
after a short wait before reporting failure.

### Get a List of WLANs

Lists WLANs for the customer account, optionally filtered by `site-id` or access point
`serial-number`, with an OData-style `filter` (only `and` is supported) and sortable by `wlanName`,
`band`, `status`, `securityLevel`, `security`, or `vlan`. Paginated: default page size 20, max 1000,
cursor continuation via `next`.

Confirm success: the response has an `items` array; each entry's `id` (for example `wlans/wlan1`) is
what a follow-up Get a Specific WLAN needs.

### Get a Specific WLAN

Retrieves full detail for one WLAN by name/ID. Use after a List call has identified it, or directly
if the identifier is known.

### Get Throughput Trend

Two variants: network-wide WLAN throughput trend, or the trend as seen by one access point. Use the
AP-scoped variant when troubleshooting a specific AP's client experience.

## Patterns

- **A profile belongs to a group, so one change reaches every AP in it.** A fix intended for one
  AP's SSID changes all of them; use a separate group for a different SSID set.
- **A profile with no usable security configuration is easy to save by accident.** Enterprise needs
  a RADIUS server, MPSK variants need servers or profiles, and visitor networks need a splash page;
  select or create those first.
- **Instant AP groups:**
  - Network type is chosen at creation: Employee (passphrase or 802.1X), Voice (all client traffic
    is prioritised into the high-priority queue), or Guest (captive portal or passphrase,
    typically unencrypted).
  - A zone setting limits broadcast to APs in that zone. An SSID whose zone matches no AP is not
    broadcast; an SSID with no zone is broadcast by every AP.
  - Dynamic multicast optimisation must be enabled on every SSID in the same VLAN if used on one.
  - Documented defaults: band all, inactivity timeout 60–3600 seconds (default 1000), max clients
    per BSSID 0–255 (default 64), DMO channel-utilisation threshold 90%.
  - The ESSID can differ from the profile name; searches by ESSID then use the ESSID.
- **The `filter` parameter's OData support is limited to `and`.** Fetch broader and filter
  client-side when `or` or grouping is needed.

## Known limitations

- The wire route for the write operations is not published (see `endpoints.md`). That affects only
  which tool performs a step; the steps, gates, and checks here apply unchanged to any tool.
- Covers WLAN SSID profiles on ArubaOS 10 and Instant AP groups. Does not cover wired port profiles,
  RF/radio profiles, group or site management, MPSK key lifecycle, Passpoint, or guest portal splash
  page design beyond selecting a profile.
- The Instant AP SSID limit is documented inconsistently (see Preconditions).
- Rate limits are dynamic per account (documented starting point: 5,000 calls per day, 7 per second);
  back off on HTTP 429 and honour any `Retry-After` header.
- Requires an authenticated session or OAuth 2.0 client in the target account; token setup is out
  of scope.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create SSID profile | Add an SSID profile to a configuration group | WLAN Provisioning |
| Set VLAN and forwarding | Choose bridge/tunnel/mixed and client VLAN assignment | WLAN Provisioning |
| Set security | Choose security level, key management, servers, passphrase | WLAN Provisioning |
| Set access rules | Choose role/network-based or unrestricted rules | WLAN Provisioning |
| Edit SSID profile | Change an existing profile, including rename | WLAN Provisioning |
| Disable SSID | Drop clients and keep the profile | WLAN Provisioning |
| Delete SSID profile | Remove the profile from the group | WLAN Provisioning |
| Get a List of WLANs | List WLANs for the account, filterable by site/AP | WLAN Monitoring |
| Get a Specific WLAN | Read detailed configuration for one WLAN | WLAN Monitoring |
| Get Throughput Trend (WLAN) | Read throughput trend for a WLAN network-wide | WLAN Monitoring |
| Get Throughput Trend (AP-scoped) | Read throughput trend for a WLAN as seen by one AP | WLAN Monitoring |

## Verification checklist

- [ ] The target group, AP generation, SSID count against the limit, forwarding mode, and licence
      tier were checked before creating or changing a profile
- [ ] Security prerequisites (servers, passphrase, splash page, or MPSK profile) existed before the
      profile was saved
- [ ] Confirmation was obtained before editing a live SSID, disabling or deleting one, or saving
      MultiZone on foundation-licence APs, unless standing instructions covered it
- [ ] The saved SSID shows `ENABLED` with the intended security level and VLAN in a follow-up read
- [ ] A changed key management on APs at ArubaOS 10.4 or earlier was checked on the device
- [ ] Pagination (`next`) was followed to completion when a full inventory was needed
- [ ] A WLAN identifier from a List call was used correctly (the `id` field, for example
      `wlans/wlan1`) for any follow-up Get call
