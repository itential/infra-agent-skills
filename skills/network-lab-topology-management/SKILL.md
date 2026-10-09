---
name: network-lab-topology-management
description: >-
  Inspect and modify links between explicitly selected lab interfaces. Use for link or virtual-network creation, inspection, supported isolation, and deletion. Covers GNS3 v2, Cisco CML, EVE-NG. Assumes an authenticated API or supported SDK client for the target lab platform.
---

# Network lab topology management

Inspect and modify links between explicitly selected lab interfaces.

## When to use this skill

Use for link or virtual-network creation, inspection, supported isolation, and deletion.

## Universal concepts

No common wire protocol is implied by this capability. Connectivity is defined by platform-specific node/interface or network identities. Interface names alone are not a portable connection identifier.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This capability implements an already supplied topology; it does not select an architecture or infer cabling intent.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API or supported SDK client for the target lab platform. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
