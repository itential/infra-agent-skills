---
name: cloud-compute-query
description: >-
  Read scoped compute inventory, storage, templates and capacity records. Use for Google Cloud project discovery and Compute Engine VM, managed group, disk, snapshot, template, machine/accelerator/image, reservation and commitment reads. Covers Google Cloud Compute Engine and Resource Manager MCP. Assumes authenticated Google Cloud MCP clients with required tool and resource read permissions.
---

# Cloud Compute Query

Read scoped compute inventory, storage, templates and capacity records.

## When to use this skill

Use for Google Cloud project discovery and Compute Engine VM, managed group, disk, snapshot, template, machine/accelerator/image, reservation and commitment reads.

## Universal concepts

No common wire protocol is implied by this capability. Project and location scope determine which records a query covers. Resource inventory, provisioned configuration and measured utilization are different data.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No infrastructure mutation, billing optimization recommendation or instance network-interface detail is inferred from basic-info responses.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes authenticated Google Cloud MCP clients with required tool and resource read permissions. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
