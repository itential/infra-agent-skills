---
name: network-inventory-query
description: >-
  Retrieve network inventory records and supported stored entity context from a selected management platform. Use for read-only host/device, interface, network and component inventory, plus documented related monitoring or entity context. Covers Zabbix and Auvik. Assumes an authenticated API client for the selected platform.
---

# Query network inventory

Retrieve network inventory records and supported stored entity context from a selected management platform.

## When to use this skill

Use for read-only host/device, interface, network and component inventory, plus documented related monitoring or entity context. Supported platforms: Zabbix and Auvik.

## Universal concepts

No common wire protocol is implied by this capability. Inventory reflects records visible to the caller. A missing match can be caused by scope or permissions; records and observations retain their platform identifiers.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This does not create assets, repair source-of-truth drift, or establish physical reachability from inventory alone.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API client for the selected platform. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
