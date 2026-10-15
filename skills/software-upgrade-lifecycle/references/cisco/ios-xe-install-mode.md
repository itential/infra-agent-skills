# Cisco IOS-XE — Install-Mode Upgrade Procedure

Upgrade IOS-XE on any Catalyst/IOS-XE platform (originally scoped to Catalyst 9000 — C9200/C9300/C9400/
C9500/C9600 — but the install/activate/commit sequence below applies to any IOS-XE device or stack
already running in INSTALL mode) already running in INSTALL mode, using Cisco's documented add/activate/
commit procedure with its built-in safety mechanisms carried forward exactly as published. Does not
cover bundle mode, bundle-to-install conversion, ISSU, Stackwise Virtual, ReloadFast, or V-Mismatch/
ROMMON recovery. Assumes an authenticated CLI/console session against the target device (or stack) with
enable/privileged exec access, able to run exec-mode commands, respond to interactive y/n prompts,
transfer a file to local flash, and detect device reachability across a reload.

## Operational procedure

### Step 1 — Confirm Eligibility

Run `show boot` (or `show version`) and `show install summary`.

- Boot variable must point to `packages.conf` — this is the definition of install mode. If it does not
  (BUNDLE mode), **stop**: bundle-to-install conversion is a separate procedure, out of scope for this
  skill.
- If the target version already shows state `C` (Activated & Committed) in `show install summary` — the
  upgrade is already done. Skip to Step 5 (Post-Upgrade Verification), then report IDEMPOTENT.
- If the target version already shows state `I` (Inactive) — a prior `install add` was run and not
  completed. Do not run `install add` again; proceed directly to Step 3 (Activate) with the existing
  package, or run `install remove inactive` first if it doesn't match the target version.
- For a stack: run `show switch` and confirm all members show `Ready`. A member in `V-Mismatch` state is
  out of scope for this skill — stop and report which member.

### Step 2 — Add the Package

```
install add file <bootflash:|flash:><image_path>
```

(Use the platform-appropriate flash prefix.)

- If the device returns `Super package already added. Add operation not allowed.` — this is a known,
  documented condition. Inspect `show install summary`: if the already-added package matches the
  target version, proceed to Step 3 with it; otherwise run `install remove inactive` first, then retry
  this step.
- On success, confirm via `show install summary` that the target version now shows state `I`.
- For a stack, confirm the package reaches every member before activating — it is normal for the file to
  exist only on the Active member's flash pre-commit, but if `install add` explicitly reports a member
  missing the package, copy it there directly (e.g. `copy bootflash:<file> bootflash-2:`) or via USB
  before continuing.
- Any other add failure (insufficient space, transfer incomplete): stop and report. Do not retry
  automatically.

### Step 3 — Activate

```
install activate
```
or, to override the default abort-timer duration (default 120 minutes, valid range 30-1200):
```
install activate auto-abort-timer <minutes>
```

The device prompts `This operation may require a reload of the system. Do you want to proceed? [y/n]` —
respond `y`; this is expected, not an error.

This reloads the device and starts the auto-abort timer. Wait for the device to become reachable again,
then confirm via `show install summary` that the target version shows state `U` (Activated & Uncommitted)
with the abort timer running. Record the activation time and surface remaining timer time in every
subsequent status update.

If `install activate` errors before reload, or the device does not come back up — stop and report; an
unreachable device after reload needs operator intervention, not further remote recovery attempts by
this skill.

### Step 4 — Commit Gate

Run the health checks in Step 5 against the activated-but-uncommitted version before deciding on commit.

- **Checks pass** — **stop and confirm with the operator before proceeding**, stating the remaining
  auto-abort-timer window from `show install summary`. Do not run `install commit` without that
  confirmation — this is the point after which the change becomes durable.
- **Checks fail** — do not commit. Report the failure and the remaining timer window. Let the operator
  choose: investigate within the window, run `install abort` (reloads back to the prior version), or
  allow the timer to expire (device auto-reloads back to the prior committed version on its own).
- **Confirmed** — run:
  ```
  install commit
  ```

### Step 5 — Post-Upgrade Verification

Confirm via `show install summary` that the target version shows state `C` (Activated & Committed) with
the auto abort timer `inactive`. Also confirm: `show version` reports the target version; boot variable
is still `packages.conf`; for a stack, `show switch` shows all members `Ready` on the same version.

- All pass → SUCCESS.
- Version/commit state correct but an unrelated health anomaly appears → PARTIAL, report the specific
  anomaly (not automatically a rollback trigger).
- Commit did not result in state `C` / timer `inactive` → report the actual state observed; do not retry
  the commit automatically.

### Step 6 — Cleanup (only if explicitly authorized)

Only after Step 5 reports SUCCESS, and only if the caller explicitly authorized cleanup:

```
install remove inactive
```

This lists every file it plans to delete and prompts `Do you want to remove the above files? [y/n]` —
surface that list to the operator before confirming. It is irreversible without re-transferring the
removed image. Never run this before commit — it can remove files needed for rollback.

## Patterns

- **Idempotency check comes first.** Step 1 exists specifically so re-running this procedure against an
  already-committed target version is a no-op (IDEMPOTENT), not a redundant reload.
- **The abort timer is the safety net, not the confirmation.** Confirmation before commit is required
  regardless of how much timer time remains — a long remaining window doesn't substitute for the
  operator's go-ahead.

## Known limitations

- Does not cover bundle mode, bundle-to-install conversion, ISSU, Stackwise Virtual, ReloadFast, or
  V-Mismatch/ROMMON recovery — any of these conditions found during Step 1 stops the procedure.
- **`install commit` (Step 4) is the point after which the change is durable** — reversible only via
  install abort/rollback before commit, or via a fresh downgrade install after commit. This is why Step
  4 requires explicit operator confirmation before proceeding.
- **`install remove inactive` (Step 6) is irreversible** without re-transferring the removed image, and
  can remove files needed for rollback if run before commit — never run it before Step 5 reports SUCCESS.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| CLI/console exec session (SSH or console) | Sends every `show`/`install` command in this procedure to the device's enable/privileged-exec prompt and captures the output; must survive the reload in Step 3 to confirm the device comes back up | Device Access |
| File transfer to local flash (SCP/TFTP/USB, etc.) | Places the target IOS-XE image on the device's flash before Step 2 runs `install add` against it | Device Access |
| Interactive prompt handling | Responds to the CLI's `[y/n]` confirmation prompts (Step 3 activate, Step 6 cleanup) as part of the same exec session | Device Access |

## Verification checklist

- [ ] `show install summary` confirms the target version reached state `C` with the abort timer
      `inactive`
- [ ] `show version` reports the target version and boot variable is still `packages.conf`
- [ ] For a stack: `show switch` shows all members `Ready` on the same version
- [ ] Commit was performed only after explicit operator confirmation
- [ ] Cleanup (`install remove inactive`), if run, happened only after a SUCCESS verification and only
      with explicit authorization
