---
name: firewall-rule-management
description: >-
  Read, create, update, delete, and activate a cloud firewall rule. Use for Zscaler ZIA cloud firewall rule objects and their staged activation. Covers Zscaler Internet Access through the publisher MCP server. Assumes an authenticated Zscaler MCP client with explicit write-tool enablement for changes.
---

# Firewall rule management

Read, create, update, delete, and activate a cloud firewall rule.

## When to use this skill

Use for Zscaler ZIA cloud firewall rule objects and their staged activation.

## Universal concepts

No common wire protocol is implied by this capability. A rule identifies match conditions, an action, and platform-specific placement. The vendor procedure distinguishes stored configuration from its activation state.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This capability covers ZIA cloud firewall rules, not URL filtering, access-policy rules, DLP or firewall appliance configuration.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Zscaler MCP client with explicit write-tool enablement for changes. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
