---
name: edge-configuration-query
description: >-
  Read configured edge-service records and their current platform state. Use for Cloudflare DNS zone/record, Worker/settings/build, Access application/policy, Tunnel/connection and ruleset reads. Covers Cloudflare API through its official MCP server. Assumes an authorized Cloudflare API MCP client and known account or zone scope.
---

# Edge Configuration Query

Read configured edge-service records and their current platform state.

## When to use this skill

Use for Cloudflare DNS zone/record, Worker/settings/build, Access application/policy, Tunnel/connection and ruleset reads.

## Universal concepts

No common wire protocol is implied by this capability. The selected account, zone and resource identifier are part of the query. Reading configured state does not execute a deployment or prove end-to-end connectivity.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No changes to DNS, Workers, Access policy, tunnels or rulesets occur. Build status is distinct from application runtime health.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authorized Cloudflare API MCP client and known account or zone scope. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
