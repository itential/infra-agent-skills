---
name: agent-security-inspection
description: >-
  Read agent security posture, component scan findings, and tool admission policy. Use for one-shot DefenseClaw skill or MCP scans, current guardrail/tool policy inspection, and alert/audit retrieval. Covers Cisco AI Defense DefenseClaw. Assumes an installed configured DefenseClaw CLI and authorized local shell.
---

# Agent security inspection

Read agent security posture, component scan findings, and tool admission policy.

## When to use this skill

Use for one-shot DefenseClaw skill or MCP scans, current guardrail/tool policy inspection, and alert/audit retrieval.

## Universal concepts

No common wire protocol is implied by this capability. A scanner finding and a runtime enforcement decision are different results. Scan scope, configured analyzers, and policy determine the reported evidence.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No installation, quarantine, exceptions, block/allow changes, guardrail disabling, SIEM/webhook configuration, or automatic remediation. MCP scans can start configured server processes and use configured external analyzers.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an installed configured DefenseClaw CLI and authorized local shell. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
