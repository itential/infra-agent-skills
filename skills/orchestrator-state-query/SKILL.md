---
name: orchestrator-state-query
description: >-
  Read device and service records maintained by a network orchestrator. Use for Cisco NSO device groups, NED identifiers, platform/configuration/state records, device synchronization checks, and service type/instance discovery. Covers Cisco NSO through its publisher MCP server. Assumes an authenticated NSO MCP client and enabled NSO RESTCONF access.
---

# Orchestrator state query

Read device and service records maintained by a network orchestrator.

## When to use this skill

Use for Cisco NSO device groups, NED identifiers, platform/configuration/state records, device synchronization checks, and service type/instance discovery.

## Universal concepts

No common wire protocol is implied by this capability. Stored configuration and observed device state are different evidence. A device synchronization result does not establish a service deployment outcome.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Service creation, redeployment, and automatic reconciliation are outside scope. Model-specific fields and device relationships are not universal.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated NSO MCP client and enabled NSO RESTCONF access. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
