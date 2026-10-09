---
name: cloud-network-inspection
description: >-
  Read cloud network configuration and traffic evidence for a specified scope. Use for scoped cloud network configuration reads, supported AWS log/model evidence, Azure network inspection, or Equinix Fabric and Network Edge inventory. Covers AWS Network MCP, Azure CLI, Equinix Fabric, and Equinix Network Edge. Assumes the selected API/MCP client or CLI is authenticated with the documented read/query permissions.
---

# Cloud network inspection

Read cloud network configuration and traffic evidence for a specified scope.

## When to use this skill

Use for scoped cloud network configuration reads, supported AWS log/model evidence, Azure network inspection, or Equinix Fabric and Network Edge inventory. Supported platforms: AWS Network MCP, Azure CLI, Equinix Fabric, and Equinix Network Edge.

## Universal concepts

No common wire protocol is implied by this capability. Configuration, observed traffic, and modeled changes are distinct evidence types. An empty query is limited to its selected resources and any account, location or time filters supported by that platform.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No network resource mutation or universal security/compliance verdict is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes the selected API/MCP client or CLI is authenticated with the documented read/query permissions. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
