---
name: device_cli_execution
description: Execute approved CLI commands or apply an approved configuration through a device session. Use when this operation is requested on Cisco pyATS / Unicon. Assumes a pyATS environment with the matching Unicon plugin and device credentials. The caller supplies platform-documented commands and verification criteria. This is a transport procedure, not a generic configuration design or rollback recipe.
---

# Device CLI Execution

Execute approved CLI commands or apply an approved configuration through a device session using the selected platform's documented procedure.

## When to use this skill

Use to run an approved show/exec command or push an approved configuration to a network device over its CLI session and capture the output, on Cisco pyATS / Unicon. Pair it with a platform procedure that supplies the commands and the expected post-change state. For parsing or comparing the output see `network_state_collection`; for staged resets see `device_reprovisioning`.
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

The caller supplies platform-documented commands and verification criteria. This is a transport procedure, not a generic configuration design or rollback recipe.

## Contributing to this skill

Change this router only to correct its shared concepts/routing or add a supported platform pointer.
Vendor details belong in that vendor's references. Recheck shared claims before adding a platform.

## Tools

Assumes a pyATS environment with the matching Unicon plugin and device credentials. The platform procedure lists the required operations or execution mechanism.

## Verification checklist

- [ ] Platform and operation match an entry in the index.
- [ ] The selected procedure's checks and any confirmation gates were followed.
- [ ] Actual results and documented failures are reported without replacing their status vocabulary.
