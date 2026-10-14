---
name: compute_instance_provisioning
description: Create, read, resize, snapshot, power-control, and decommission virtual machine instances on a supported hypervisor or cloud platform. Instance lifecycle only — not a general cloud or hypervisor administration skill. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. No vendor coverage yet — see references/INDEX.md.
argument-hint: "[platform] [action: create|read|resize|snapshot|power|delete] [instance identifier, fields]"
---

# Compute Instance Provisioning

Manages the lifecycle of a virtual machine instance — create, read, resize, snapshot, power-control,
decommission — on whichever platform the caller is targeting, following that platform's own
documented procedure exactly.

## When to use this skill

- Creating, reading, resizing, snapshotting, powering on/off or restarting, or deleting a virtual
  machine instance on a supported hypervisor or cloud platform.
- Not for containers or Kubernetes workloads — see `container_workload_deployment`.
- Not for upgrading network-device operating systems — see `software_upgrade_lifecycle`.
- Not for allocating addresses or recording the instance in an inventory — see `ipam_allocation`,
  `dcim_asset_management`, and `cmdb_asset_management`. Where creating an instance requires
  attaching an existing network, volume, or address, that attachment is part of the platform's own
  create procedure; creating those objects themselves is out of scope.

## Universal concepts (shared virtual-instance vocabulary, not a wire standard)

*(To be filled in as vendors are added — see `AGENTS.md` rule 4: only claims verified true across
every vendor actually listed belong here. Do not pre-populate this section with assumptions before
a vendor's real behavior has been checked against them.)*

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- No vendor coverage yet — see `references/INDEX.md`. A platform not listed there needs a new
  reference file before this skill can be used for it.
- Scope is the instance lifecycle only. Networks, storage systems, images, identity, and other
  parts of a cloud or hypervisor are out of scope even where the same platform offers them.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed API path — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates on
      deletion, resize (where the platform documents a restart), and power-off of a running instance
- [ ] Outcome reported using the platform procedure's own status vocabulary
