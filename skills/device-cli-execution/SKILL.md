---
name: device-cli-execution
description: >-
  Execute approved device commands or transport an approved configuration through a supported session. Use for platform-supported CLI execution, including read-only Netmiko and Junos inspection and the documented pyATS/Unicon or RADKit transport modes. Covers Cisco pyATS / Unicon, Cisco RADKit, Netmiko, and Juniper Junos CLI. Assumes the selected session client, matching platform support, credentials and caller-supplied approved commands are available.
---

# Device CLI Execution

Execute approved device commands or transport an approved configuration through a supported session.

## When to use this skill

Use for platform-supported CLI execution, including read-only Netmiko and Junos inspection and the documented pyATS/Unicon or RADKit transport modes. Supported platforms: Cisco pyATS / Unicon, Cisco RADKit, Netmiko, and Juniper Junos CLI.

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

Assumes the selected session client, matching platform support, credentials and caller-supplied approved commands are available. The selected procedure lists required operations and bindings.

## Verification checklist

- [ ] Platform and operation match an entry in the index.
- [ ] The selected procedure's checks and any confirmation gates were followed.
- [ ] Actual results and documented failures are reported without replacing their status vocabulary.
