---
name: network-state-collection
description: Capture structured device state before and after a change, or gather evidence while troubleshooting, by parsing command output, learning feature state, and diffing saved snapshots. Use when you need observed state data to compare or inspect. Covers Cisco pyATS / Genie; assumes pyATS, Genie, and an authenticated testbed or already-captured command output. It reports what was observed; it does not diagnose root causes or approve a change.
---

# Network State Collection

Parse command output, learn feature state, and compare saved snapshots to produce evidence of network state.

## When to use this skill

Use to record device state before a change and again after it, to turn raw command output into
structured data, or to gather evidence while troubleshooting. Health screens and
post-change verification belong to `network-health-verification`. Applying changes to devices is outside this skill.

## Universal concepts

- Snapshots are comparable only when both sides cover the same devices, commands or features, and scope.
- Volatile fields (counters, timers) are handled by documented defaults or explicit exclusions,
  and state being checked is never excluded.
- A collection failure or empty result is incomplete data, not a healthy network.
- An empty difference establishes equality only for the fields actually collected.
- Parser and feature support vary by platform; unsupported coverage is reported, not substituted.

## Procedure

1. Identify the requested tool and mode in [references/INDEX.md](references/INDEX.md).
2. Open the linked tool procedure and follow it exactly, including its confirmation gates.
3. Report results using that procedure's own status vocabulary.

## Known limitations

Collection and comparison report observed data only. Live collection is gated in the
tool procedure.

## Contributing to this skill

Change this router only to correct its shared concepts/routing or add a supported platform pointer.
Vendor details belong in that vendor's references. Recheck shared claims before adding a platform.

## Tools

A local pyATS/Genie CLI with device transport, or the Genie parser library for captured text.

## Verification checklist

- [ ] Tool and mode match an entry in the index.
- [ ] Requested collections produced data and evidence, or an explicit failure.
- [ ] Both comparison inputs contain collected state.
