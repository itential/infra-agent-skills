# Juniper SRX (Junos OS) — Route-Based IPsec VPN Tunnel Configuration Procedure

Creates, reads, updates, and deletes a route-based, autokey-IKE, site-to-site IPsec VPN tunnel on an
SRX Series firewall running Junos OS: the IKE proposal/policy/gateway (phase 1), the IPsec
proposal/policy/VPN object (phase 2), and the secure tunnel (`st0`) interface the VPN binds to. Does
not cover policy-based VPNs (the older model where a security policy names the tunnel directly rather
than routing to it), remote-access/dial-up VPN, Auto Discovery VPN or hub-and-spoke Next-Hop Tunnel
Binding, certificate/PKI issuance, or the security-zone/security-policy configuration that permits
traffic across an established tunnel. Assumes CLI access to the target SRX device (direct or through
an existing remote-execution capability) in configuration mode. Source: Juniper's Junos OS
Networking/VPN-IPsec documentation (`security-route-based-ipsec-vpns`,
`security-ipsec-vpn-configuration-overview`, `security-secure-tunnel-interface-in-a-virtual-router`,
and the CLI statement reference for `security ike`/`security ipsec` proposal fields),
juniper.net/documentation, current release documentation, retrieved 2026-09-17.

Junos itself documents IPsec VPN negotiation as occurring in two phases: Phase 1 establishes a
secure channel used to negotiate the IPsec security association, and Phase 2 negotiates the IPsec
SA that will actually authenticate/encrypt the tunnel's traffic — this procedure follows that same
two-phase structure.

## Operational procedure

1. **Configure the underlying interfaces, security zones, and routing before the VPN objects
   themselves.** A route-based VPN depends on: the physical/outgoing interface that will carry
   encrypted traffic (assigned to an "untrust"-style zone permitting the `ike` host-inbound
   service, and `ping` if operational reachability testing is wanted), the internal-facing interface
   toward protected hosts (assigned to a "trust"-style zone), and a secure tunnel interface unit
   (`st0.<unit>`) assigned to its own zone (commonly a dedicated VPN zone). A static or dynamic route
   toward the remote site's protected subnet, with the `st0` unit as next hop, is what actually
   routes traffic into the tunnel for a route-based VPN — this is the mechanism that distinguishes
   route-based from policy-based: the security policy only needs to permit zone-to-zone traffic, not
   name the tunnel itself.
2. **Confirm the `st0` interface unit number and addressing choice.** A secure tunnel (`st0`)
   interface supports exactly one IPv4 address and one IPv6 address at a time — this is documented as
   applying to every route-based VPN on the platform, not a per-deployment choice. The `disable`
   option is not supported on `st0` interfaces. Units `st0.16000` through `st0.16385` are reserved
   for Multinode High Availability and chassis-cluster HA control-link encryption and are not
   user-configurable — pick a unit number in the `st0.0`-`st0.15999` range for a user tunnel. If the
   tunnel needs to run in a non-default routing instance (virtual router), the `st0` unit can be
   placed there directly; note the documented overlap rule: an IKE external-interface address must
   not overlap across virtual routers, an internal/trust interface address may overlap across virtual
   routers, and an `st0` address may overlap across virtual routers only for point-to-point tunnels,
   not for point-to-multipoint (hub-and-spoke/NHTB) tunnels.
3. **Configure the IKE proposal (phase 1 algorithm set)** under `[edit security ike]`:
   `set security ike proposal <name> authentication-method <method>`, plus
   `authentication-algorithm`, `encryption-algorithm`, `dh-group`, and `lifetime-seconds` as needed —
   see `ike-ipsec-proposal-fields.md` for the documented option lists. A predefined proposal set
   (Junos ships `Standard`, `Compatible`, and `Basic` predefined sets per the configuration overview)
   can be referenced instead of building a custom proposal, and is a reasonable default when the
   peer's exact required algorithm set isn't already known.
4. **Configure the IKE policy (phase 1 policy)**: `set security ike policy <name> mode <main|
   aggressive>`, `set security ike policy <name> proposals <proposal-name[,...]>`, and — for
   pre-shared-key authentication — `set security ike policy <name> pre-shared-key ascii-text
   <key>` (or `hexadecimal <key>`). Main mode is the standard, more secure choice; aggressive mode
   trades some identity protection for fewer round trips and should only be used when a specific
   peer requires it.
5. **Configure the IKE gateway (phase 1 peer definition)**: `set security ike gateway <name>
   ike-policy <policy-name>`, `set security ike gateway <name> address <peer-ip-or-fqdn>`, and
   `set security ike gateway <name> external-interface <interface-name>` (the local, outgoing
   interface the gateway is anchored to). Set local/remote IKE identification (local-identity/
   remote-identity) if the peer requires an identity other than its IP address. Unverified: the exact
   `version` keyword values (e.g. an IKEv1-only vs. IKEv2-only vs. either selector) on a current
   SRX-scoped page, so this step does not assert specific keywords; consult the target device's own
   command-completion help (`set security ike gateway <name> version ?`) to confirm the accepted
   values before scripting against them.
6. **Configure the IPsec proposal (phase 2 algorithm set)** under `[edit security ipsec]`:
   `set security ipsec proposal <name> protocol <ah|esp>`, plus `authentication-algorithm`,
   `encryption-algorithm`, `lifetime-seconds`, and `lifetime-kilobytes` as needed — see
   `ike-ipsec-proposal-fields.md` for the documented option lists (ESP is the standard choice,
   providing both confidentiality and authentication; AH provides authentication only).
7. **Configure the IPsec policy (phase 2 policy)**: `set security ipsec policy <name> proposals
   <proposal-name[,...]>`, and, if Perfect Forward Secrecy is required, `set security ipsec policy
   <name> perfect-forward-secrecy keys <group>`.
8. **Configure the IPsec VPN object and bind it to the tunnel interface**:
   `set security ipsec vpn <name> ike gateway <gateway-name>`,
   `set security ipsec vpn <name> ike ipsec-policy <ipsec-policy-name>`,
   `set security ipsec vpn <name> bind-interface st0.<unit>`, and
   `set security ipsec vpn <name> establish-tunnels immediately` (to bring the tunnel up as soon as
   the configuration commits) or leave `establish-tunnels` unset/on-traffic if the tunnel should only
   negotiate when matching traffic actually appears.
9. **Commit the configuration**: `commit` (or `commit confirmed <minutes>` if the calling procedure's
   own change-management practice calls for an auto-rollback safety net — this skill does not itself
   mandate one, since that is a site-specific practice, not a documented Junos VPN requirement).
10. **Confirm the configuration was applied as intended** with `show security ike` and
    `show security ipsec` from configuration mode before considering the change complete — compare
    the displayed hierarchy against what was intended to be set.
11. **Confirm phase 1 and phase 2 actually negotiated** — see Verification below. A successful commit
    only means the configuration was accepted; it does not mean the tunnel is up.
12. **Update an existing tunnel** by issuing additional `set` statements against the same object
    names (Junos configuration statements are idempotent set-and-replace, not append-only) and
    committing again. Changing a proposal's algorithms does not retroactively affect an SA already
    negotiated under the old parameters — see Known limitations.
13. **Delete a tunnel, gateway, or interface binding.** **Stop and confirm with the operator before
    running any `delete security ike gateway ...`, `delete security ipsec vpn ...`, `delete
    interfaces st0 ...`, or equivalent removal of a routing statement that currently carries live
    traffic through the tunnel** — each of these tears down the live tunnel path or removes the means
    to re-establish it. Not documented in the sources: a worked example of the exact `delete`
    command sequence for these objects (the source example used only `set`); the
    `delete <hierarchy>`-mirrors-`set` pattern is a well-established general Junos CLI convention,
    unverified against a VPN-object-specific example — confirm the exact hierarchy path against the target device's own configuration (`show
    security ike` / `show security ipsec` output) before issuing the delete, rather than assuming the
    object name alone is sufficient without matching the real configured hierarchy.

## Verification

Run these from operational mode:

- `show security ike security-associations` — lists active phase 1 (IKE) SAs: index, state (`UP` or
  `DOWN`), initiator/responder cookie, mode, and remote address. No SA listed for the target gateway
  means IKE didn't establish — check the IKE policy, external interface, and reachability before
  assuming a phase 2 problem.
- `show security ike security-associations index <index> detail` — phase 1 SA detail: role
  (initiator/responder), exchange type, authentication method, negotiated algorithms, remaining
  lifetime, traffic statistics, and count of IPsec SAs created under this IKE SA.
- `show security ipsec security-associations` — lists active phase 2 (IPsec) SAs: ID, algorithm,
  SPI, remaining lifetime (seconds/kilobytes), VPN-monitoring status column (`-` not enabled, `U` up,
  `D` down), and gateway. A total-active-tunnels/total-SAs summary line appears at the top.
- `show security ipsec security-associations index <id> detail` — phase 2 SA detail per direction:
  local/remote identity (this is the phase 2 proxy ID — the source notes a proxy-ID mismatch as one
  of the most common causes of IPsec failure; the documented default for a route-based VPN is local
  `0.0.0.0/0`, remote `0.0.0.0/0`, service `any`), bind-interface, SPI, hard/soft lifetime remaining,
  mode, protocol, and algorithms, plus a running tunnel-events history log useful for diagnosing a
  specific negotiation failure reason recorded by the device itself.
- `show security ipsec statistics index <id>` (or the unscoped `show security ipsec statistics` for
  all SAs) — ESP/AH encrypted/decrypted byte and packet counters, plus error counters (authentication
  failures, replay errors, decryption failures, malformed headers/trailers) — useful once the SA is
  confirmed up but traffic still isn't flowing as expected.
- A basic end-to-end reachability check (e.g. `ping <remote-host> rapid count 100` from an actual
  host behind the tunnel, not the SRX itself) that fails while the SA shows `UP` points to a routing,
  security-policy, or NAT problem rather than an IKE/IPsec negotiation problem.
- If no SA appears at all and negotiation appears stuck, the source recommends reviewing the `kmd`
  log or enabling trace options as the next diagnostic step, rather than assuming a specific fixable
  cause without further evidence.

## Known limitations

- Covers route-based, autokey-IKE, site-to-site VPN only — policy-based VPN, remote-access/dial-up
  VPN, Auto Discovery VPN, and hub-and-spoke NHTB are each documented as distinct configurations with
  their own considerations and are out of this procedure's scope.
- Unverified: the exact `version` keyword values available on
  `set security ike gateway <name> version` against a current SRX-scoped source — consult the target
  device's own command-completion help rather than assuming specific keyword values from this
  procedure.
- The exact Diffie-Hellman group list available on current SRX/Junos releases is only partially
  confirmed — `group1`, `group2`, `group5`, and `group14` are documented on a dedicated `dh-group`
  statement reference page, but that page's scope (whether it's the current SRX-era page or an
  older one) is unverified; additional higher groups may be supported on current releases but are
  unconfirmed. Confirm the full accepted
  value list against the target device's own command-completion help before relying on a specific
  higher DH group (e.g. group19-group21) being available.
- Exact `delete` command sequences for removing IKE/IPsec objects are not documented in a worked
  example in the sources — see step 13; the general Junos `set`/`delete` symmetry convention is well
  established but unverified for this specific object type.
- Changing a proposal's algorithms does not retroactively renegotiate an already-established SA; the
  existing SA continues under its originally negotiated parameters until it naturally rekeys or is
  explicitly cleared.
- Exact default lifetime/lifesize numeric values for the IPsec proposal were not independently
  confirmed in the sources — confirm current defaults on the target device
  rather than assuming a specific number.

## Tools

CLI-driven: the literal Junos `set`/`delete`/`show`/`commit` configuration statements and the
operational-mode `show security ike`/`show security ipsec` commands are the payload passed to a
generic "run a command on this device" capability — there is no separate per-operation API tool to
bind against, per this repo's convention for CLI-driven procedures. See
`ike-ipsec-proposal-fields.md` for the field/option reference used when constructing the `set`
statements in steps 3-8.

## Verification checklist

- [ ] `st0` unit number confirmed within the user-configurable range (`st0.0`-`st0.15999`) and its
      IPv4/IPv6 addressing confirmed as at most one of each
- [ ] IKE gateway's authentication method, identity, and external-interface settings deliberately
      chosen, not left at a guessed/default value
- [ ] Proposal algorithm choices confirmed against `ike-ipsec-proposal-fields.md`'s documented option
      lists rather than assumed from general IKE/IPsec knowledge
- [ ] Configuration committed, and `show security ike security-associations` / `show security ipsec
      security-associations` both confirmed the SA state as `UP`/active before reporting the tunnel
      as operational — configuration commit success alone was not treated as sufficient
- [ ] Any `delete` of an IKE gateway, IPsec VPN object, `st0` interface, or routing statement carrying
      live tunnel traffic was confirmed with the operator first
