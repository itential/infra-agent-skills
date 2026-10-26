---
name: network-state-collection
description: Capture structured network state before and after a change, or gather evidence while troubleshooting, by parsing command output, learning feature state, querying platform state or snapshots, and comparing saved snapshots. Use when you need observed state data to compare or inspect. Covers Cisco pyATS / Genie, IP Fabric, Forward Networks, and Arista CloudVision; assumes the chosen tool's access (a pyATS testbed or captured output, or an authenticated platform API client). It reports what was observed; it does not diagnose root causes or approve a change.
---

# Network State Collection

Parse command output, learn feature state, query platform snapshots, and compare saved snapshots to produce evidence of network state.

## When to use this skill

Use to record device state before a change and again after it, to turn raw command output into
structured data, or to gather evidence while troubleshooting. Health screens and
post-change verification belong to `network-health-verification`. Applying changes to devices is outside this skill.

## Universal concepts

- Snapshots, or reads of live or time-bounded state, are comparable only when both sides cover the same devices, commands or features, and scope.
- Where volatile fields (counters, timers) are present, they are handled by documented defaults or
  explicit exclusions, and state being checked is never excluded.
- A collection failure or empty result is incomplete data, not a healthy network.
- An empty difference establishes equality only for the fields actually collected.
- Parser, feature, and device coverage vary by tool and platform; unsupported or uncollected coverage is reported, not substituted or read as healthy.

## Procedure

1. Identify the requested tool and mode in [references/INDEX.md](references/INDEX.md).
2. Open the linked tool procedure and follow it exactly, including its confirmation gates.
3. Report results using that procedure's own status vocabulary.

## Known limitations

Collection and comparison report observed data only. Live collection or discovery is gated in
the tool procedure.

## Contributing to this skill

Change this router only to correct its shared concepts/routing or add a supported platform pointer.
Vendor details belong in that vendor's references. Recheck shared claims before adding a platform.

## Tools

A local pyATS/Genie CLI with device transport or the Genie parser library for captured text, or an authenticated API client for the IP Fabric, Forward Networks, or Arista CloudVision platform.

## Verification checklist

- [ ] Tool and mode match an entry in the index.
- [ ] Requested collections produced data and evidence, or an explicit failure.
- [ ] Both comparison inputs contain collected state.
