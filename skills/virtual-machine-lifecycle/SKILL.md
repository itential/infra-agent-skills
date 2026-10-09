---
name: virtual-machine-lifecycle
description: >-
  Create, start, stop, reset, resize or delete one virtual machine and verify its asynchronous operation. Use for Google Compute Engine instance lifecycle through official MCP tools. Covers Google Cloud Compute Engine MCP. Assumes an authenticated Google Cloud Compute MCP client with required operation permissions and explicit project, zone and instance identity.
---

# Virtual Machine Lifecycle

Create, start, stop, reset, resize or delete one virtual machine and verify its asynchronous operation.

## When to use this skill

Use for Google Compute Engine instance lifecycle through official MCP tools.

## Universal concepts

No common wire protocol is implied by this capability. A returned operation identifier records acceptance; completion requires the platform operation result. Resource changes can affect running workloads.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

The tool exposes a limited creation schema. Networks, arbitrary boot-disk options and rollback are not invented or supplied through undocumented inputs.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Google Cloud Compute MCP client with required operation permissions and explicit project, zone and instance identity. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
