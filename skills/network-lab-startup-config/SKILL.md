---
name: network-lab-startup-config
description: >-
  Read, replace, or extract supported lab-node startup configuration. Use for CML stored configuration handling and EVE-NG native export of a node configuration into its lab. Covers Cisco CML, EVE-NG. Assumes an authenticated API or supported SDK client for the target lab platform.
---

# Network lab startup configuration

Read, replace, or extract supported lab-node startup configuration.

## When to use this skill

Use for CML stored configuration handling and EVE-NG native export of a node configuration into its lab.

## Universal concepts

No common wire protocol is implied by this capability. Stored configuration and running guest configuration are separate states. Extracting a configuration can overwrite the stored version.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Guest CLI edits, unsupported node extraction, and EVE-NG direct lab-file manipulation are outside this capability.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API or supported SDK client for the target lab platform. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
