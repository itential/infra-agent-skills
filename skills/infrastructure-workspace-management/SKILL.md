---
name: infrastructure-workspace-management
description: >-
  Manage an infrastructure workspace and inspect its execution runs. Use for HCP Terraform workspace list/read/create/update/safe-delete, variable inspection, and run create/read/list/cancel. Covers HashiCorp HCP Terraform and Terraform Enterprise API v2. Assumes an authenticated API client authorized for the organization/workspace; run actions require a user or team token.
---

# Infrastructure workspace management

Manage an infrastructure workspace and inspect its execution runs.

## When to use this skill

Use for HCP Terraform workspace list/read/create/update/safe-delete, variable inspection, and run create/read/list/cancel.

## Universal concepts

No common wire protocol is implied by this capability. A workspace associates configuration and state with run history. A queued run is not a completed deployment.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

This procedure queues explicitly plan-only runs; apply, force-delete, and force-cancel are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated API client authorized for the organization/workspace; run actions require a user or team token. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
