# Cisco IOS XR (Classic 64-bit RPM Install) — Upgrade Procedure

Upgrade Cisco IOS XR software on a router running the classic RPM-based install model (`install add` /
`install activate` / `install commit`) — confirmed identical across Cisco NCS 5500 Series and Cisco
ASR 9000 Series in their respective System Setup and Software Installation Guides (IOS XR 7.11.x and
7.10.x). This is the "Perform System Upgrade and Install Feature Packages" procedure, not the newer
IOS XR7 install workflow used on NCS 5700 Series routers (a materially different workflow — see Known
limitations). Assumes an authenticated CLI/console session against the target router with EXEC access
to both the XR VM and System Admin VM, able to run exec-mode `install`/`show` commands, and to reach an
image/package repository (local disk, USB, or a remote server over HTTP/HTTPS/TFTP/FTP/SFTP via the
management port or a data port).

## Operational procedure

### Step 0 — Pre-upgrade checks (do before staging anything)

- **Disk space and filesystem health.** Ensure adequate disk space. Run `fsck` to check filesystem
  status — in System Admin EXEC mode to install a System Admin package, in XR EXEC mode to install an
  XR package.
- **Check the supported upgrade/downgrade path** — never assume a target version is reachable from the
  current one:
  ```
  show install upgrade-matrix running
  ```
  or, checking against a specific target ISO already staged locally:
  ```
  show install upgrade-matrix iso <path-to-ISO>
  show install upgrade-matrix iso <path-to-ISO> all
  show install upgrade-matrix iso <path-to-ISO> from-running
  ```
  These report required bridging SMUs, blocking SMUs, unsupported hardware, and caveats for the
  from→to pair. If the running version is below Release 7.5.1, upgrade to 7.5.1 first, then re-check the
  matrix for the real target. **Do not bypass this check** unless the operator explicitly authorizes the
  `force` keyword on `install replace` — using `force` suppresses the block but only warns, it does not
  stop a genuinely incompatible upgrade from proceeding.
- **Preserve configuration commit history before upgrading, if it matters for audit/troubleshooting.**
  The commit-history database schema (configuration namespace version) can change between releases;
  post-upgrade, commands like `show configuration rollback changes <commit-id>` referencing pre-upgrade
  commits may report `Configuration namespace version ... is not supported by the current software` —
  this is expected, not a defect. Export `show configuration commit list` and
  `show configuration commit changes <commit-id>` output externally beforehand if that history needs to
  survive the upgrade.
- **If upgrading from Release 7.10.x/7.11.1 specifically to 7.11.2 or later** (not required for 7.11.2→
  24.x.y and later): check NPU operating mode first —
  ```
  show hw-module profile npu-operating-mode
  ```
  If `Native` (not `Compatibility` or `Not Applicable`), continue: check `show running-config | i hw` for
  an existing `hw-module profile mdb ...` line. If none is configured, check the default via
  `show hw-module profile mdb-scale`, then set it explicitly with `hw-module profile mdb <profile-name>`
  followed by `commit` — this avoids continuous process restarts affecting the SDR console on
  Native-mode systems with base/VRF configs in place (VRF, OSPF, BGP L3VPN, L2VPN xconnect, MPLS OAM).
  No manual reload is needed here; the pending profile change takes effect as part of the upgrade reload
  in Step 3.

### Step 1 — Add the package(s) to the repository

```
install add source <http|shttp>://package_path/ filename1 filename2 ...
install add source tftp://package_path/ filename1 filename2 ...
install add source <ftp|sftp>://user@server:/package_path/ filename1 filename2 ...
install add source disk2: filename1 filename2 ...
```

A space is required between `package_path` and the filename(s). Runs asynchronously — the CLI returns
once files are unpacked, not once fully validated in the background. The XR VM and System Admin VM have
separate repositories; the system automatically routes a routing package to the XR VM repository and a
system-administration package to the System Admin VM repository — no separate action needed for that
split.

- Confirm via `show install request` (operation ID and in-progress status) and
  `show install repository` (packages only appear here once `install add` completes) — do not proceed
  to activate before repository confirms the files landed.
- `show install inactive` — confirms which repository packages are inactive and therefore eligible to
  activate.
- **Documented corruption handling:** a sanity check for corrupt RPMs is available via
  `run rpm -K --nosignature /install_repo/gl/xr/<package_name>` in System Admin EXEC mode. From Release
  7.11.21 onward, a corruption during install/upgrade/post-upgrade raises an alarm and syslog
  automatically; replacing the corrupt file with a valid one clears the alarm.

### Step 2 (optional) — Prepare before activating

Preparing pre-loads and pre-validates a package without activating it — recommended when upgrade
downtime matters, since prepared activation is faster and a corrupted file fails at prepare time instead
of at activation time.

```
install prepare package_name
install prepare id operation_id
```

Using the operation ID prepares every package added under that operation together — no need to prepare
each individually. Confirm via `show install prepare`. `install prepare clean` clears a prepare
operation if needed.

### Step 3 — Activate

```
install activate package_name
install activate id operation_id
```

Runs asynchronously by default (use the `sync` option to block until complete). Using an operation ID
activates every package from that `install add` operation together. **If activation fails partway, reuse
the same operation ID to retry** rather than re-adding the packages — this activates the same set
consistently. Once activation completes, **the system reloads automatically** — this is expected, not a
failure signal. For a restart-class SMU, the SMU only takes effect once the processes it affects are
restarted (which may itself require a manual reload — if a warning appears prompting a manual reload
after an SMU activation, perform that reload promptly; the SMU's components activate only after it).

- Confirm via `show install active` — verify the same image and package versions are active on every RP
  and every line card, not just the one that issued the command.

### Step 4 — Commit (durability gate)

```
install commit
```

Commits the Host, XR, and System Admin newly-active software as durable. On Multi-SDR systems,
`install commit sdr` commits only the SDR the CLI session belongs to. **Stop and confirm with the
operator before running this** if the activation in Step 3 hasn't been operationally validated yet — the
source doesn't document a built-in abort-timer/rollback-on-timeout mechanism the way IOS-XE install mode
has, so treat commit as the durability point requiring the same explicit go-ahead.

### Step 5 — Post-upgrade follow-up (do not skip)

- **Upgrade FPD** (Field-Programmable Device firmware) if the upgrade touched hardware requiring it:
  `upgrade hw-module location all fpd all` from System Admin EXEC mode; monitor with
  `show hw-module fpd`; reload the router once FPD upgrade completes. For NC55-PWR-3KW-DC/2HV power
  supply modules specifically, upgrade SC IO FPGA first (`upgrade hw-module location <SC0/SC1> fpd all`
  from Sysadmin), then `upgrade hw-module location pm-all fpd`, then reload the shelf controller
  (`hw-module location <SC0/SC1> reload` from Sysadmin) — in that order.
- **Verify the installation:** `install verify packages`.
- If the new package/SMU causes an issue, use Uninstall (below) rather than attempting an in-place fix.

### Uninstall (deactivate + remove a package or SMU)

1. `show install active` — confirm the package is actually active (only active packages can be
   deactivated).
2. `install deactivate package_name` or `install deactivate id operation_id` — deactivates all features/
   patches tied to the package(s); using an operation ID deactivates everything added under it together,
   including any System Admin packages added in that same operation.
3. `show install inactive` — confirm the package now shows inactive (only inactive packages can be
   removed).
4. `install commit` — commit the deactivation.
5. `install remove package_name` (or `install remove id operation_id`, or `install remove inactive all`
   to remove every inactive package from both XR and System Admin) — removes the now-inactive package
   from the repository.
6. `show install repository` — confirm the removed package no longer appears.

**ISO images cannot be uninstalled** — the only path back from an unwanted ISO-based system upgrade is
installing an older ISO version (a downgrade), not an uninstall. Kernel SMUs that install third-party
components on the host, XR VM, or System Admin VM also cannot be uninstalled — only overwritten by a
subsequent ISO or kernel-SMU install.

## Patterns

- **The upgrade-matrix check is the authoritative compatibility source, not a courtesy.** Don't infer
  upgrade support from version numbers alone — always run `show install upgrade-matrix` against the
  actual target before staging anything.
- **Operation IDs are the retry mechanism.** A failed activate or prepare should be retried with the
  same operation ID, not by re-running `install add` — re-adding creates a new, separate operation.
  Similarly, one operation ID batches every package added in that operation for prepare/activate/
  deactivate/remove — no need to specify packages individually if they share an operation ID.
- **Reload after activate is normal, not a fault condition.** The system reloads automatically once
  activation completes; this is part of the documented flow, not something to treat as an unplanned
  interruption.
- **Commit is the durability point, mirrored on the uninstall path too.** Both activating a new package
  and deactivating an old one require their own `install commit` before the change is durable across a
  future reload.

## Known limitations

- Covers the classic 64-bit RPM install model (`install add`/`activate`/`commit`) shared by NCS 5500
  and ASR 9000 in these guides — **does not cover the separate IOS XR7 install workflow** used on
  NCS 5700 Series routers, which is a materially different process (its own data-model/repository setup
  and upgrade steps) documented in a different chapter of the NCS 5500 guide. If the target platform
  uses IOS XR7, this procedure does not apply — a separate reference file is needed.
- Does not cover initial device bring-up, management-port configuration, or ROMMON/factory-reset
  recovery — those are prerequisites or separate procedures, not part of this upgrade flow.
- **ISO images and kernel SMUs cannot be uninstalled** — only overwritten by a further install. This is
  why a bad ISO upgrade is recovered via downgrade-install, not uninstall.
- **`install commit` is the durability gate and does not have a documented auto-abort/rollback-on-
  timeout safety net** the way Cisco IOS-XE install mode does — treat it as requiring explicit operator
  confirmation on every use, not just on a first-time or high-risk upgrade.
- The ASR 9000 guide also documents a legacy Chapter 11 ("Upgrading and Managing Cisco IOS XR
  Software") referencing older 32-bit PIE-based release management (e.g. "Upgrading to Cisco IOS XR
  Software Release 4.0") — this is historical/legacy reference material in that guide, not a current
  alternative procedure, and is out of scope here.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| CLI/console exec session (SSH or console), both XR VM and System Admin VM | Sends every `show`/`install`/`hw-module` command in this procedure and captures output; must survive the automatic reload after Step 3 to confirm the router comes back up | Device Access |
| File transfer to repository (HTTP/HTTPS/TFTP/FTP/SFTP, local disk, or USB) | Places the target ISO/package/SMU files where `install add` can reach them, via the management port or a data port for remote sources | Device Access |

## Verification checklist

- [ ] `show install upgrade-matrix` was checked against the actual target version before staging any
      files, and any required bridging SMUs or blocking conditions were resolved (not bypassed with
      `force` without operator authorization)
- [ ] `show install repository` confirmed the added package(s) before attempting prepare/activate
- [ ] `show install active` confirmed the same image/package versions active on every RP and line card
      after activation
- [ ] `install commit` was only run after the activated version was operationally validated and the
      operator explicitly confirmed
- [ ] Post-upgrade FPD upgrade was run and completed (with its own reload) if the upgrade touched
      hardware requiring it
- [ ] `install verify packages` confirmed the installation post-upgrade
