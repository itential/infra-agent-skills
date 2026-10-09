---
name: network-state-collection
description: >-
  Collect structured network state and perform supported snapshot comparisons. Use for pyATS/Genie command parsing, feature learning and comparisons, NAPALM read-only getters, or Linux iproute2 link/address/route inspection. Covers Cisco pyATS / Genie, NAPALM, and Linux iproute2. Assumes the selected collector or CLI and its required device access or captured input are available.
---

# Network State Collection

Collect structured network state and perform supported snapshot comparisons.

## When to use this skill

Use for pyATS/Genie command parsing, feature learning and comparisons, NAPALM read-only getters, or Linux iproute2 link/address/route inspection. Supported platforms: Cisco pyATS / Genie, NAPALM, and Linux iproute2.

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

Assumes the selected collector or CLI and its required device access or captured input are available. The selected procedure lists required operations and bindings.

## Verification checklist

- [ ] Platform and operation match an entry in the index.
- [ ] The selected procedure's checks and any confirmation gates were followed.
- [ ] Actual results and documented failures are reported without replacing their status vocabulary.
