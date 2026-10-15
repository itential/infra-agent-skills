# Palo Alto Networks PAN-OS — IPsec VPN Tunnel Configuration Procedure

Creates, reads, updates, and deletes a route-based (and, where noted, policy-based) site-to-site
IPsec VPN tunnel on a PAN-OS firewall: the IKE Gateway (phase 1) object, the IKE Crypto Profile, the
IPSec Crypto Profile, the IPsec Tunnel object (phase 2), and its associated tunnel interface. Does
not cover GlobalProtect remote-access VPN, certificate/PKI issuance, or the firewall's separate
security-policy/NAT configuration needed to actually permit traffic across the tunnel — those are
out of scope. Assumes an authenticated management-plane client for the target firewall (Panorama-
managed or standalone) is already available, whether operated through the web UI, the PAN-OS XML
API, or the operational CLI. Source: PAN-OS Networking Administrator's documentation (Network
Security / IPsec VPN administration guide), current version, docs.paloaltonetworks.com, retrieved
2026-09-17.

## Operational procedure

1. **Confirm the tunnel interface exists (or create one) and note its zone/virtual-router
   assignment.** A PAN-OS tunnel interface does not itself require an IP address to route traffic
   between the two sites — an address is only needed if tunnel monitoring or a dynamic routing
   protocol will run over the tunnel. The interface must belong to a security zone (the documentation
   recommends a dedicated VPN zone rather than reusing an existing trust/untrust zone) and to a
   virtual router — keep the tunnel interface in the same virtual router as the physical interface
   carrying the encrypted traffic, per the source's own recommendation.
2. **Define or select an IKE Crypto Profile** (the phase 1 algorithm set): choose a Diffie-Hellman
   group, an authentication (hash) algorithm, an encryption algorithm, and a key lifetime. See
   `endpoints.md` for the full option lists as documented (DH groups, hash algorithms, encryption
   algorithms including which require IKEv2 and a specific DH group) and the documented lifetime
   range/default. Also set the IKEv2 "Authentication Multiple" value if periodic reauthentication
   (as a multiple of the key lifetime) is wanted; the documented default disables it.
3. **Define or select an IPSec Crypto Profile** (the phase 2 algorithm set): choose the IPsec
   protocol (ESP for confidentiality plus authentication, or AH for authentication only), an
   encryption algorithm, an authentication algorithm, and a Diffie-Hellman group for Perfect Forward
   Secrecy (or explicitly no PFS). See `endpoints.md` for the full documented option lists. The exact
   default lifetime/lifesize values were not independently confirmed for the on-box configuration
   interface in the source reviewed for this skill — confirm the current default against the target
   firewall's own configuration rather than assuming a specific number, and set an explicit value if
   the requirement is anything other than "whatever the platform defaults to."
4. **Create the IKE Gateway object** (phase 1 peer definition):
   - Select the IKE version mode: IKEv1-only, IKEv2-only, or IKEv2-preferred (falls back to IKEv1 if
     the peer doesn't support IKEv2).
   - Set the local address type/interface and the local IP address — the source describes this as
     the external-facing, publicly routable interface address that terminates the tunnel locally.
   - Set the peer address type (a static IP, an FQDN, or "Dynamic" for a peer without a fixed
     address) and the corresponding peer address value.
   - Choose an authentication method: pre-shared key (set the key value and the local/peer IKE
     identification type — FQDN, IP address, KEYID, or User FQDN) or certificate-based (select/
     import/generate the local certificate, set local/peer identification, choose exact or wildcard
     peer-ID matching, and reference a certificate profile that defines how the peer's certificate is
     validated).
   - Reference the IKE Crypto Profile from step 2.
   - Set Passive Mode only if this gateway must never initiate the IKE exchange itself (it will only
     respond to the peer's initiation). Enable NAT Traversal only if a NAT device sits between the
     two tunnel endpoints; exact validation behavior for this setting was not independently confirmed
     in the source reviewed — treat as "enable when a NAT is known to be in the path," not as a
     default-on setting.
5. **Create the IPsec Tunnel object** (phase 2 / the tunnel itself):
   - Reference the tunnel interface from step 1.
   - Choose the key-exchange type: Auto Key (uses the IKE Gateway from step 4 plus the IPSec Crypto
     Profile from step 3 to negotiate SAs automatically — the standard case for a peer that also
     supports IKE) or Manual Key (requires manually entering the encryption/authentication keys, a
     protocol choice, and local/remote SPI values directly — used only when the peer cannot run IKE
     at all; treat as an unusual, higher-operational-burden path rather than the default choice).
   - If tunnel monitoring is wanted, assign the tunnel interface an IP address (per step 1) and set a
     monitoring destination IP (a reachable address on the far side of the tunnel) plus a monitor
     profile defining the firewall's action if monitoring detects the tunnel is down.
   - For a policy-based deployment only, configure Proxy IDs (local subnet, remote subnet, and a
     protocol restriction — a specific protocol number, "any" covering TCP/UDP, or TCP/UDP with a
     port). Route-based deployments (the tunnel selected by a routed destination through the tunnel
     interface, not by a named policy) do not require Proxy IDs for basic operation; the source's own
     default route-based proxy ID is a 0.0.0.0/0-to-0.0.0.0/0-any match under the covers, so leaving
     Proxy IDs unset relies on that default rather than omitting phase 2 traffic selection entirely.
   - Leave advanced options (replay protection and its window size, TOS-header copy, IPsec mode, GRE
     encapsulation) at their documented defaults unless a specific requirement calls for changing
     them — see `endpoints.md` for the documented option values and defaults.
6. **Commit the configuration.** PAN-OS configuration changes made via the web UI or XML API are
   staged (candidate configuration) until committed; the tunnel is not active on the data plane
   until a commit succeeds. Report the tunnel as configured-but-not-yet-active until commit
   completes, and as active only once phase 1/phase 2 state is separately confirmed (step 8).
7. **Update an existing tunnel** by editing the relevant object's fields (IKE Gateway, IPSec Tunnel,
   or either Crypto Profile) the same way as creation, then committing. Changing a Crypto Profile's
   algorithm set does not retroactively renegotiate an SA already established under the old
   parameters — the tunnel continues under the prior negotiated parameters until it naturally rekeys
   or is explicitly cleared (step 9's clear commands) to force renegotiation.
8. **Confirm phase 1 and phase 2 status separately** — see Verification below. Do not report a
   tunnel as "up" from configuration success alone.
9. **Delete a tunnel or gateway.** **Stop and confirm with the operator before deleting an IPsec
   Tunnel object, an IKE Gateway, or a tunnel interface that currently has an active SA** — removing
   any of these drops the live traffic path through that tunnel. This skill's sources did not
   document delete-specific field behavior beyond the general PAN-OS object-management pattern
   (remove the object, then commit); this procedure does not assert a vendor-documented delete
   confirmation dialog or safeguard beyond the commit step itself, so the confirmation gate here is
   this procedure's own required step, not a platform-enforced one. Forcing an existing SA down
   without deleting the configuration is a separate, also-disruptive action — see the `clear vpn`
   commands in Verification, and gate those the same way.

## Verification

Run these from the firewall's operational-mode CLI (or the equivalent via the calling tool's own
operational-command mechanism):

- `show vpn ike-sa` — lists phase 1 (IKE) security associations; use to confirm phase 1 negotiation
  actually completed for the target gateway, not just that the gateway object exists.
- `show vpn ike-sa gateway <gateway-name>` — phase 1 SA detail scoped to one gateway.
- `show vpn ipsec-sa` — lists phase 2 (IPsec) security associations; use to confirm the tunnel itself
  is up, as distinct from phase 1 alone being established.
- `show vpn ipsec-sa tunnel <tunnel-name>` is not independently confirmed as valid syntax in the
  source reviewed for this skill — the source instead shows `show vpn ike-sa tunnel <tunnel>` (phase
  1, scoped by tunnel) and a separate `show vpn flow`/`show vpn tunnel` pairing for phase 2/tunnel
  listing; use `show vpn tunnel` to list configured auto-key tunnels and `show vpn flow` for
  IPsec traffic counters rather than assuming an unconfirmed command variant works.
- `show vpn gateway` — lists configured IKE gateways.
- `show running tunnel flow info` — basic traffic statistics across all VPN tunnels.
- `test vpn ike-sa gateway <gateway-name>` / `test vpn ipsec-sa tunnel <tunnel-name>` — actively
  triggers negotiation; useful to confirm a newly created tunnel can establish, but treat as an
  active network operation (it sends real IKE/IPsec negotiation traffic), not a passive check.
- `clear vpn ike-sa gateway <gateway-name>` / `clear vpn ike-sa tunnel <tunnel-name>` / `clear vpn
  ipsec-sa tunnel <tunnel-name>` — **stop and confirm with the operator before running any of
  these**: each forcibly tears down an existing SA (forcing renegotiation from scratch), dropping
  in-flight traffic through that SA in the process. This skill's source describes these in the
  context of IKEv1 troubleshooting specifically; their exact behavior against an IKEv2-only gateway
  was not independently confirmed — verify against the target firewall's own documentation for its
  running PAN-OS version before relying on them in an IKEv2-only environment.
- `debug ike global on` (with output reviewed in the `ikemgr.log`) and `debug ike pcap on`/`off` —
  deeper negotiation-level troubleshooting; treat as a diagnostic step for a tunnel that fails to
  establish via the above checks, not a routine verification step.

## Known limitations

- Does not cover GlobalProtect remote-access VPN configuration, certificate/PKI lifecycle, or the
  security-policy/NAT rules required to actually permit traffic across an established tunnel — a
  tunnel configured per this procedure can be fully up at the IKE/IPsec level and still pass no
  traffic if policy doesn't permit it (see `firewall-management` for that layer).
- Manual Key IPsec (no IKE) is documented as an option but treated here as an unusual path — this
  procedure does not detail its SPI/key-management operational burden beyond noting it exists.
- Exact default lifetime/lifesize values for the IPSec Crypto Profile, and the precise validation
  behavior of the IKE Gateway's NAT Traversal setting, were not independently confirmed against the
  on-box configuration interface in the source reviewed — confirm current defaults on the target
  firewall rather than assuming the values found during this skill's research.
- The `clear vpn ike-sa`/`clear vpn ipsec-sa` operational commands are documented in this skill's
  source in an IKEv1 troubleshooting context; whether they apply unchanged to an IKEv2-only gateway
  was not confirmed — verify before relying on them against an IKEv2-only deployment.
- A committed configuration change is not the same fact as an established tunnel — always confirm
  phase 1 and phase 2 state separately per Verification before reporting a tunnel as operational.

## Tools

| Operation | Description | Category |
|---|---|---|
| IKE Crypto Profile create/read/update/delete | Phase 1 algorithm set (DH group, hash, encryption, lifetime) | Network → Network Profiles |
| IPSec Crypto Profile create/read/update/delete | Phase 2 algorithm set (protocol, encryption, authentication, PFS group) | Network → Network Profiles |
| IKE Gateway create/read/update/delete | Phase 1 peer definition (address, auth method, identity, crypto profile reference) | Network → Network Profiles / IKE Gateways |
| IPsec Tunnel create/read/update/delete | Phase 2 tunnel object (interface binding, IKE gateway reference, IPSec crypto profile reference, proxy IDs) | Network → IPSec Tunnels |
| Tunnel interface create/read/update/delete | Logical interface bound to a zone and virtual router | Network → Interfaces → Tunnel |
| Commit | Pushes candidate configuration to the data plane | Device operations |

See `endpoints.md` for the literal field names, documented option lists, and defaults per object.

## Verification checklist

- [ ] Tunnel interface confirmed assigned to a security zone and virtual router before referencing it
      from an IPsec Tunnel object
- [ ] IKE Gateway's authentication method (pre-shared key vs. certificate) and identity fields set
      deliberately, not left at a guessed default
- [ ] Crypto Profile algorithm choices confirmed against `endpoints.md`'s documented option lists,
      including any IKEv2-only encryption-algorithm/DH-group pairing requirement
- [ ] Configuration committed, and phase 1 (`show vpn ike-sa`) and phase 2 (`show vpn ipsec-sa`/
      `show vpn tunnel`) state confirmed separately before reporting the tunnel as up
- [ ] Any `clear vpn ike-sa`/`clear vpn ipsec-sa` command, or deletion of a gateway/tunnel/tunnel
      interface with an active SA, was confirmed with the operator first
