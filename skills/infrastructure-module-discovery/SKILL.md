---
name: infrastructure-module-discovery
description: >-
  Find versioned infrastructure provider and module documentation. Use for public or private Terraform Registry provider/module discovery and documentation retrieval. Covers HashiCorp Terraform MCP server. Assumes an approved Terraform MCP client; private registry queries also require authorized HCP Terraform or Terraform Enterprise access.
---

# Infrastructure module discovery

Find versioned infrastructure provider and module documentation.

## When to use this skill

Use for public or private Terraform Registry provider/module discovery and documentation retrieval.

## Universal concepts

No common wire protocol is implied by this capability. Publisher, namespace, component, and version identify the artifact being described.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Discovery does not install modules or prove that community code is safe or suitable.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an approved Terraform MCP client; private registry queries also require authorized HCP Terraform or Terraform Enterprise access. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
