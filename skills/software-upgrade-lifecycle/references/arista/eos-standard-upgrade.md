# Arista EOS — Standard Upgrade/Downgrade Procedure

Upgrade or downgrade Arista EOS via the **standard** procedure — replacing the EOS image and reloading
the switch — as documented in the Arista EOS User Manual §8.3 "Standard Upgrades and Downgrades." Two
variants: a 5-step single-supervisor procedure and a 4-step dual-supervisor procedure using the
`install` command. This is Arista's own documented alternative to Smart System Upgrade (SSU,
`reload fast-boot`) — use this procedure when SSU isn't needed or isn't available (a downgrade, or an
unsupported platform/config); SSU is a materially different procedure and out of scope here (see Known
limitations). Assumes an authenticated CLI/console session against the target switch with EXEC access,
able to run exec-mode commands, transfer a file to flash (USB/FTP/SCP/HTTP), and detect switch
reachability across a reload.

See Known limitations for a documentation artifact this file corrects.

## Single-Supervisor Switch Procedure (5 steps)

### Step 1 — Prepare the Switch

- **Back up the running config:** `copy running-config flash:/<filename>` (e.g.
  `copy running-config flash:/cfg_06162014`). Confirm: `Copy completed successfully.`
- **Confirm flash space:** `dir flash:` — verify enough free space for **two copies of the target image,
  plus a recommended 240MB** for diagnostic information in case of a fatal error during reload. If
  space is inadequate and the switch reloads anyway, it boots to the Aboot prompt, from which files can
  be deleted from `/mnt/flash` to free space; exiting Aboot restarts the boot process. Prefer catching
  this before reloading rather than recovering from Aboot.
- **Confirm management connectivity:** `show interfaces status` (management interface shows `connected`)
  and `ping <default-gateway>` — confirm reachability before proceeding, since you'll need it to log back
  in after the reload.

### Step 2 — Transfer the Image File (skip if already on flash)

`copy <source> flash:/<destfile>` — source can be:
- USB: `copy usb1:/<sourcefile> flash:/<destfile>`
- FTP: `copy ftp://<user>:<password>@<host>/<sourcefile> flash:/<destfile>`
- SCP: `copy scp://<user>@<host>/<path>/<sourcefile> flash:/<destfile>`
- HTTP: `copy http://<host>/<sourcefile> flash:/<destfile>`

After transfer, confirm the file is present via `dir flash:`, then verify its integrity:
```
verify /md5 flash:<image-filename>
```
Compare the returned MD5 against the value published on the EOS download page for that image — the
source is explicit that this is where the reference checksum comes from, not something computed
locally as a cross-check. **Do not proceed to Step 3 on a checksum mismatch** — re-transfer instead of
trusting a partially-corrupt file.

### Step 3 — Modify boot-config

```
configure terminal
boot system flash:/<image-filename>
show boot-config
write
```

Confirm via `show boot-config` that `Software image:` now points to the target image path before
saving. `write` persists the change to `startup-config` — **do not skip this**; without it, the
boot-config change may not survive as expected across the reload in Step 4 (the source presents `write`
as part of this step, not optional cleanup).

### Step 4 — Reload

```
reload
```

Expected: `The system is going down for reboot NOW!` on any port except the console (the console shows
full rebooting output). **This resets the switch, causing temporary downtime and packet loss on
single-supervisor switches** — this is expected for a standard (non-SSU) reload, not a fault condition.

### Step 5 — Verify

```
show version
```
Confirm the `Software image version:` line matches the target version. Report SUCCESS if it matches;
if it doesn't, report the actual version observed — do not retry the reload automatically.

## Dual-Supervisor Switch Procedure (4 steps)

### Step 1 — Prepare the Switch

- **Confirm you are on the primary (active) supervisor**, not standby:
  ```
  show redundancy status
  ```
  Confirm `my status = Active` (not `STANDBY`). Doing this procedure from the standby supervisor is not
  the documented path.
- **Back up the running config:** `copy running-config <filename>` (destination defaults to flash if no
  prefix given).
- **Confirm flash space on both supervisors:** `dir flash:` (primary) and
  `dir supervisor-peer:mnt/flash/` (standby) — verify enough room on **both** for the new image, not
  just the one you're logged into.
- **Confirm management interfaces on both supervisors are up and reachable** — `show interfaces status`
  and `ping <gateway>` on each. If a management VRF is used, ping the virtual management interface
  (`management 0`), not the physical interface's IP directly.
- **Confirm any extensions running on the active supervisor are also available on the standby** — the
  source calls this out as a required check with no further detail on how to verify per-extension
  availability; if the target platform's extension list isn't already known, confirm with the operator
  rather than assuming parity.

### Step 2 — Transfer the Image File to the Primary Supervisor

Same transfer methods and MD5-verify step as the single-supervisor procedure's Step 2 — transfer lands
on the **primary** supervisor's flash; the `install` command in Step 3 handles propagating it to the
standby.

### Step 3 — Install the New EOS Image

```
install source <image-filename> reload
```
Full command syntax (per §8.4.1): `install source source_path [destination destination_path] [now] [reload]`.
- `source_path` — file path/name of the EOS image; if no path given, the switch looks on the primary
  supervisor's flash.
- `destination destination_path` — optional; defaults to storing under the image's original filename.
- `now` — skip further confirmation prompts.
- `reload` — reload the supervisor(s) after install; **on dual-supervisor switches this reloads both**,
  with control returning to the primary afterward. Omit `reload` only if the intent is to stage the
  image without activating it yet (confirm that's actually the intent before omitting it — an installed-
  but-not-reloaded image has no effect until reloaded).

Run in `configure` mode. Expected sequence output, in order:
```
Preparing new boot-config... done.
Copying new software image to standby supervisor... done.
Copying new boot-config to standby supervisor... done.
Committing changes on standby supervisor... done.
Reloading standby supervisor... done.
Committing changes on this supervisor... done.
Reloading this supervisor...
```
Both supervisors are briefly unavailable during this — `install` is documented as minimizing (not
eliminating) packet loss during the reload, which is expected, not a fault.

**Upgrade both supervisors together, in the same `install ... reload` operation — never leave them on
mismatched image generations.** The source documents a specific disruptive failure mode: due to a
change in supervisor heartbeat timeout, one supervisor booting a post-SSO image (4.10.0-SSO, 4.11.x and
later) while its peer still runs a pre-SSO image causes the pre-SSO supervisor to reload — a disruption
with both supervisors briefly inactive. Using `install ... reload` as documented (both supervisors in
one operation) is exactly what avoids this.

### Step 4 — Verify

```
show version
```
Same confirmation as the single-supervisor procedure: `Software image version:` must match the target.

## Patterns

- **The flash-space check exists because the boot process itself needs the headroom.** EOS copies the
  `.swi` image into internal flash again while booting — this is *why* two copies' worth of space plus
  240MB diagnostic headroom is required, not an arbitrary safety margin. Checking `dir flash:` (and, on
  dual-sup, `dir supervisor-peer:mnt/flash/` too) before transferring is what prevents an Aboot-prompt
  recovery scenario.
- **`install ... reload` is the dual-supervisor equivalent of manual boot-config-then-reload** — it
  folds Steps 3-4 of the single-supervisor procedure (modify boot-config, reload) into one command that
  also handles propagating the image/config to the standby supervisor and sequencing both reloads. Don't
  try to replicate the single-supervisor manual `boot system`/`write`/`reload` sequence on a
  dual-supervisor switch — `install` is the documented path specifically because it avoids the pre/post-
  SSO mismatch failure mode above.
- **MD5 verification's reference value comes from the vendor's download page, not a local computation.**
  There's nothing to compare against without first retrieving the published checksum for that specific
  image — don't skip this step by treating "the file exists and has a plausible size" as sufficient.

## Known limitations

- **Covers the standard image-replace-and-reload procedure only** — not Smart System Upgrade (SSU,
  `reload fast-boot`/`reload hitless`), which is a materially different, lower-downtime procedure using
  graceful-restart protocols, available only on selected platforms and only for upgrades (not
  downgrades). Use SSU instead of this procedure when it's available and applicable — this file doesn't
  cover it.
- **Not applicable to switches participating in MLAG without the separate "Upgrading MLAG Peers"
  procedure** — §8.1 of the source explicitly defers MLAG upgrades to a different section, which was not
  extracted here. Do not attempt this standard procedure on an MLAG peer without that separate guidance.
- **Documentation artifact flagged and excluded, not carried forward:** the source's §8.3.1.1
  ("Preparing the Switch for SSU") subsection — reused verbatim, including its heading, from the SSU
  chapter §8.2.1.1 — contains `show reload fast-boot` verification, BGP graceful-restart configuration,
  and MLAG `reload-delay 0` configuration, all framed around "the SSU process" / "hitless upgrade." None
  of that is applicable to a standard `reload`-based upgrade, which is a full chassis/supervisor reboot,
  not a graceful/hitless restart — a full reload doesn't need BGP graceful-restart pre-configuration the
  way a hitless SSU restart does. These steps were deliberately excluded from Step 1 above rather than
  reproduced; if the target switch is later found to actually need SSU-style handling, that's a signal to
  use the SSU procedure instead of this one, not to add SSU steps into this one.
- No documented auto-abort-timer or rollback-on-timeout mechanism exists for this procedure (unlike
  Cisco IOS-XE install mode's auto-abort timer) — once `reload` (single-sup) or `install ... reload`
  (dual-sup) executes, there is no built-in safety window; recovery from a bad image is manual (boot an
  older image from Aboot, or a subsequent downgrade install).

## Tools

| Mechanism | Description | Category |
|---|---|---|
| CLI/console exec session (SSH or console) | Sends every `show`/`copy`/`verify`/`boot system`/`write`/`reload`/`install` command in this procedure and captures output; must survive the reload to confirm the switch comes back up | Device Access |
| File transfer to flash (USB, FTP, SCP, or HTTP) | Places the target EOS `.swi` image on the primary supervisor's flash before Step 2/3 references it | Device Access |

## Verification checklist

- [ ] `dir flash:` (and, on dual-sup, `dir supervisor-peer:mnt/flash/`) confirmed adequate free space
      before transferring the image — not discovered via an Aboot-prompt recovery after a failed reload
- [ ] `verify /md5` output matched the checksum published on the EOS download page before proceeding
      past the transfer step
- [ ] Single-sup: `show boot-config` confirmed the correct image path, and `write` was run, before
      issuing `reload`
- [ ] Dual-sup: `show redundancy status` confirmed the session was on the primary (Active) supervisor
      before starting; both supervisors were upgraded together via one `install ... reload` operation,
      never left on mismatched pre/post-SSO image generations
- [ ] `show version`'s `Software image version:` line confirmed the target version post-reload
- [ ] If the target switch participates in MLAG or supports SSU for this change, that was flagged to
      the operator rather than silently applying this standard procedure regardless
