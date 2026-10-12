---
name: network_test_execution
description: Prepare and run network tests and inspect their reported results. Use when this operation is requested on Cisco pyATS (AEtest, Blitz, Robot Framework, Genie harness, Health Check) and Cisco XPRESSO (single registered job requests). Assumes the chosen pyATS test libraries and testbed, or an authenticated XPRESSO session with a registered job. Framework execution is covered; expected network state remains an input. XPRESSO deployment, scheduling, bundles, and resource administration are excluded.
---

# Network Test Execution

Prepare and run network tests and inspect their reported results using the selected platform's documented procedure.

## When to use this skill

Use to run pre- or post-change validation or health checks against network devices and read the results, on Cisco pyATS (AEtest, Blitz, Robot Framework, Genie harness, Health Check) or Cisco XPRESSO. Pick the mode that matches the test format you already have. Gathering raw state without assertions belongs to `network_state_collection`.
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

Framework execution is covered; expected network state remains an input. XPRESSO deployment, scheduling, bundles, and resource administration are excluded.

## Contributing to this skill

Change this router only to correct its shared concepts/routing or add a supported platform pointer.
Vendor details belong in that vendor's references. Recheck shared claims before adding a platform.

## Tools

Assumes the chosen pyATS test libraries and testbed, or an authenticated XPRESSO session with a registered job. The platform procedure lists the required operations or execution mechanism.

## Verification checklist

- [ ] Platform and operation match an entry in the index.
- [ ] The selected procedure's checks and any confirmation gates were followed.
- [ ] Actual results and documented failures are reported without replacing their status vocabulary.
