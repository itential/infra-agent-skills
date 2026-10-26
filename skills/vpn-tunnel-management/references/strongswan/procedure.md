# strongSwan — IPsec/IKE Tunnel Configuration Procedure

Creates, reads, updates, and deletes a site-to-site (or host-to-host) IPsec tunnel on a strongSwan
IKE daemon (`charon`) using the current `swanctl` control utility and its `swanctl.conf` connection
definition file. Does not cover the legacy `ipsec.conf`/`starter`/`pluto` toolchain, EAP/XAuth
remote-access profiles, or certificate/PKI provisioning — those are separate procedures. Assumes
shell access to the strongSwan host (local or via an existing remote-execution capability) with
permission to edit files under the swanctl configuration directory (commonly `/etc/swanctl`) and to
run `swanctl` against the running `charon` daemon.

Scope note: strongSwan is open-source software, not a single vendor appliance — "the tunnel" here is
a `swanctl.conf` connection (an IKE_SA definition) plus one or more of its child `CHILD_SA`
definitions (the IPsec-level policy/SA, analogous to what other platforms label an IPsec phase 2 or
a proxy-ID/traffic-selector set). Sources: strongSwan documentation, `swanctl.conf`(5) reference and
the `swanctl`(8) command reference, both at docs.strongswan.org, version 5.9 line, retrieved
2026-09-17.

## Operational procedure

1. **Identify or assign a connection name and, per tunnel, a child name.** A `swanctl.conf`
   `connections` section holds one IKE-level configuration (the connection) per name, and each
   connection can define one or more `children` subsections (each an independent CHILD_SA / IPsec
   tunnel sharing that IKE_SA). Confirm which existing connection (if any) an update/delete targets
   before proceeding — see `swanctl --list-conns` under Verification below.
2. **Build or edit the `connections.<conn>` block** with the IKE-level (phase 1-equivalent)
   parameters:
   - `version` — `0` (accept either as responder, initiate as IKEv2; the strongSwan-documented
     default), `1` for IKEv1/ISAKMP only, or `2` for IKEv2 only.
   - `local_addrs` / `remote_addrs` — the local and peer tunnel endpoint addresses (single
     addresses, DNS names, CIDR subnets, or ranges are all accepted).
   - `proposals` — the offered IKE algorithm set(s): each proposal is a dash-separated combination
     of encryption algorithm, integrity algorithm, PRF, and Diffie-Hellman group (AEAD ciphers
     collapse encryption+integrity into one combined-mode keyword); multiple proposals are
     comma-separated. The keyword `default` requests strongSwan's own built-in, broadly
     interoperable proposal rather than a hand-picked algorithm list — a reasonable starting point
     if the peer's exact supported algorithm set isn't already known, but confirm it satisfies any
     externally mandated cipher policy before relying on it.
   - `local.auth` / `remote.auth` — authentication method for each side (`psk` for a pre-shared key,
     `pubkey` for certificate-based, or an EAP/XAuth method for remote-access scenarios out of this
     procedure's scope).
   - `local.id` / `remote.id` — the IKE identity each side presents/expects.
   - `rekey_time` — how often the IKE_SA itself is rekeyed (IKEv2 only; IKEv1 instead relies on
     `reauth_time`-driven reauthentication). Leave at the documented default unless a specific
     interval is required — see Known limitations for the interaction between `rekey_time` and
     `reauth_time`.
3. **Store the shared secret separately, if using PSK authentication.** Pre-shared keys are defined
   in the `secrets` section of `swanctl.conf` (or a file included by it), not inline in the
   `connections` block — keep this file's permissions restricted, since it holds the tunnel's
   authentication material in cleartext on disk.
4. **Add one or more `children.<child>` blocks** under the connection for the IPsec-level (phase
   2-equivalent) definition:
   - `local_ts` / `remote_ts` — the traffic selectors (CIDR subnet plus optional protocol/port) each
     side will send/accept through this CHILD_SA. The special value `dynamic` (the default) resolves
     to the tunnel's own outer address or negotiated virtual IP rather than a fixed subnet — set
     explicit subnets for a site-to-site tunnel carrying more than host-to-host traffic.
   - `esp_proposals` — the offered ESP algorithm set(s), same dash/comma syntax as the IKE-level
     `proposals`. Note strongSwan's own documented caveat: for an IKEv2 connection, the first
     CHILD_SA created alongside the IKE_SA always derives its keys from the IKE_SA's key material
     regardless of any Diffie-Hellman group specified here — a DH group set on `esp_proposals` only
     takes effect on a later rekey or a separately negotiated CHILD_SA, so a proposal mismatch on
     that group may not surface immediately.
   - `mode` — `tunnel` (the default) for a standard site-to-site tunnel; `transport` or the other
     documented modes (`transport_proxy`, `beet`, `pass`, `drop`) are for the narrower scenarios each
     is intended for and out of this procedure's default scope.
   - `start_action` — whether this child is established automatically. The documented default,
     `none`, does nothing on load; use `start` to initiate immediately on load, `trap` to install an
     on-demand trap policy that negotiates when matching traffic appears, or `trap|start` for both.
5. **Load the configuration into the running daemon.** Run `swanctl --load-all` (or the narrower
   `swanctl --load-conns` / `swanctl --load-creds` if only connections or only credentials changed)
   to have `charon` re-read `swanctl.conf` and any included secrets/credential files. This step does
   not itself bring a tunnel up — see step 6.
6. **Bring the tunnel up (create/read the live state).** If `start_action` isn't already `start` or
   `trap|start`, initiate it explicitly with `swanctl --initiate --child <child-name>` (add
   `--ike <conn-name>` if the child name alone is ambiguous across connections). Confirm the
   resulting state per Verification below before reporting success — a loaded configuration and an
   established SA are two different facts, and this procedure's own sources make that same
   distinction (a loaded connection with no active SA is normal until traffic or an explicit
   initiate triggers negotiation, depending on `start_action`).
7. **Update an existing tunnel by editing its `swanctl.conf` block and reloading.** strongSwan has no
   separate "in-place edit" call distinct from create — change the relevant `connections.<conn>` or
   `children.<child>` keys in the file and run `swanctl --load-all` again. A change to `proposals`/
   `esp_proposals` or other negotiated parameters does not retroactively alter an already-established
   SA; the existing SA continues under the old parameters until it rekeys or is explicitly
   re-initiated. If the change must take effect immediately rather than at the next natural rekey,
   **stop and confirm with the operator before terminating the live SA** (step 8) to force
   renegotiation under the new parameters — this drops in-flight traffic through the tunnel.
8. **Delete/tear down a tunnel.** Two distinct actions exist, and the correct one depends on intent:
   - To take down the live SA(s) without removing the configuration (e.g. to force renegotiation, or
     as a temporary stop): **stop and confirm with the operator before proceeding**, then run
     `swanctl --terminate --child <child-name>` (or `--ike <conn-name>` to tear down the whole IKE_SA
     and every child under it). This is disruptive to any traffic currently using the tunnel.
   - To remove the tunnel's configuration entirely: remove its `connections.<conn>` (and/or
     `children.<child>`) block from `swanctl.conf`, then run `swanctl --load-conns` so the daemon
     drops the definition. **Stop and confirm with the operator before removing a connection that
     currently has an active SA** — reloading connections does not by itself terminate an existing
     SA built from the removed definition, but leaves the running tunnel orphaned from any
     configuration that could recreate or manage it going forward; terminate it explicitly (previous
     bullet) as part of the same confirmed change if full teardown is intended.

## Verification

- `swanctl --list-conns` — lists the connection definitions currently loaded in the daemon; use this
  to confirm a create/update actually loaded before checking live state, and to confirm a delete's
  configuration-removal step took effect.
- `swanctl --list-sas` — lists currently active IKE_SAs (and, nested under each, their CHILD_SAs).
  Treat a target connection/child appearing here as the fact that a tunnel is actually established
  ("up"), not just configured — this procedure's own source material explicitly distinguishes
  "loaded configuration" from "active SA," and reporting one as if it were the other is a status
  error, not a rounding difference.
- No documented single "success" exit code or output string beyond a subcommand completing normally
  was found in the sources; if the executing tool surfaces `swanctl`'s exit
  status or stderr output, report that verbatim on failure rather than inferring a specific error
  condition that wasn't independently confirmed against the source documentation.

## Known limitations

- This procedure was written against `swanctl`/`swanctl.conf`, strongSwan's current, documented
  control interface — the legacy `ipsec.conf`/`starter`/`stroke` toolchain uses different file and
  command syntax entirely and is out of scope here.
- Does not cover EAP/XAuth-based remote-access VPN profiles, certificate/PKI issuance and rollover,
  IPComp compression tuning, or Postquantum Preshared Key (PPK) configuration — each is a documented
  but separate feature area from the base site-to-site tunnel this procedure covers.
- **`rekey_time` and `reauth_time` interact**: per the source, if `reauth_time` is set on a
  connection, `rekey_time` defaults to `0` (rekeying disabled) unless also set explicitly — a
  connection intended to both reauthenticate and rekey needs both values set, not just one.
- Exact CLI exit codes and machine-parseable error strings for `swanctl` subcommands were not found
  in the documentation; error handling here relies on the executing tool's
  own captured stderr/exit status rather than a documented error vocabulary.
- Editing a live connection's negotiated parameters does not retroactively change an already
  established SA — see step 7; forcing immediate effect requires an explicit, confirmed terminate.

## Tools

CLI-driven: the literal `swanctl` command (and direct edits to the `swanctl.conf` file and included
credential/secrets files) is the payload passed to a generic "run a command on this host" / "edit a
file on this host" capability — there is no separate per-operation API tool to bind against, per
this repo's convention for CLI-driven procedures.

## Verification checklist

- [ ] Target connection name (and child name, if the connection has more than one) confirmed against
      `swanctl --list-conns` before an update or delete
- [ ] Pre-shared keys or other credential material placed in the `secrets` section/file, never inline
      in the `connections` block, and that file's permissions restricted
- [ ] After loading configuration, live state confirmed via `swanctl --list-sas` rather than assuming
      a loaded connection is an established tunnel
- [ ] Any `swanctl --terminate` (tearing down a live SA) or removal of a connection/child with an
      active SA was confirmed with the operator first — both are disruptive to live traffic
- [ ] Outcome reported using "loaded" vs. "established/up" as genuinely distinct states, matching
      this procedure's own status vocabulary
