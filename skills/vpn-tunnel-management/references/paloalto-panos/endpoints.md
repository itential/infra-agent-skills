# Endpoints/Fields — Palo Alto Networks PAN-OS IPsec VPN

Literal field names, documented option lists, and defaults. `procedure.md`'s steps reference these
by name; bind them to whichever concrete tool the calling agent has (web UI, PAN-OS XML API, or
`set`/`edit` CLI configuration commands) — this skill does not assume one specific transport.
Source: PAN-OS Networking Administrator's documentation (Network Security / IPsec VPN
administration), current version, docs.paloaltonetworks.com, retrieved 2026-09-17.

## IKE Crypto Profile fields

- **DH Group** — one of: `group1`, `group2`, `group5`, `group14`, `group19`, `group15` (IKEv2 only),
  `group16` (IKEv2 only), `group20`, `group21` (IKEv2 only).
- **Authentication (hash) algorithm** — one of: `md5`, `sha1`, `sha256`, `sha384`, `sha512`, or
  `non-auth`.
- **Encryption algorithm** — one of: `des`, `3des`, `aes-128-cbc`, `aes-192-cbc`, `aes-256-cbc`,
  `aes-128-gcm` (requires IKEv2 and DH Group `group19`), `aes-256-gcm` (requires IKEv2 and DH Group
  `group20`). `des` is documented as available on PAN-OS 10.1.0 and earlier only.
- **Key Lifetime** — a duration in seconds, minutes, hours, or days; documented range is 3 minutes
  to 365 days; documented default is 8 hours.
- **IKEv2 Authentication Multiple** — an integer 0-50; documented default is 0. Multiplies the Key
  Lifetime to derive the interval at which the gateway re-authenticates (as distinct from rekeying).

## IPSec Crypto Profile fields

- **IPsec Protocol** — `ESP` (encryption plus authentication) or `AH` (authentication only, no
  encryption).
- **Encryption algorithm (ESP)** — one of: `des`, `3des`, `aes-128-cbc`, `aes-192-cbc`,
  `aes-256-cbc`, `aes-128-gcm`, `aes-128-ccm`, `aes-256-gcm`.
- **Authentication algorithm** — one of: `md5`, `sha1`, `sha256`, `sha384`, `sha512`.
- **DH Group (PFS)** — one of: `group1`, `group2`, `group5`, `group14`, `group15`, `group16`,
  `group19`, `group20`, `group21`, or `no-pfs` to disable Perfect Forward Secrecy.
- **Lifetime** — a duration in seconds, minutes, hours, or days; documented range is 3 minutes to
  365 days. An exact on-box default was not independently confirmed in the source reviewed for this
  skill — confirm the current default on the target firewall rather than assuming a specific value.
- **Lifesize** — a data-volume threshold after which the SA must rekey. Units and default were not
  independently confirmed in the source reviewed — treat as an explicit unknown rather than assuming
  a value; consult the target firewall's own configuration or current PAN-OS documentation before
  setting one deliberately.

## IKE Gateway fields

- **Name** — object identifier.
- **Version** — `IKEv1 only mode`, `IKEv2 only mode`, or `IKEv2 preferred mode` (attempts IKEv2 first
  and falls back to IKEv1 if the peer doesn't support it).
- **Address Type** — `IPv4` or `IPv6`.
- **Interface** — the local physical/outgoing interface the gateway terminates on.
- **Local IP Address** — the local tunnel endpoint address (documented as the external-facing,
  publicly routable interface address in the typical case).
- **Peer IP Address Type** — `IP`, `FQDN`, or `Dynamic` (no fixed peer address known in advance).
- **Peer Address** — the corresponding value for the selected Peer IP Address Type.
- **Authentication** — `Pre-Shared Key` or `Certificate`.
  - Pre-Shared Key path: **Pre-shared Key** value (documented maximum length 255 characters);
    **Local Identification** and **Peer Identification**, each one of `FQDN`, `IP address`, `KEYID`,
    or `User FQDN`.
  - Certificate path: **Local Certificate** (select existing, import, or generate new);
    **Local Identification** — one of `Distinguished Name`, `FQDN`, `IP address`, or `User FQDN`;
    **Peer Identification** — same option set; **Peer ID Check** — `Exact` or `Wildcard`;
    **Certificate Profile** — references how the peer's certificate is validated.
- **IKE Crypto Profile** — reference to a profile defined per the IKE Crypto Profile fields above.
- **Passive Mode** — boolean; when enabled the gateway only responds to IKE negotiation and never
  initiates it.
- **NAT Traversal** — boolean; enables UDP encapsulation of IKE/IPsec traffic for a path with a NAT
  device between the two endpoints. Exact validation/error behavior when enabled unnecessarily (no
  NAT present) was not independently confirmed in the source reviewed.

## IPsec Tunnel object fields

- **Name** — object identifier.
- **Tunnel Interface** — the tunnel interface (new or existing) this object binds to.
- **Type** — `Auto Key` (uses an IKE Gateway plus an IPSec Crypto Profile for automatic SA
  negotiation) or `Manual Key` (operator supplies encryption/authentication keys directly, plus a
  protocol choice and Local SPI/Remote SPI values — no IKE negotiation at all).
- **IKE Gateway** (Auto Key only) — reference to the IKE Gateway object.
- **IPSec Crypto Profile** (Auto Key only) — reference to the IPSec Crypto Profile object.
- **Tunnel Monitor** — requires the tunnel interface to have an assigned IP address.
  - **Destination IP address** — a reachable address on the far side of the tunnel, used for an ICMP
    liveness check.
  - **Profile** — defines the firewall's action if the monitor detects the tunnel down.
- **Proxy IDs** (policy-based deployments) — each entry:
  - **Local** — local IP address or subnet.
  - **Remote** — remote address/subnet.
  - **Protocol** — `Number` (a specific protocol ID), `Any` (covers TCP/UDP), `TCP` (with an optional
    port), or `UDP` (with an optional port).
  - Documented default proxy ID for a route-based VPN (i.e., when none is explicitly configured) is
    local `0.0.0.0/0`, remote `0.0.0.0/0`, protocol `any`.
- **Show Advanced Options**:
  - **Enable Replay Protection** — boolean; anti-replay via sequence numbers and a sliding window.
  - **Anti-Replay Window** — one of `64`, `128`, `256`, `512`, `1024` (documented default), `2048`,
    `4096`.
  - **Copy TOS Header** — boolean; copies the inner IP header's Type-of-Service value to the outer
    (encapsulating) IP header.
  - **IPSec Mode** — documented default `Tunnel`; explicitly selectable.
  - **Add GRE Encapsulation** — boolean; wraps payload in GRE before IPsec encryption, for multicast
    or other cases GRE-over-IPsec is specifically needed for.

## Operational CLI commands (verification/troubleshooting)

See `procedure.md`'s Verification section for how each of these fits into the overall procedure and
its own confirmation-gate requirements for the destructive ones.

- `show vpn ike-sa` / `show vpn ike-sa gateway <gateway-name>` / `show vpn ike-sa tunnel <tunnel>`
- `show vpn ipsec-sa`
- `show vpn gateway`
- `show vpn tunnel`
- `show vpn flow`
- `show running tunnel flow info`
- `test vpn ike-sa gateway <gateway-name>` / `test vpn ipsec-sa tunnel <tunnel-name>`
- `clear vpn ike-sa gateway <gateway-name>` / `clear vpn ike-sa tunnel <tunnel-name>` / `clear vpn
  ipsec-sa tunnel <tunnel-name>` — destructive; see `procedure.md`'s confirmation-gate requirement
- `debug ike global on` (output to `ikemgr.log`), `debug ike pcap on` / `debug ike pcap off`

No specific machine-parseable success/failure string or exit-code vocabulary for these commands (or
for the config-side create/update/delete operations, however the calling tool executes them) was
found in the source reviewed for this skill — surface the executing tool's own output/exit status
verbatim rather than asserting an error string this research didn't confirm.
