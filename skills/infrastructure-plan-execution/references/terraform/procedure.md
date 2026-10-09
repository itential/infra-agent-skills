# Terraform CLI infrastructure plans

Prepare a Terraform working directory and execute a reviewed plan for that directory's selected workspace.

Sources: HashiCorp's current CLI references for [init](https://developer.hashicorp.com/terraform/cli/commands/init), [fmt](https://developer.hashicorp.com/terraform/cli/commands/fmt), [validate](https://developer.hashicorp.com/terraform/cli/commands/validate), [plan](https://developer.hashicorp.com/terraform/cli/commands/plan), [apply](https://developer.hashicorp.com/terraform/cli/commands/apply), [destroy](https://developer.hashicorp.com/terraform/cli/commands/destroy), [output](https://developer.hashicorp.com/terraform/cli/commands/output), [state list](https://developer.hashicorp.com/terraform/cli/commands/state/list), and [import](https://developer.hashicorp.com/terraform/cli/commands/import), retrieved 2026-10-09.

## Common Sequences

- Configuration check: Initialize → Format/check → Validate.
- Infrastructure change or removal: Initialize → Validate → Plan → Inspect and apply → Inspect state/output.
- Adopt one existing resource: Initialize → Import → Plan; applying later follows the change sequence.

## Initialize

Initialization runs `terraform init` in the chosen configuration directory. It installs required modules/providers and prepares the backend. A completed initialization permits later commands; initialization errors stop the sequence. Backend migration is separate: before a state migration, stop and confirm with the operator before proceeding; the documented migration prompts remain enabled. This procedure does not bypass locks or use forced migration.

## Format/check

`terraform fmt -check -diff` checks formatting without rewriting files. A nonzero result means formatting differs or a command error occurred; the diagnostics distinguish them. If rewriting is requested, stop and confirm with the operator before proceeding with `terraform fmt`; its output names changed files.

## Validate

`terraform validate -json` returns the validity flag, error/warning counts, and diagnostics. A valid configuration has no validation errors; warnings remain reportable. Output that is not JSON can represent a failure before validation began and is a command error, not a successful empty result. Validation checks configuration consistency, not remote service behavior.

## Plan

`terraform plan -out=<plan-file> -detailed-exitcode` creates a saved plan. For removal, `terraform plan -destroy -out=<plan-file> -detailed-exitcode` creates a destroy plan. Exit 0 means no changes, 2 means proposed changes, and 1 means error. A failed plan is not eligible for apply. Missing variables, provider errors, and state-lock errors require resolving the reported cause; disabling locking is not part of this procedure.

## Inspect and apply

`terraform show <plan-file>` displays the saved plan. Before applying the exact reviewed file, **stop and confirm with the operator before proceeding**, including every deletion/replacement it contains. `terraform apply <plan-file>` executes that plan without another approval prompt. Success is a completed apply with its change summary. On failure, Terraform records completed changes in state and does not roll them back; the failure is reported with partial completion, then a new plan is required for any follow-up change. A timeout is not evidence that nothing changed.

## Inspect state/output

`terraform state list` lists managed resource addresses; `terraform output` lists root outputs. A selected output or JSON/raw output can reveal sensitive values even when ordinary output redacts them; the result must remain in an approved secret-capable channel. These commands inspect recorded state and are not an independent live-resource health test.

## Import

The resource block and its provider configuration already exist, and the provider's own import documentation supplies the object ID. Before changing state, **stop and confirm with the operator before proceeding**. `terraform import <resource-address> <object-id>` binds one existing object to one address; it does not generate configuration. One remote object must not be bound to multiple addresses. A successful import is followed by Plan to reveal differences between configuration and the imported object. Provider/import errors leave the adoption unverified.

## Patterns

Saved plans can contain unredacted sensitive data. Plan review and artifact handling therefore cover the file itself, not just terminal output. A speculative plan is not interchangeable with the final saved plan.

## Known limitations

A successful apply is not an application health assertion. Provider-specific failures are not enumerated by Terraform's generic CLI reference; their exact diagnostics require the provider's documentation. Direct `terraform destroy` is an alternative interactive command, but this procedure uses a saved destroy plan so the exact removals can be reviewed.

## Tools

| Operation | Description | Category |
|---|---|---|
| Local Terraform CLI | Runs the documented commands in the selected configuration directory | Local process |

## Verification checklist

- Initialization and validation completed for the intended directory/workspace.
- Plan exit status and all diagnostics were preserved.
- The approved saved plan is the file supplied to apply.
- Apply failures are reported as potentially partial, without a rollback claim.
- State/output inspection does not disclose secret values.
