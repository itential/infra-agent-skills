---
name: diagram-rendering
description: >-
  Render supplied diagram source with a selected publisher-supported renderer. Use for rendering supplied XML/CSV/Mermaid, Markdown mind maps, supported diagram text, or an approved Python Diagrams definition. Covers draw.io MCP, Markmap CLI, Kroki, and Python Diagrams. Assumes the selected renderer is installed or an approved rendering service/client is available.
---

# Diagram rendering

Render supplied diagram source with a selected publisher-supported renderer.

## When to use this skill

Use for rendering supplied XML/CSV/Mermaid, Markdown mind maps, supported diagram text, or an approved Python Diagrams definition. Supported platforms: draw.io MCP, Markmap CLI, Kroki, and Python Diagrams.

## Universal concepts

No common wire protocol is implied by this capability. A rendered view reflects supplied source, not discovered network state. Supported languages and output formats depend on the selected renderer.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Topology discovery, inferred architecture, branding rules and automatic publication are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes the selected renderer is installed or an approved rendering service/client is available. The selected procedure lists required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
