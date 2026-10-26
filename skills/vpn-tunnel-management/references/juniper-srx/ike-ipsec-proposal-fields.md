# Field Reference — Juniper SRX (Junos OS) IKE/IPsec Proposal Options

Literal statement syntax and documented option lists for the IKE and IPsec proposal-level statements
referenced from `procedure.md` steps 3 and 6. Source: Junos OS CLI Reference (statement pages
`authentication-algorithm (Security IKE)`, `dh-group`, `encryption-algorithm (Security IKE)`,
`proposal (Security IPsec)`), juniper.net/documentation, retrieved 2026-09-17.

This file is a field reference for the Junos CLI statements used in `procedure.md`; Junos here is
CLI-driven, so there is no wire-level REST/API to document.

## IKE proposal — `[edit security ike proposal <name>]`

- `authentication-method` — one of `pre-shared-keys`, `rsa-signatures`, `dsa-signatures` (per the
  legacy M/T-series proposal page; the modern SRX-era proposal path has no single consolidated
  statement page in the sources, so this specific option list should be
  confirmed against the target device's own command-completion help before being treated as
  exhaustive for current SRX releases).
- `authentication-algorithm` — documented values: `md5`, `sha1`, `sha-256`, `sha-384` (from the
  current, non-M/T-series-scoped `authentication-algorithm (Security IKE)` statement page).
- `dh-group` — documented values from the dedicated `dh-group` statement page: `group1` (768-bit),
  `group2` (1024-bit), `group5` (1536-bit), `group14` (2048-bit). Unverified: whether this
  specific page's scope includes the higher groups (`group15`,
  `group16`, `group19`, `group20`, `group21`) that other platforms in this same skill document as
  IKEv2-capable options — treat those higher groups as unconfirmed for Junos in this procedure and
  verify via the target device's own command-completion help before relying on one.
- `encryption-algorithm` — documented values: `aes-128-cbc`, `aes-128-gcm` (IKEv2 only; when used,
  configure `aes-128-gcm` at `[edit security ipsec proposal <name>]` instead and do not also set
  `authentication-algorithm` at the IKE proposal level), `aes-192-cbc`, `aes-256-cbc`, `aes-256-gcm`
  (IKEv2 only; same co-configuration note as `aes-128-gcm`, using `[edit security ipsec proposal
  <name>]`), `chacha20-poly1305` (IKEv2 only, for control-plane security; documented as unsupported
  on the SRX1500 platform specifically). `3des-cbc` and `des-cbc` are documented as still present but
  marked "NOT RECOMMENDED" in CLI help text starting in a Junos OS release using the IKED daemon with
  the `junos-ike` package installed — avoid choosing either for a new configuration.
- `lifetime-seconds` — a numeric value in seconds; Unverified: the exact documented range/default
  for the modern SRX proposal statement — confirm
  against the target device's own configuration or current documentation.

## IKE policy — `[edit security ike policy <name>]`

- `mode` — `main` (standard, protects peer identities during the exchange) or `aggressive` (fewer
  round trips, exchanges identity/hash payloads unprotected — use only when a specific peer requires
  it).
- `proposals` — one or more IKE proposal names (or a predefined set name — Junos documents
  `Standard`, `Compatible`, and `Basic` predefined proposal sets per the configuration overview
  page, usable in place of a custom proposal).
- `pre-shared-key` — `ascii-text <key>` or `hexadecimal <key>`, for pre-shared-key authentication.

## IKE gateway — `[edit security ike gateway <name>]`

Fields confirmed directly from the worked configuration example in `procedure.md`'s source:
`ike-policy <policy-name>`, `address <peer-ip-or-fqdn>`, `external-interface <interface-name>`. The
source's separate configuration-overview page additionally describes setting local/remote IKE
identification when the remote gateway's IP isn't known in advance, and selecting an IKE version —
exact statement/keyword syntax for identification and version is not documented on a dedicated
statement-reference page in the sources; confirm exact keywords via the target
device's own command-completion help (`set security ike gateway <name> ?`) before scripting against
them.

## IPsec proposal — `[edit security ipsec proposal <name>]`

Documented values, from the current (SRX-era) `proposal (Security IPsec)` statement page:
- `protocol` — `ah` or `esp`.
- `authentication-algorithm` — `hmac-sha-256-128`, `hmac-sha-256-96` (documented as non-RFC-compliant
  — the source separately notes that for Multinode High Availability link encryption, a commit fails
  if the proposal specifies `hmac-sha1-96`, and the same restriction applies to standalone VPN
  configuration at the same hierarchy level), `hmac-sha-384`, `hmac-sha-512`.
- `encryption-algorithm` — `aes-128-cbc`, `aes-128-gcm`, `aes-192-cbc`, `aes-192-gcm`, `aes-256-cbc`,
  `aes-256-gcm`, `chacha20-poly1305`. The source notes that updating this value on an existing
  proposal causes the device to delete existing IPsec SAs using that proposal (a disruptive,
  immediate-effect change, unlike updating the IKE-proposal-level `encryption-algorithm`, which the
  same source describes as not deleting existing SAs).
- `extended-sequence-number` — a flag enabling Extended Sequence Number (ESN) support.
- `lifetime-kilobytes` — numeric data-volume threshold for rekeying.
- `lifetime-seconds` — numeric time threshold for rekeying.

## IPsec policy — `[edit security ipsec policy <name>]`

- `proposals` — one or more IPsec proposal names (or a predefined set name, same `Standard`/
  `Compatible`/`Basic` convention as IKE).
- `perfect-forward-secrecy keys <group>` — enables PFS using the specified Diffie-Hellman group for
  the phase 2 rekey exchange; omit entirely to leave PFS disabled.

## IPsec VPN object — `[edit security ipsec vpn <name>]`

Fields confirmed directly from the worked configuration example in `procedure.md`'s source:
`bind-interface <st0-unit>`, `ike gateway <gateway-name>`, `ike ipsec-policy <ipsec-policy-name>`,
`establish-tunnels immediately`. The source's configuration-overview page also references specifying
proxy IDs as part of phase 2 negotiation and a `df-bit` setting observed in the worked example's own
`show security ipsec` detail output (`DF-bit: clear`) but not documented at the
statement-reference level in the sources — confirm exact syntax and accepted values for
proxy-ID and `df-bit` configuration via the target device's own command-completion help before
scripting against them.
