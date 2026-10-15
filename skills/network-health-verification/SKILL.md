---
name: network-health-verification
description: Screen network devices for health problems (CPU, memory, logs, core files, crashinfo) after a change or while troubleshooting. Use to run documented health checks as part of a job run and read each check's result. Covers Cisco pyATS Health Check in integrated job mode; assumes pyATS, a testbed, authenticated device access, and an existing pyATS job. Thresholds are inputs; this does not decide what "healthy" means for a network.
---

# Network Health Verification

Run health checks against network devices and report what each check observed.

## When to use this skill

Use to confirm devices are healthy after a change, or to screen for resource, log, or crash problems
while troubleshooting, by running health checks with a job. Capturing state snapshots to compare
yourself belongs to `network-state-collection`. Applying the change itself is outside this skill.

## Universal concepts

- A health result reflects only the checks, thresholds, and device coverage actually run;
  unsupported or skipped checks are unknown, not healthy.
- Some checks have side effects (clearing logs, copying or deleting crash files) and need explicit
  approval before the run.
- Thresholds and criteria are caller inputs, not defaults this skill defines.

## Procedure

1. Identify the requested tool in [references/INDEX.md](references/INDEX.md).
2. Open the linked procedure and follow it exactly, including its confirmation gates.
3. Report results using that procedure's own status vocabulary.

## Known limitations

The tool's side-effect options are flagged in its procedure. Coverage is limited to the
implementation in the index.

## Contributing to this skill

Change this router only to correct its shared concepts/routing or add a supported tool pointer.
Tool details belong in that tool's references. Recheck the universal concepts before adding a tool.

## Tools

A local pyATS job/CLI session with device transport; the mode procedure lists the specifics.

## Verification checklist

- [ ] Tool matches an entry in the index.
- [ ] The selected procedure's checks and confirmation gates were followed.
- [ ] Results and documented failures are reported without replacing their status vocabulary.
