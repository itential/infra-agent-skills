---
name: controller-data-query
description: >-
  Retrieve an explicitly scoped controller record using a documented read operation. Use for reading inventory, configuration, health, wireless, or compliance records from a supported controller. Covers Cisco Meraki, Cisco Catalyst Center, Cisco ACI APIC and Arista CloudVision. Assumes an authenticated publisher MCP or native API client and an account authorized to read the target controller.
---

# Controller data query

Retrieve an explicitly scoped controller record using a documented read operation.

## When to use this skill

Use for reading inventory, configuration, health, wireless, or compliance records from a supported controller.

## Universal concepts

No common wire protocol is implied by this capability. The selected publisher reference or live catalogue identifies supported operations and their required inputs. Results describe the selected controller, account, filters, and observation interval.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This capability performs record retrieval, not a root-cause diagnosis, compliance judgment, or configuration change. Available operations depend on the publisher reference or catalogue and controller release.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated publisher MCP or native API client and an account authorized to read the target controller. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
