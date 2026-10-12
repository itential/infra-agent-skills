---
name: network_state_collection
description: Parse command output, learn feature state, and compare saved network snapshots. Use when this operation is requested on Cisco pyATS / Genie. Assumes pyATS, Genie, and an authenticated testbed or captured command output. Collection and comparison report observed data; they do not diagnose root causes or approve a network change.
---

# Network State Collection

Parse command output, learn feature state, and compare saved network snapshots using the selected platform's documented procedure.

## When to use this skill

Use to capture device state before and after a change, or to gather structured evidence while troubleshooting, on Cisco pyATS / Genie: parse command output, learn a feature's state, and diff two snapshots. It reports observed data only; running commands that change devices belongs to `device_cli_execution`, and pass/fail test runs to `network_test_execution`.
The supported modes are listed in [references/INDEX.md](references/INDEX.md).

## Universal concepts

There is no cross-platform wire standard for this capability. Coverage and success criteria
are limited to the documented implementations in the index; no other platform behavior is implied.
A completed operation and the suitability of its result for a particular network are separate checks.

## Procedure

1. Identify the requested platform and supported mode in [references/INDEX.md](references/INDEX.md).
2. Open the indexed platform procedure and follow it exactly, including its mode-specific reference.
3. Report its observed output or result using that procedure's own status vocabulary.

## Known limitations

Collection and comparison report observed data; they do not diagnose root causes or approve a network change.

## Contributing to this skill

Change this router only to correct its shared concepts/routing or add a supported platform pointer.
Vendor details belong in that vendor's references. Recheck shared claims before adding a platform.

## Tools

Assumes pyATS, Genie, and an authenticated testbed or captured command output. The platform procedure lists the required operations or execution mechanism.

## Verification checklist

- [ ] Platform and operation match an entry in the index.
- [ ] The selected procedure's checks and any confirmation gates were followed.
- [ ] Actual results and documented failures are reported without replacing their status vocabulary.
