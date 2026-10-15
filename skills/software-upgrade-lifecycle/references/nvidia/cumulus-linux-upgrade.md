# NVIDIA Cumulus Linux — Upgrade Procedures

Upgrade Cumulus Linux via one of three documented methods — **Optimized Image Upgrade**, **Package
Upgrade**, or **ONIE Image Upgrade** — each with materially different scope, destructiveness, and ISSU
support. Confirm which method applies before starting; they are not interchangeable, and choosing wrong
(especially reaching for ONIE when a non-destructive method would do) has real consequences (see the
comparison table below). Assumes an authenticated CLI/console session against the target switch with
sudo/NVUE access, able to run `nv` (NVUE) and Linux CLI commands, transfer/fetch an image file over the
network or from local storage, and detect switch reachability across a reboot.

## Method comparison (confirm which applies before proceeding)

| Aspect | Optimized Image | Package Upgrade | ONIE Image |
|---|---|---|---|
| ISSU support | Yes | Yes | No |
| Configuration preserved | Yes | Yes | **No — destructive** |
| Reboot count | 1 | 0–1 | 1 |
| Can downgrade | To 5.12 or later only | N/A | Yes |
| Cross-release-train (e.g. 4.x→5.x) | No | No | Yes |
| Disk requirement | 30GB+ SSD | 0.8GB free | Any |

**Every method starts and ends with a support-bundle capture** (not upgrade-specific to any one method):
```
nv action generate system tech-support
```
Run before and after the upgrade; copy the archive off-switch. This is the source's own universal
pre/post step regardless of which method is chosen.

## Method 1 — Optimized Image Upgrade (non-destructive, ISSU-capable)

### Prerequisites
- 30GB+ SSD confirmed via `sudo blockdev --getsize64 /dev/sda`, or confirm the `CL-SYSTEM-2` partition
  exists via `sudo blkid`.
- Cannot downgrade to 5.11.0 or earlier using this method.
- **If ISSU is needed**, two day-0 configuration steps are required first (both disruptive on their
  own — see Patterns):
  ```
  nv set router bgp graceful-restart mode full
  nv set system forwarding resource-mode half
  ```
  The first resets BGP neighbors when applied; the second restarts `switchd` and halves available
  TCAM/KVD resources. Neither is something to apply casually alongside an unrelated change — confirm
  with the operator that halving forwarding-resource capacity is acceptable for this switch's role
  before setting it.

### Procedure
1. Fetch the image:
   ```
   nv action fetch system image http://<server>/cumulus-linux-<version>-<platform>.bin
   ```
2. Install it:
   ```
   nv action install system image files cumulus-linux-<version>-<platform>.bin
   ```
   Append `force` to override a documented compatibility block if one applies and the operator has
   confirmed proceeding anyway — don't add `force` reflexively on the first failure.
3. Set the newly-installed image to boot next:
   ```
   nv action boot-next system image other
   ```
4. **Stop and confirm with the operator before proceeding** — the reboot in this step activates the new
   image, and there's no documented auto-abort timer or rollback-on-timeout; Method 1's `boot-next ...
   rollback` (below) is a manual action taken after the fact, not an automatic safety net. Reboot (warm
   reboot supports ISSU where prerequisites are met):
   ```
   nv action reboot system mode warm
   ```
5. Confirm the switchover completed cleanly:
   ```
   sudo csmgrctl -wf
   ```

Equivalent direct Linux-command form (non-NVUE):
```
cl-image-upgrade -u cumulus-linux-<version>-<platform>.bin
cl-image-upgrade -s
cl-image-upgrade -a
sudo csmgrctl -wf
```

### Rollback
```
nv action boot-next system image other rollback
```

## Method 2 — Package Upgrade (apt-based, non-destructive, ISSU-capable)

### Prerequisites
- 0.8GB free disk space — confirm via `nv show system disk usage` or `sudo df -h`.
- **Cannot upgrade across release trains** (e.g. 4.x to 5.x) — this method only advances within the
  currently-installed train, to the latest release available in the configured repository.
- **Never use `sudo -E apt-get dist-upgrade`** — the source calls this out explicitly as the wrong
  command for this procedure; use the documented NVUE or `apt-get upgrade` forms instead.

### Procedure
1. Dry-run first, to preview what would change without applying it:
   ```
   sudo nv action upgrade system packages to latest use-vrf default dry-run
   ```
2. Apply:
   ```
   sudo nv action upgrade system packages to latest use-vrf default
   ```
3. **Handle file-conflict prompts** if they appear during the upgrade: `Y`/`I` keeps the new version,
   `N`/`O` keeps the current file, `D` shows a diff, `Z` drops to a shell. Don't reflexively accept the
   new version on every prompt without checking what's being replaced if the switch has local
   customizations to config files under active management.
4. Check whether a reboot is actually required (package upgrades don't always need one):
   ```
   nv show system reboot required
   ```
5. If required, **stop and confirm with the operator before proceeding** — same reasoning as Method 1
   (no auto-abort timer or rollback-on-timeout). Reboot (warm reboot supports ISSU where prerequisites
   are met — same BGP graceful-restart-full and half-resource-mode day-0 config as Method 1):
   ```
   nv action reboot system mode warm
   ```
6. Confirm:
   ```
   sudo csmgrctl -wf
   ```

Equivalent direct Linux-command form:
```
sudo -E apt-get update
sudo -E apt-get upgrade --dry-run
sudo -E apt-get upgrade
sudo csmgrctl -wf
```

Expected output when no reboot is needed (services restart in place instead):
```
Policy: Service frr.service action stop postponed
Policy: Restarting services: frr.service
Policy: Finished restarting services
Policy: Removed /usr/sbin/policy-rc.d
Policy: Upgrade is finished
```

## Method 3 — ONIE Image Upgrade (destructive, no ISSU)

**This method erases configuration.** Use it only when a cross-release-train jump or a from-scratch
reinstall is actually the goal — not as a default path when Methods 1 or 2 would suffice.
**Stop and confirm with the operator before proceeding** — this is the one method in this file with no
non-destructive fallback if something goes wrong mid-procedure.

### Pre-checks (mandatory, not optional, given the destructive nature)
1. Back up the NVUE configuration:
   ```
   nv config save
   ```
   then copy `/etc/nvue.d/startup.yaml` off-switch before proceeding.
2. Alternatively (or additionally), back up the individual Linux config files under `/etc/` that matter
   (FRR, network, ACL, QoS configuration files — the source lists these categories specifically; confirm
   exactly which files apply to the target switch's configuration before relying on a partial backup).
3. Download the target image from the NVIDIA Enterprise support portal.
4. **Note the recovery constraint up front:** if config restore fails post-install, in-band SSH access
   won't be available — recovery requires out-of-band access (the `eth0` management interface or
   console). Confirm out-of-band access is actually available before starting, not after something goes
   wrong.
5. Confirm the switch's existing ONIE installer is newer than 5.3.0012 — the source states installation
   fails on installers at or below that version.
6. Any third-party applications will need manual reinstallation after this method completes — they are
   not preserved.

### Procedure
NVUE form:
```
nv action install system image onie http://<server>/cumulus-linux-<version>-<platform>.bin \
  startup-config /etc/nvue.d/startup.yaml force activate reboot
```
Direct ONIE-command form:
```
sudo onie-install -a -i http://<server>/cumulus-linux-<version>-<platform>.bin \
  -t /etc/nvue.d/startup.yaml && sudo reboot
```

### Post-install (required, not cleanup)
1. **Reimport all certificates** — certificates are not automatically restored by this method:
   ```
   nv action import system security
   ```
2. **If the backed-up `startup.yaml` came from Cumulus Linux 5.15 or earlier**, IPv6 addresses need
   translation before it's usable on the new version:
   ```
   nv config translate filename /home/cumulus/startup.yaml > normalized.yaml
   sudo cp normalized.yaml /etc/nvue.d/startup.yaml
   nv config apply startup
   ```
   Skipping this on an old backup risks applying a config the new version can't correctly interpret —
   don't assume an old `startup.yaml` applies cleanly without this step.

## Patterns

- **ISSU eligibility is a day-0 decision, not something to bolt on at upgrade time.** BGP graceful-
  restart-full and half-resource forwarding mode both have disruptive side effects when first applied
  (a BGP neighbor reset; a `switchd` restart that halves TCAM/KVD capacity) — if the switch wasn't
  already configured this way, applying it "in order to do ISSU this one time" introduces its own
  disruption. Treat ISSU as something the switch is either already provisioned for, or a planned change
  in its own right — not a free option available at upgrade time.
- **Package Upgrade is a moving target ("to latest"), not a specific pinned version.** There's no
  documented way in this procedure to pin to an exact version within the same train — it upgrades to
  whatever the configured repository currently serves as latest. If a specific target version matters,
  confirm the repository is pinned to serve that version before running this method.
- **ONIE is the only method that crosses release trains — and the only one with no config-preserving
  path.** If the ask is "go from 4.x to 5.x," ONIE is the documented path, but that also means accepting
  a destructive reinstall; there's no way to get the cross-train jump without it via these three methods.
- **`csmgrctl -wf` at the end of Methods 1 and 2 is a confirmation step, not decoration.** Both
  procedures end with it — don't consider the upgrade complete on `install`/`upgrade` command success
  alone.

## Known limitations

- Covers these three documented upgrade methods only. NVOS (NVIDIA's successor platform) is a distinct
  product with its own documentation, not covered here — a third-party source found during research
  reported NVIDIA is transitioning away from standalone Cumulus Linux toward NVOS; this wasn't
  independently confirmed against an NVIDIA primary source and is flagged as an inference risk, not a
  fact this file relies on. Confirm the target platform is still on Cumulus Linux (not NVOS) before
  using this file.
- **ONIE Image Upgrade is destructive and has no ISSU path** — config is not preserved automatically,
  third-party applications must be manually reinstalled, and certificates must be manually reimported
  post-install. This is why it carries its own explicit confirmation gate above, on top of the
  general "confirm before an irreversible step" discipline this skill uses elsewhere.
- Package Upgrade cannot cross release trains (e.g. 4.x→5.x) and always targets "latest," not a pinned
  version — if either constraint doesn't fit the ask, this isn't the right method.
- No documented auto-abort-timer or rollback-on-timeout exists for any of the three methods — Method 1's
  `boot-next ... rollback` is a manual action taken after the fact, not an automatic safety net that
  fires on its own.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| NVUE CLI session (`nv ...` commands) or direct Linux CLI session (SSH/console) | Sends every `nv action`/`nv set`/`nv show`/`apt-get`/`cl-image-upgrade`/`onie-install` command in this procedure; must survive the reboot to confirm the switch comes back up on the target version | Device Access |
| Image server or local storage reachable from the switch (HTTP fetch, or a locally-staged file) | Serves the `.bin` Cumulus Linux image the `fetch`/`install`/`onie-install` commands retrieve | Device Access |
| Out-of-band access (management `eth0` or console) | Required specifically for the ONIE method's recovery path if in-band config restore fails post-install | Device Access |

## Verification checklist

- [ ] The correct method was chosen deliberately (not defaulted to ONIE) based on whether config
      preservation, cross-train upgrade, or ISSU was actually required
- [ ] `nv action generate system tech-support` was captured before AND after the upgrade
- [ ] For ISSU: BGP graceful-restart-full and half-resource forwarding mode were confirmed as intentional
      day-0 configuration, not applied reactively at upgrade time without operator sign-off
- [ ] For Package Upgrade: a dry-run was reviewed before the real upgrade command ran
- [ ] For ONIE: configuration was backed up and copied off-switch, out-of-band access was confirmed
      available, and the operator explicitly confirmed before proceeding with the destructive install
- [ ] Post-upgrade: `csmgrctl -wf` (Methods 1/2) confirmed clean completion, or (ONIE) certificates were
      reimported and an old `startup.yaml` was translated if sourced from 5.15 or earlier
