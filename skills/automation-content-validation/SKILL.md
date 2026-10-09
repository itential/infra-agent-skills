---
name: automation-content-validation
description: >-
  Validate automation source files against an explicitly selected published rule profile. Use for Ansible playbook, role or project linting and rule/profile inspection. Covers Ansible ansible-lint. Assumes ansible-lint and project dependencies are installed in an isolated or otherwise trusted execution environment.
---

# Automation content validation

Validate automation source files against an explicitly selected published rule profile.

## When to use this skill

Use for Ansible playbook, role or project linting and rule/profile inspection.

## Universal concepts

No common wire protocol is implied by this capability. Validation findings describe the selected files and rule set; they do not establish deployment success. There is no cross-vendor lint-result standard.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No automatic fixes, production deployment, secret-detection guarantee or universal choice of policy profile is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes ansible-lint and project dependencies are installed in an isolated or otherwise trusted execution environment. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
