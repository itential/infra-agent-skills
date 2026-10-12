---
name: device_reprovisioning
description: Validate and execute an approved staged device reset or baseline restoration. Use when this operation is requested on Cisco pyATS Clean. Assumes pyATS / Genie Clean, a testbed, and a platform-specific approved Clean definition. Stage selection, image compatibility, and recovery details require the selected platform documentation. This does not invent a universal erase or upgrade sequence.
---

# Device Reprovisioning

Validate and execute an approved staged device reset or baseline restoration using the selected platform's documented procedure.

## When to use this skill

Use to reset a network device to a known baseline through a pre-approved, platform-specific staged Clean definition, on Cisco pyATS Clean. It is destructive: it needs a written definition, image inputs and a recovery plan before it starts. For ordinary software upgrades see `software_upgrade_lifecycle`; for command-level changes see `device_cli_execution`.
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

Stage selection, image compatibility, and recovery details require the selected platform documentation. This does not invent a universal erase or upgrade sequence.

## Contributing to this skill

Change this router only to correct its shared concepts/routing or add a supported platform pointer.
Vendor details belong in that vendor's references. Recheck shared claims before adding a platform.

## Tools

Assumes pyATS / Genie Clean, a testbed, and a platform-specific approved Clean definition. The platform procedure lists the required operations or execution mechanism.

## Verification checklist

- [ ] Platform and operation match an entry in the index.
- [ ] The selected procedure's checks and any confirmation gates were followed.
- [ ] Actual results and documented failures are reported without replacing their status vocabulary.
