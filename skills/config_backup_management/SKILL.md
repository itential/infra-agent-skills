---
name: config_backup_management
description: Capture a point-in-time copy of a network site's configuration as a portable file, track the capture job, retrieve the file, and redeploy a saved copy to recreate or refresh a site (a redeploy, not a documented rollback). Covers Prisma SD-WAN (site snapshots in YAML) today. Use for taking a configuration backup before a change, keeping a baseline, or replicating or refreshing a site from a saved copy. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. Check references/INDEX.md for which platforms and operations are covered.
argument-hint: "[platform] [action: capture|check_capture|retrieve|list_captures|redeploy|check_redeploy|list_redeploys] [site or job identifier, saved file]"
---

# Config Backup Management

Captures a saved copy of a configuration, follows the capture to completion, retrieves the copy, and
redeploys a saved copy, on whichever platform the caller targets, following that platform's own
documented procedure exactly.

## When to use this skill

- Taking a configuration backup or baseline before a change, replicating a site's configuration, or
  refreshing a site by redeploying a previously saved copy. Which of these a platform supports is
  platform-dependent; see `references/INDEX.md`.
- Not for comparing device state before and after a change — see `network_state_collection`.
- Not for the change record or its approval — see `change_management`.
- Not for software image upgrades or rollback — see `software_upgrade_lifecycle`.
- Not for editing the contents of a saved copy or designing configuration; this skill moves copies
  around, it does not author configuration.

## Universal concepts (no wire standard; one implementation today)

Only one platform is documented, so these are expectations to be re-checked when a second platform is
added (`AGENTS.md` rules 4 and 14). Where a platform differs, its own procedure wins.

- **A saved copy is a file of configuration at a moment in time.** Where the platform exposes it, it is
  produced by a capture request, not by editing live state.
- **Capture may be asynchronous.** An accepted request is not a finished copy; confirm the job outcome
  before relying on the file.
- **Redeploying a copy writes configuration to the platform.** Where a copy matches something that
  already exists, the effect on that existing object is platform-defined; treat redeploy as a
  state-changing action and confirm before it.
- **A copy can carry sensitive configuration (assumption).** Where the platform does not state what is
  excluded, store and share the file as sensitive.
- **Retention, scheduling, and storage location are not defined by the platform procedure** unless its
  own file says so; they are the caller's concern.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- Platform coverage is in `references/INDEX.md`; a platform not listed there needs a new reference
  file before this skill can be used for it.
- Does not cover scheduling, retention, or off-platform storage of copies.
- Does not cover configuration comparison or drift detection.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed API route — belong in that platform's own
`references/<platform>/` files, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its confirmation gate before redeploy
- [ ] Outcome reported using the platform procedure's own status vocabulary
