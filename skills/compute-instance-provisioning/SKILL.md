---
name: compute-instance-provisioning
description: Create, read, resize, snapshot, power-control, and decommission virtual machine instances on a supported hypervisor or cloud platform — currently Amazon EC2, Google Compute Engine, VMware vSphere, and Morpheus. Instance lifecycle only — not a general cloud or hypervisor administration skill. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. Check references/INDEX.md for which platforms and operations are covered.
argument-hint: "[platform] [action: create|read|resize|snapshot|power|delete] [instance identifier, fields]"
---

# Compute Instance Provisioning

Manages the lifecycle of a virtual machine instance — create, read, resize, snapshot, power-control,
decommission — on whichever platform the caller is targeting, following that platform's own
documented procedure exactly.

## When to use this skill

- Creating, reading, resizing, snapshotting, powering on/off or restarting, or deleting a virtual
  machine instance on a supported hypervisor or cloud platform.
- Not for containers or Kubernetes workloads — see `container-workload-deployment`.
- Not for upgrading network-device operating systems — see `software-upgrade-lifecycle`.
- Not for allocating addresses or recording the instance in an inventory — see `ipam-allocation`,
  `dcim-asset-management`, and `cmdb-asset-management`. Where creating an instance requires
  attaching an existing network, volume, or address, that attachment is part of the platform's own
  create procedure; creating those objects themselves is out of scope.

## Universal concepts (shared virtual-instance vocabulary, not a wire standard)

These are claims expected to hold for any hypervisor or cloud platform, and were re-checked against each
platform listed in `references/INDEX.md` (`AGENTS.md` rules 4 and 14). Where a platform differs, its own
procedure wins.

- **An instance has a lifecycle state that decides which operations are allowed, and write calls are
  usually asynchronous.** Read the current state before changing an instance, and confirm the target
  state after; an accepted request is not a finished one.
- **Deleting an instance is final, and what happens to its storage depends on the platform and its
  settings.** Treat deletion as a confirmation point and tell the operator which storage will go with
  it.
- **Some changes, such as resizing, may require the instance to be powered off,** where the platform
  says so; some platforms allow certain changes while it runs. Power-off interrupts the workload and can lose volatile state; confirm before
  doing it, and let the platform's own procedure say what else changes.
- **What "snapshot" means differs by platform** (a point-in-time copy of the whole machine, of its
  disks, or an image to launch from), and not every platform can revert an instance to one, or offers a snapshot of an instance at all. Do not
  assume either exists.
- **Repeating a create request can create a second instance** unless the platform offers an
  idempotency mechanism; use it where it exists.

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
- Scope is the instance lifecycle only. Networks, storage systems, images as standalone catalog objects, identity, and other
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
      launch, power-on, power-off, reboot, resize, an image that reboots the instance, and deletion
- [ ] Outcome reported using the platform procedure's own status vocabulary
