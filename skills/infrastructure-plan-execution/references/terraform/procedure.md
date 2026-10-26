# Terraform CLI infrastructure plans

Prepare a Terraform working directory, then execute a reviewed saved plan for its selected workspace.

Sources: HashiCorp Terraform CLI command reference pages for init, fmt, validate, plan, apply, import, output and state list, at developer.hashicorp.com/terraform/cli/commands, retrieved 2026-10-26.

## Common Sequences

- Configuration check: Initialize → Format check → Validate.
- Change or removal: Initialize → Validate → Plan → Review and apply → Inspect state and outputs.
- Adopt one existing resource: Initialize → Import → Plan.

## Initialize

`terraform init` in the configuration directory sets up the backend and installs modules and providers; it is safe to repeat. Success is completion without error; an error stops the sequence. Changing backend configuration can trigger state migration: stop and confirm with the operator before proceeding with `-migrate-state`. `-force-copy` answers the migration prompts automatically and `-reconfigure` skips migration entirely, so use neither. Lock handling is not changed by this procedure (`-lock=false` is not used).

## Format check

`terraform fmt -check -diff` reports formatting differences without rewriting. Exit 0 means formatted; non-zero means differences exist (the documentation does not distinguish a command error by exit code, so read the output). Plain `terraform fmt` rewrites files in place: stop and confirm with the operator before proceeding with it.

## Validate

`terraform validate -json` returns `valid`, `error_count`, `warning_count` and `diagnostics`. Valid means no errors; report warnings. Validation checks local syntax and internal consistency, not remote services or provider APIs. Stdout that is not valid JSON means a failure before validation began; treat it as an error, not a pass.

## Plan

`terraform plan -out=<plan-file> -detailed-exitcode` writes a saved plan; adding `-destroy` plans removal of everything in the workspace. Exit 0 is no changes, 2 is changes proposed, 1 is error. A failed plan is not eligible for apply. Resolve missing variables, provider errors and lock errors at their cause; `-lock=false` is documented as dangerous with concurrent users and is not used. The plan file holds sensitive values in cleartext even when terminal output hides them, so protect the file as a secret.

## Review and apply

`terraform show <plan-file>` displays the plan. Stop and confirm with the operator before proceeding, covering every deletion and replacement in it, then run `terraform apply <plan-file>`. Applying a saved plan does not prompt, and `-auto-approve` is ignored for it, so the operator gate is the only approval. Success is a completed apply with its change summary. If it fails, Terraform records completed changes in state and does not roll back; report partial completion and produce a new plan for any follow-up.

## Inspect state and outputs

`terraform state list` prints managed resource addresses; an address pattern or `-id` narrows it. `terraform output` lists root outputs and shows sensitive ones as `<sensitive>`. A named output, `-json` and `-raw` print sensitive values in plain text, so keep that result out of shared channels. Both commands read recorded state and are not a live health check.

## Import

`terraform import <resource-address> <object-id>` binds one existing remote object to one address; the object ID format comes from the provider's documentation. It does not generate configuration. Stop and confirm with the operator before proceeding, since it changes state. Binding one object to several addresses is warned against. Not documented on the import page: whether the resource block must exist first and what to run afterwards; assumption: write the block first and run Plan afterwards to see differences from the real object. Provider or import errors mean the adoption is unverified.

## Patterns

A speculative plan is not the final saved plan; apply only the file that was reviewed.

## Known limitations

- A successful apply says nothing about application health.
- Provider-specific failures are documented by each provider, not the CLI reference.
- Plain `terraform destroy` exists but prompts interactively; this procedure uses a saved destroy plan so the exact removals are reviewed.

## Tools

| Operation | Description | Category |
|---|---|---|
| Local CLI session | Runs the commands above in the configuration directory | Local process |

## Verification checklist

- Init and validate succeeded for the intended directory and workspace.
- Plan exit code and diagnostics were kept.
- Apply used the reviewed saved plan, after operator confirmation.
- Apply failures are reported as possibly partial, with no rollback claim.
- State and output reads did not expose sensitive values.
