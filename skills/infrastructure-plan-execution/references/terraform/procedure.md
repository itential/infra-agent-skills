# Terraform CLI infrastructure plans

Prepare a Terraform working directory, execute a reviewed saved plan (apply or destroy), then read recorded state and outputs or import one existing resource.

Sources: HashiCorp Terraform CLI command reference pages for init, validate, plan, apply, import, output and state list, at developer.hashicorp.com/terraform/cli/commands, retrieved 2026-10-26.

## Common Sequences

- Configuration check: Initialize → Validate.
- Change or removal: Initialize → Validate → Plan → Review and apply → Inspect state and outputs.
- Adopt one existing resource: Initialize → Import → Plan.

## Initialize

`terraform init` in the configuration directory sets up the backend and installs modules and providers; it is safe to repeat. Success is completion without error; an error stops the sequence. Changing backend configuration can trigger state migration: stop and confirm with the operator before proceeding with `-migrate-state`, unless the operator's standing instructions pre-authorize the migration. `-force-copy` answers the migration prompts automatically, and `-reconfigure` abandons the existing configuration without migrating state. `-lock=false` disables state locking.

## Validate

`terraform validate -json` returns `valid`, `error_count`, `warning_count` and `diagnostics`. Valid means no errors; report warnings. Validation checks local syntax and internal consistency, not remote services or provider APIs. Terraform documents that an error before validation begins is not covered by the JSON setting, so stdout that is not valid JSON is a generic error, not a pass.

## Plan

`terraform plan -out=<plan-file> -detailed-exitcode` writes a saved plan; adding `-destroy` plans removal of all objects the configuration currently manages. Exit 0 is no changes, 2 is changes proposed, 1 is error. A failed plan is not eligible for apply. Missing variables, provider errors and lock errors are resolved at their cause; Terraform documents `-lock=false` as dangerous when others may run commands against the same workspace. The plan file holds sensitive values in cleartext even when terminal output hides them, so protect the file as a secret.

## Review and apply

`terraform show <plan-file>` displays the plan. Stop and confirm with the operator before proceeding, covering every deletion and replacement in it, unless the operator's standing instructions pre-authorize applying this saved plan. Then `terraform apply <plan-file>`. Applying a saved plan does not prompt, so this gate is the only approval. Success is a completed apply with its change summary. A failed apply may leave infrastructure partly changed; Terraform documents that it does not roll back a partially completed apply and that the configuration must be applied again after the error is resolved. Not documented: behavior when state changed between saving the plan and applying it.

## Inspect state and outputs

`terraform state list` prints managed resource addresses; an address pattern or `-id` narrows it. `terraform output` lists root outputs and shows sensitive ones as `<sensitive>`. A named output, `-json` and `-raw` print sensitive values in plain text, so keep that result out of shared channels. Both commands read recorded state and are not a live health check.

## Import

`terraform import <resource-address> <object-id>` binds one existing remote object to one address; the object ID format comes from the provider's documentation. It does not generate configuration. Import changes recorded state only, not the remote object. Binding one object to several addresses is warned against. Not documented on the import page: whether the resource block must exist first and what to run afterwards; assumption: write the block first and run Plan afterwards to see differences from the real object. Provider or import errors mean the adoption is unverified.

## Patterns

Only the saved plan file that was reviewed is applied.

## Known limitations

- A successful apply says nothing about application health.
- Provider-specific failures are documented by each provider, not the CLI reference.
- Destroy is carried out by applying a saved destroy plan; the interactive `terraform destroy` command is not part of this procedure.

## Tools

| Operation | Description | Category |
|---|---|---|
| Local CLI session | Runs the commands above in the configuration directory | Local process |

## Verification checklist

- Init and validate succeeded for the intended configuration directory.
- Plan exit code and diagnostics were kept.
- Apply used the reviewed saved plan, after operator confirmation or standing pre-authorization.
- Apply failures are reported as possibly partial, with no rollback claim.
- State and output reads did not expose sensitive values.
