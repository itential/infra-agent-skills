# Cisco ASA — Route-Based IPsec VPN with Virtual Tunnel Interfaces (Static and Dynamic VTI)

Configures a route-based IPsec VPN on a Cisco ASA using a Virtual Tunnel Interface (VTI). Two
shapes exist: a static VTI, bound to one configured peer, and a dynamic VTI, where a hub clones a
per-session virtual access interface from a template so many spokes can share one definition.
Build order is the same either way: IPsec proposal, then IPsec profile, then the tunnel interface
(static) or virtual template plus tunnel group (dynamic).

Scope: create/configure only. The source documents no read, update, or delete procedure, no
verification commands, no error text, and no step for saving the configuration; each is stated
below as unknown rather than filled from general knowledge. Out of scope: the peer's own
configuration, dynamic-routing protocol setup, IP SLA/route tracking, and crypto-map (policy-based)
VPN. Assumes CLI access to the ASA in configuration mode, direct or through an existing
remote-execution capability. This is a CLI-driven procedure: the literal commands below are the
payload sent through that session, and `<angle-bracket>` items are caller-supplied values.

Source: Cisco, "Virtual Tunnel Interface" chapter of the ASA configuration guide (PDF supplied by
the contributor, 14 pages including feature history through ASA 9.19(1)), read 2026-10-06. No
secondary sources. The chapter does not print its guide version or date.

## Applicability checks

- Device must be in single-context, routed mode, and not clustered. Dynamic VTI also lacks support
  for ECMP, VRF, IKEv1, and QoS (inference: dynamic VTI is therefore IKEv2-only; the chapter
  states the exclusions, not that conclusion).
- Release dependence (feature history): dynamic VTI, OSPF/EIGRP over VTI, and loopback interfaces
  as tunnel source or address source arrive in 9.19(1); IPv6 on static VTI and the 1024-VTI ceiling
  arrive in 9.16(1), and releases before that capped the count at 100. The release that first
  introduced static VTI is not in this chapter (unknown). Confirm the target release first.
- VTI count: static VTIs max out at 1024 per device; dynamic virtual access interfaces at 1024 or
  the platform's interface maximum, whichever is smaller. Named subinterfaces count toward the
  total; members of a port-channel do not (only the port-channel itself does). The practical figure
  may be lower still because it cannot exceed the VLAN count the platform supports.
- Address families: IPv4 or IPv6 inside and outside in any combination is accepted, but a given VTI
  runs one tunnel mode (IPv4 or IPv6) and that mode must match the address family configured on
  the VTI. Only static IPv6 addresses work as tunnel source or destination. If the source interface
  holds several IPv6 addresses, one can be chosen as the endpoint, otherwise the first global one
  is used.
- Only IPsec mode exists on a VTI; terminating GRE on the ASA is unsupported.
- Where a VTI uses `ip unnumbered`/`ipv6 unnumbered`, the interface lending its address (the
  "borrow" interface) should not be used as the tunnel source address for any VTI, static or
  dynamic. The chapter's wording is terse; whether "any VTI" means any VTI on the device or only
  the same VTI is not clear (unknown), so avoid the overlap entirely.
- Platform-wide behaviors worth knowing: all VTI traffic is encrypted by default; the VTI security
  level is 0 and cannot be changed; Security Group Tag traffic is discarded once decrypted; NAT in the
  path causes IKE and ESP to be wrapped in UDP; IKE and IPsec SA rekeys are not tied to traffic
  volume, which is how the chapter says VTI tunnels remain permanently up; static, BGP, OSPF, and EIGRP routes can steer traffic into a VTI; ICMP ping works between
  VTI interfaces. The chapter says VTI supports IKEv1 and IKEv2 generally; reading that as
  covering static VTI is an inference, since the dynamic-VTI limits above are listed separately.
- A dynamic VTI hub supports only hub-and-spoke topology; the chapter's wording places this in the
  management-center context, so whether it is a limit of the feature everywhere is unclear.
- Routing caveat for a device that belongs to two VTI domains and runs BGP over a physical
  interface: a state change triggered by the interface health check removes that physical
  interface's routes until BGP re-forms with the new active peer. Logical (VTI) interfaces do not
  show this behavior.

## Operational procedure

1. **Choose static or dynamic VTI and the authentication method.** Authentication is a pre-shared
   key or certificates, configured under the tunnel group the VTI uses (IKEv2 allows a different
   method or key in each direction). For certificates: IKEv1 needs the trustpoint named on the
   initiating end and in the tunnel-group command on the responding end; IKEv2 needs it under the
   tunnel group on both ends (no command syntax for the tunnel-group trustpoint is given — unknown).
   Take any pre-shared key from the caller's secret store; do not hardcode one.

2. **Check for crypto-map conflicts before any dynamic VTI.** Mixing dynamic crypto maps and a
   dynamic VTI for LAN-to-LAN VPNs leaves only the dynamic VTI tunnels working; the chapter's
   explanation is that both mechanisms rely on the default tunnel group. Cisco's remedies: move those VPNs to dynamic VTI, or give static crypto
   maps their own tunnel groups. A VTI and a crypto map may share one physical interface if the
   crypto map's peer differs from the VTI's tunnel destination.
   **Stop and confirm with the operator before adding a dynamic VTI to a device that has crypto-map
   LAN-to-LAN tunnels; those tunnels may stop coming up.**

3. **Create the IPsec proposal.** The chapter gives two forms; pick by IKE version.
   - IKEv1 transform set:
     `crypto ipsec ikev1 transform-set <set-name> <encryption> <authentication>`
     Encryption: `esp-aes` (128-bit), `esp-aes-192`, `esp-aes-256`, `esp-null`.
     Authentication: `esp-md5-hmac`, `esp-sha-hmac`, `esp-none`.
   - IKEv2 IPsec proposal:
     `crypto ipsec ikev2 ipsec-proposal <proposal-name>` then, in that submode,
     `protocol esp encryption <algorithm> [<algorithm> ...]` (aes, aes-192, aes-256, aes-gcm,
     aes-gcm-192, aes-gcm-256, null) and
     `protocol esp integrity <algorithm> [<algorithm> ...]` (sha-1, sha-256, sha-384, sha-512, null).
     The chapter's worked example pairs aes-gcm-256 encryption with null integrity. Whether null
     integrity is valid with non-GCM encryption, and whether the integrity line is mandatory, is
     not stated (unknown).
   If an object with the chosen name already exists, the chapter does not say what re-entering it
   does. **Stop and confirm with the operator before reusing an existing name, since a live
   profile may reference it.**

4. **Create the IPsec profile and attach the proposal.**
   `crypto ipsec profile <profile-name>`, then in profile submode one of
   `set ikev1 transform-set <set-name>` or `set ikev2 ipsec-proposal <proposal-name>`.
   Optional profile settings, each in profile submode:
   - SA lifetime: `set security-association lifetime {seconds <number> | kilobytes {<number> | unlimited}}`.
     The chapter's example puts seconds and kilobytes on one line. Defaults and ranges are not
     given (unknown).
   - PFS: `set pfs group14`. Both peers must agree on the DH group. Only group14 is shown; other
     accepted groups are unknown.
   - Certificate for initiating tunnels: `set trustpoint <trustpoint-name>`.
   - Reverse route injection with a dynamic reverse route: `set reverse-route dynamic`
     (the keyword is optional in the syntax `set reverse-route [dynamic]`).
   - Initiation control: `responder-only` makes this end wait for the peer rather than start the
     tunnel or rekey. Profile-mode entry is an assumption (the chapter prints no prompt). Guidance
     by situation:
     - IKEv2: give the responder-only side a longer SA lifetime than the initiator's profile
       so the initiator can complete rekeys.
     - IKEv1 against an IOS peer: IOS is the side that should be responder-only, because it lacks
       continuous-channel mode; the ASA then initiates and rekeys.
     - Peer's rekey configuration not known: two documented fallbacks are removing responder-only
       (so either end may start SA setup) or giving the responder-only end an infinite IPsec
       lifetime (so its SA never ages out).

5. **Static VTI: create the tunnel interface.**
   ```
   interface tunnel <tunnel-id>
    nameif <interface-name>
    ip address <ip-address> <subnet-mask>
    tunnel source interface <source-interface-name>
    tunnel destination <peer-ip-address>
    tunnel mode ipsec ipv4
    tunnel protection ipsec profile <profile-name>
   ```
   - Instead of a fixed address, the interface can reuse another interface's address with
     `ip unnumbered <interface-name>` or `ipv6 unnumbered <interface-name>` (physical or loopback).
     The chapter's static-section text for this repeats the dynamic template's wording (a source
     defect); it is applied here as the same option per the feature history. Whether it is
     exclusive of `ip address` is unknown.
   - The tunnel source can be a physical or loopback interface.
   - IPv6: assumed `tunnel mode ipsec ipv6` (the chapter prints the ipv4/ipv6 choice only for the
     dynamic template).
   - Optional traffic selector: an extended ACL, e.g.
     `access-list <acl-name> extended permit ip <source> <source-mask> <destination>`, applied with
     `tunnel protection ipsec policy <acl-name>`. Without it the VTI offers any-to-any selectors.
     The chapter's syntax line omits `ipsec` (`tunnel protection policy`) while its example and
     feature history include it; the `ipsec` form is used here.
   - Tunnel ID: the chapter prints 0 to 10413 and says up to 10413 VTIs, contradicting its 1024
     static-VTI limit. Follow 1024 and confirm against the target release.

6. **Dynamic VTI: create the virtual template.** Prerequisite: the IPsec profile and the
   interface whose address will be borrowed already exist.
   ```
   interface virtual-Template <template-number> type tunnel
    nameif <interface-name>
    ip unnumbered <interface-name>        (or: ipv6 unnumbered <interface-name>)
    tunnel source interface <source-interface-name>
    tunnel mode ipsec {ipv4 | ipv6}
    tunnel protection ipsec profile <profile-name>
   ```
   - The template must not be shut down. Name, IPsec mode, and IPsec profile are the required
     parts; the borrowed address comes from any physical or loopback interface and is shared by
     every virtual access interface cloned from the template.
   - Number range printed is 1 to 10413, probably the same inflated figure as the tunnel ID range
     in step 5 (not confirmed); the real ceiling is release-dependent per the applicability checks.
   - Cloned interfaces are named `<template-nameif>_va<n>` (e.g. `dVTI101_va1`) and are removed
     when the session ends.
   - `tunnel source interface` is optional. Set it to restrict the ASA to accepting sessions on
     that one interface; cloned interfaces then take their MTU from it. Omit it and sessions are
     accepted on any interface, with MTU taken from whichever interface received the request, and
     IKEv2 is switched on across all interfaces except management-only and failover ones.
   - Changing an existing template requires `shutdown` on it first. Inference (not stated): this
     ends sessions built from that template. **Stop and confirm with the operator before modifying
     a live template.**

7. **Dynamic VTI: link the template to a tunnel group and set route exchange.**
   ```
   tunnel-group <tunnel-group-name> type <type>
   tunnel-group <tunnel-group-name> ipsec-attributes
    virtual-template <template-number>
    ikev2 route set interface
    ikev2 route accept any
   ```
   The chapter's example uses type `ipsec-l2l`. One template may serve several tunnel groups.
   `ikev2 route set interface` makes the ASA announce its VTI address in IKEv2 so the two VTI
   addresses can reach each other, which BGP and path monitoring need. `ikev2 route accept any`
   takes the peer's announced address and is on by default. A routing policy for the dynamic-VTI
   traffic and an access rule for the encrypted traffic are still needed; no commands for either
   are given (unknown).

8. **IKE-side settings.** Shown only in the chapter's worked IKEv2 static-VTI example, not as
   steps. IKEv1 IKE-policy syntax is not shown anywhere (unknown). Example algorithm choices are
   illustrative, not required values.
   ```
   crypto ikev2 policy <policy-number>
    encryption <algorithm>
    integrity <algorithm>
    group <dh-group>
    prf <prf-algorithm>
    lifetime seconds <number>
   tunnel-group <peer-ip-address> ipsec-attributes
    ikev2 remote-authentication pre-shared-key <pre-shared-key>
    ikev2 local-authentication pre-shared-key <pre-shared-key>
   crypto ikev2 enable <interface-name>
   ```
   The tunnel-group name has to equal the IKE identity the peer sends. For IKEv1 site-to-site, a
   name that is not an IP address is allowed when authentication is by certificate and/or the peer
   is set to aggressive mode. Whether the example's tunnel-group line needs a `type` is not stated (unknown).

9. **Traffic filtering.** ACLs can be attached to a VTI. Two device-wide commands can alter
   filtering: `sysopt connection permit-vpn` skips ACL evaluation for IPsec traffic, and
   `same-security-traffic permit intra-interface` lets same-level traffic hairpin, which is
   needed for an ACL on the level-0 VTI to take effect when the outside interface is also level 0
   (`permit` keyword assumed from the standard form; the chapter names only the intra-interface
   argument). **Stop and confirm with the operator before enabling either; both loosen filtering
   across the whole device, not just this tunnel.**

10. **Peer requirement.** The remote device needs a matching IPsec proposal and profile. If an
    IKEv2 peer includes configuration-request payloads, the ASA cannot bring the tunnel up; turn
    that off on the peer (on an IOS peer, `no config-exchange request` in its IKEv2 profile).
    Negotiation starts once all parameters exist on both ends.

11. **Saving the configuration** is not covered by the source (unknown). Consult platform guidance
    before assuming changes survive a reload.

12. **Confirm the outcome** (see Verification).

## Changing a live VTI (disruptive actions the chapter mentions)

- **MTU.** The VTI's MTU follows its physical interface when the VTI is enabled. After the
  physical MTU changes, the VTI must be disabled and enabled again. Commands are not printed;
  interface `shutdown`/`no shutdown` is assumed. Inference: disabling drops the tunnel until it is
  re-enabled. **Stop and confirm with the operator before disabling the VTI.**
- **BFD on a static VTI.** If the neighbor will not come up while the interface carries both IPv4
  and IPv6 addresses, Cisco's fix is to remove the tunnel interface and recreate it with one
  address type. Inference: removal tears down the live tunnel. **Stop and confirm with the operator
  before removing the tunnel interface.** BFD is enabled only on the tunnel interface (static) or
  the tunnel group (dynamic), never additionally as a BGP neighbor for the same overlay neighbor,
  and the DPD interval should be 60 seconds or more, increasing with the number of BFD tunnels.

## Verification

The chapter provides no inspection commands, expected output, or error strings.

- Commands to display IKE/IPsec SAs, VPN sessions, or dynamic virtual access interfaces are not in
  the source (unknown). Do not report the tunnel as established from configuration entry alone;
  use platform-specific guidance for state.
- Pinging between the two VTI addresses is a reasonable reachability probe (the chapter says only
  that ping is supported; using it as a check is an inference).
- Dynamic VTI: expect one `_va<n>` interface per active session.

## Known limitations

- Create/configure only; read, update, and delete are undocumented in the source.
- Source defects/inconsistencies: the 0-10413 tunnel ID and 1-10413 template ranges versus the
  1024 limit; the static `ip unnumbered` text pasted from the dynamic section; the two spellings
  of the traffic-selector command (see step 5).
- Unrestricted/unknown: lifetime defaults and ranges, PFS groups beyond group14, tunnel-group
  certificate syntax, IKEv1 IKE-policy syntax, routing-policy and access-rule commands.
- Not covered: IP SLA/static route tracking (the chapter suggests it to keep a tunnel up when the
  router in the active path is down, and points to the ASA general operations guide), peer
  configuration, and the 9.17 local-tunnel-ID/Umbrella SIG feature.
- Disruptive or loosening steps, each gated above: dynamic VTI beside crypto maps, reusing an
  existing name, modifying a virtual template, disabling a VTI for MTU, removing a tunnel
  interface, enabling ACL bypass or intra-interface traffic.

## Tools

An authenticated CLI/console session (SSH or console) to the target ASA in configuration mode.
Commands in this file are payload sent through that session, not separate tools.

| Operation | Description | Category |
|---|---|---|
| Run a command on the ASA | Send configuration commands from this file over an authenticated CLI session | Execution/transport |

## Verification checklist

- [ ] ASA is single-context, routed, non-clustered, and its release supports the chosen features
- [ ] Crypto-map conflict checked before adding a dynamic VTI, with operator confirmation
- [ ] Proposal, profile (proposal attached), and tunnel interface or virtual template plus tunnel
      group configured, with matching parameters on the peer
- [ ] Pre-shared key (if any) came from the caller's secret store
- [ ] No interface used as an `ip unnumbered` address donor is also a VTI tunnel source
- [ ] Any MTU disable/enable, interface removal, template change, name reuse, or device-wide
      filtering option was confirmed with the operator first
- [ ] Tunnel state confirmed from the ASA's own SA/session state (command unknown in this source);
      optional ping between VTI addresses succeeded
- [ ] Config persistence handled per platform guidance (not in this source)
