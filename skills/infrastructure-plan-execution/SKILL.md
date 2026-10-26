---
name: infrastructure-plan-execution
description: Prepare, review, and apply a declarative infrastructure plan, or plan its removal, then inspect the resulting recorded state and outputs and adopt an existing resource under management. Use when a configuration directory must be initialized, validated, planned, applied, or destroyed through a reviewed saved plan. Covers HashiCorp Terraform CLI. Assumes the CLI, an existing configuration, state backend access, and provider credentials are already available; this skill does not install tools or author configuration. Does not cover writing resource definitions, provider-specific resource design, or approval workflows.
argument-hint: "[platform] [action] [configuration_directory]"
---

# Infrastructure Plan Execution

Prepares a configuration, produces a reviewed plan, applies or destroys exactly that plan, and reads back recorded state, using the platform's own documented procedure and result vocabulary.

## When to use this skill

- A configuration directory must be initialized or validated before a change.
- A plan must be produced, reviewed, and then applied, or a removal plan produced and executed.
- Recorded resource addresses or outputs must be listed.
- An existing remote object must be bound to a resource address in the configuration.
- Not for writing or redesigning the configuration, installing the tool, or managing credentials.

## Universal concepts (apply regardless of platform)

- A plan describes proposed changes and is separate from applying it; applying can change or delete real resources.
- Where a platform documents a saved plan, applying that exact artifact is the reviewed path, and a failed or unreviewed plan is not eligible.
- Where documented, a failed apply is not rolled back automatically, so a failure can leave the infrastructure partially changed.
- Where documented, plan artifacts and state can hold sensitive values that terminal output hides.
- No wire-level standard governs this capability; claims here are hedged accordingly.

## Procedure

1. Identify the platform from the request or the `platform` argument. If it is not in `references/INDEX.md`, stop; do not improvise a procedure.
2. Follow `references/<platform>/procedure.md` exactly, including its confirmation gates.
3. Report the outcome in that procedure's own result vocabulary, preserving partial or incomplete results.

## Known limitations

- Does not author configuration, choose providers, or design resources.
- Platform coverage is exactly the platforms in `references/INDEX.md`.

## Contributing to this skill

Change this router only to correct shared concepts or add a pointer to a newly supported platform. Platform-specific operations, errors, and bindings belong under that platform's `references/` directory.

## Tools

A local command-line client for the platform, run in the configuration directory. Each procedure lists the operations it uses.

## Verification checklist

- [ ] Platform confirmed against `references/INDEX.md`
- [ ] That platform's `procedure.md` followed, including confirmation gates
- [ ] Apply or destroy used the exact plan the operator reviewed
- [ ] Result reported in the platform's own vocabulary, with partial failure stated
