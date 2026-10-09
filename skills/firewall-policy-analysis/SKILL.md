---
name: firewall-policy-analysis
description: >-
  Compare a candidate firewall rule with an existing policy using a documented offline analysis engine. Use for vendor-format parsing, normalized rule inspection and candidate overlap analysis. Covers AutomateIP FWRule MCP, with its documented multi-vendor parsers. Assumes an available FWRule MCP client and operator-supplied configuration or normalized rule data.
---

# Firewall Policy Analysis

Compare a candidate firewall rule with an existing policy using a documented offline analysis engine.

## When to use this skill

Use for vendor-format parsing, normalized rule inspection and candidate overlap analysis.

## Universal concepts

No common wire protocol is implied by this capability. Results describe the supplied policy model; parser fidelity and object resolution affect the answer.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No firewall change or business approval decision is performed. Supported input formats and parser limits are defined by the engine.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an available FWRule MCP client and operator-supplied configuration or normalized rule data. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
