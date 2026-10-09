---
name: host-state-query
description: >-
  Read host processes, file metadata and installed client capabilities. Use for Linux process listings, directory metadata and curl capability inspection. Covers Linux with procps-ng, GNU coreutils and curl. Assumes an already authorized shell or SSH session on the selected host.
---

# Host state query

Read host processes, file metadata and installed client capabilities.

## When to use this skill

Use for Linux process listings, directory metadata and curl capability inspection.

## Universal concepts

No common wire protocol is implied by this capability. A command reports the selected host’s observed state. Presence of a process or file is not proof of application health.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No process termination, file writes, service changes, credential collection or universal resource thresholds are included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an already authorized shell or SSH session on the selected host. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
