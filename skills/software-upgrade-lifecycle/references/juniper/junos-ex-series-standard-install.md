# Juniper Junos OS — EX Series Standard Software Installation (CLI)

Upgrade or downgrade Junos OS on an EX Series switch using the **Standard Installation** method —
Juniper's own term for the typical `request system software add` upgrade/downgrade path, distinct from
Category Change Installation (moving between Junos OS editions, e.g. to Junos-FIPS) and Recovery
Installation (repairing damaged software), neither of which this file covers. Two variants: single
Routing Engine (most EX platforms) and redundant Routing Engine (EX6200, EX8200 with dual REs). Assumes
an authenticated CLI/console session against the target switch with appropriate privilege, able to run
exec-mode and configuration-mode commands, transfer a file to `/var/tmp` (FTP/HTTP or local copy), and
detect switch/RE reachability across a reboot.

## Single Routing Engine Procedure

Applies to EX2200, EX2300, EX3200, EX3300, EX3400, EX4100, EX4200, EX4300, EX4500, EX4550, EX6200
(single-RE mode), EX8200 (single-RE mode), and most Virtual Chassis configurations.

### Step 1 — Pre-checks (EX2300 / EX3400 / EX4100 specifically)

```
show system storage
```
Confirm at least **620 MB** of disk space is available. If not:
```
request system storage cleanup
```
This platform-specific check is documented for these three models — for other EX platforms the source
doesn't state a specific figure; if disk space is a concern on an unlisted platform, check
`show system storage` anyway rather than assuming headroom.

### Step 2 — Obtain and stage the package

Download the target software package/bundle, then copy it to the switch's `/var/tmp` directory (FTP or
other transfer). Optionally back up the current configuration first — not gated by the source as
mandatory, but recommended given the destructive nature of what follows.

### Step 3 — Install

```
request system software add source [package-path]
```
Where `package-path` is one of: a local path (`/var/tmp/package.tgz`), an FTP URL
(`ftp://hostname/pathname/package.tgz`), or an HTTP URL (`http://hostname/pathname/package.tgz`).

Platform-specific variants:
- Single Virtual Chassis member: `request system software add source [path] member member-id`
- EX4300-MP: `request system software add source [path] force-host`

**Validation runs by default when the target is a different release** — `request system software add`
validates the package against the current configuration automatically unless `no-validate` is passed
(other options include `no-copy`, `force`/`force-host`, `member`, `partition`, `delay-restart`,
`unlink`, `validate-on-host`/`validate-on-routing-engine`). Don't add `no-validate` without a specific
reason to skip it — it's the documented safety mechanism at this step.

If installing without `reboot` appended and needing to back out before rebooting:
```
request system software delete package.tgz
```
(Not available on EX2300/EX3400 — confirm platform support before relying on this cancellation path.)

### Step 4 — Reboot

**Stop and confirm with the operator before proceeding** — the switch reboots and is briefly
unreachable, and there's no documented auto-abort timer or rollback-on-timeout to fall back on (see
Known limitations). Confirm the install in Step 3 actually reported success before rebooting on it.

```
request system reboot
```

### Step 5 — Verify

```
show version
```
Confirm the reported version matches the target package.

### Step 6 — Update the alternate partition

```
request system snapshot slice alternate
```
or, for every Virtual Chassis member:
```
request system snapshot slice alternate all-members
```
This propagates the newly-active software to the alternate boot partition — skipping it leaves the
alternate partition on the old version, which matters if the switch later boots from that partition
(e.g. after a failure of the primary partition).

## Redundant Routing Engine Procedure

Applies to EX6200 and EX8200 with dual Routing Engines.

**Critical pre-condition — stop and confirm before proceeding:** graceful Routing Engine switchover
(GRES) and nonstop active routing (NSR) **must be disabled** before starting. The source states plainly:
"If graceful routing engine switchover (GRES) or nonstop active routing (NSR) is enabled when you
initiate a software installation, the software does not install properly." This is not optional prep —
it's a hard precondition.

### Step 1 — Disable GRES/NSR on the primary RE

```
cli
configure
deactivate routing-options nonstop-routing
deactivate routing-options nonstop-bridging
deactivate chassis redundancy graceful-switchover
commit
exit
```

### Step 2 — Install on the backup RE first

1. Download and copy the software package to `/var/tmp` (same transfer methods as the single-RE
   procedure).
2. Log into the **backup** RE's console specifically — not the primary.
3. Install: `request system software add source [package-path]`
4. Reboot: `request system reboot`
5. Verify: `show version`

### Step 3 — Switch control to the now-upgraded RE, then upgrade the original primary

**Stop and confirm with the operator before proceeding** — this transfers mastership away from the
current primary and then reboots the chassis's other RE, the point in this procedure where the chassis
is most exposed (mastership just moved, and the newly-demoted RE is about to reboot too). Confirm
Step 2's install and reboot on the backup RE actually succeeded before starting this step.

1. From the primary RE console, transfer routing-engine mastership:
   ```
   request routing-engine login member 1
   ```
2. Confirm slot 1 is now primary: `show chassis routing-engine`
3. Install on the new backup (the original primary, now demoted):
   `request system software add source [package-path]`
4. Reboot: `request system reboot`
5. Log into slot 1's console.
6. Re-enable GRES and NSR:
   ```
   set chassis redundancy graceful-switchover
   set routing-options nonstop-routing
   commit
   ```
7. Update the alternate partition on **both** REs: `request system snapshot slice alternate` (run on
   each).

### Step 4 (optional) — Return mastership to the original primary

```
request routing-engine login member 0
```
Verify: `show chassis routing-engine`. This is optional — the source doesn't require restoring the
original primary/backup roles, only that both REs end up running the target version with GRES/NSR
re-enabled.

## USB Flash Drive Boot (recovery-adjacent path, single RE)

Only usable when the `loader>` prompt is displayed (not a normal EXEC-mode operation):
```
install source file:///junos-install-media-usb-ex-arm-64-<version>.tgz
```
The package is typically the sole file at the root of the USB media.

## Patterns

- **Validation is on by default for a cross-release install — don't disable it without reason.** Passing
  `no-validate` removes a real safety check, not a formality; the default behavior already validates the
  package against the running configuration.
- **The redundant-RE procedure is upgrade-the-backup-first, always.** Never install directly on the
  active/primary RE first — the sequence (backup RE → switch mastership → now-backup RE) exists
  specifically so there's always a stable RE to fail back to mid-procedure.
- **GRES/NSR must be off during install, then explicitly re-enabled afterward — this is a paired
  operation, not two independent steps.** Forgetting Step 3's re-enable leaves the chassis without
  graceful switchover protection going forward, silently.
- **The alternate-partition snapshot is easy to skip and easy to forget why it matters.** It's not
  "housekeeping" — without it, an unplanned boot from the alternate partition boots the *old* version.

## Known limitations

- Covers Standard Installation only (single-RE and redundant-RE variants) — does not cover Category
  Change Installation (moving between Junos OS editions, e.g. to Junos-FIPS, which explicitly cannot use
  `request system software rollback` and instead requires `request system snapshot` immediately after)
  or Recovery Installation (repairing damaged software). Both are out of scope here.
- The 620 MB disk-space figure is documented specifically for EX2300/EX3400/EX4100 — not stated as a
  universal figure for every EX platform; check `show system storage` regardless of platform rather than
  assuming this number applies elsewhere.
- **Skipping GRES/NSR deactivation on a redundant-RE chassis is documented to cause the install to not
  work properly** — this is stated as a precondition failure mode, not a soft recommendation.
- No documented auto-abort-timer or rollback-on-timeout exists for either procedure — once
  `request system reboot` runs, there's no built-in safety window; recovery from a bad install is manual
  (a further install, or Recovery Installation if the software is now damaged).

## Tools

| Mechanism | Description | Category |
|---|---|---|
| CLI/console exec session (SSH or console), per Routing Engine on dual-RE chassis | Sends every `request`/`show`/`configure` command in this procedure; must reach each RE independently during the redundant-RE procedure and survive reboots to confirm the switch/RE comes back up | Device Access |
| File transfer to `/var/tmp` (FTP, HTTP, or local copy) | Places the target software package on the switch before `request system software add` references it | Device Access |

## Verification checklist

- [ ] `show system storage` (or the documented 620MB check on EX2300/EX3400/EX4100) confirmed adequate
      space before staging the package
- [ ] Single-RE: `show version` confirmed the target version post-reboot, and the alternate-partition
      snapshot was updated
- [ ] Redundant-RE: GRES and NSR were deactivated before Step 1 and explicitly re-enabled and committed
      after both REs were upgraded — never left disabled
- [ ] Redundant-RE: the backup RE was upgraded first in every case, never the active/primary RE first
- [ ] Redundant-RE: `show chassis routing-engine` confirmed mastership state at each transfer point,
      not assumed from the prior command's success alone
