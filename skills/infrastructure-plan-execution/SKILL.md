---
name: infrastructure-plan-execution
description: >-
  Prepare, inspect, and apply an infrastructure execution plan. Use for Terraform CLI initialization, formatting, validation, plan/apply, destroy planning, state listing, output inspection, and import. Covers HashiCorp Terraform CLI. Assumes Terraform CLI, an existing configuration, backend access, and provider credentials are available.
---

# Infrastructure plan execution

Prepare, inspect, and apply an infrastructure execution plan.

## When to use this skill

Use for Terraform CLI initialization, formatting, validation, plan/apply, destroy planning, state listing, output inspection, and import.

## Universal concepts

No common wire protocol is implied by this capability. A plan describes proposed changes; applying it can alter or remove managed resources.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Provider-specific resource design and business approval systems are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes Terraform CLI, an existing configuration, backend access, and provider credentials are available. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
