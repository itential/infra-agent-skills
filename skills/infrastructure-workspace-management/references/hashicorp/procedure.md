# HCP Terraform workspace and plan-run lifecycle

Manage a workspace record or queue and inspect a speculative plan without applying infrastructure changes.

Sources: current HashiCorp [workspaces](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces), [runs](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run), [workspace variables](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables), and [API overview](https://developer.hashicorp.com/terraform/cloud-docs/api-docs), retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Workspace change: Locate workspace → Create/update workspace → Read workspace.
- Plan: Read workspace → Create plan-only run → Read run; optional Cancel run → Read run.
- Remove empty workspace: Read workspace → Safe-delete workspace.

## Locate workspace

Listing is scoped to the organization and requested filters. All pages are followed before claiming a complete list. Fuzzy name matching is discovery only; the resulting ID or exact organization/name selects Read workspace. No match is not a permissions test.

## Read workspace

The detail result identifies configuration, execution mode and associated workspace state. Variables are a separate read operation: it returns variable metadata and readable values, while sensitive values are unavailable after writing. Reports omit values that could contain credentials. Missing/unauthorized responses leave the identity unresolved.

## Create/update workspace

The organization, name and intended settings are supplied by the operator. **Stop and confirm with the operator before proceeding**, because execution settings can affect later infrastructure runs. Creation returns the new workspace; an update is verified through Read workspace. A rename also changes its name-based API/UI address. Agent execution requires an agent pool; local execution only stores state. Conflicting or invalid attributes require correcting the request. VCS linkage, project movement, and inherited-setting overrides require their specific permissions and approved values rather than guessed defaults.

## Create plan-only run

Before queuing the remote execution, **stop and confirm with the operator before proceeding**, including the workspace and configuration version. The request explicitly selects a speculative plan and the intended workspace/configuration version. If a configuration version is omitted, the platform uses the latest version for the workspace. A created run returns its ID, not a successful plan. Its subsequent result comes from Read run. Organization tokens cannot perform this action. Malformed input or an inaccessible workspace prevents creation; after an uncertain submission, run inventory is inspected before another submission.

## Read run

A specific run's native status is retained. A completed speculative plan has `planned_and_finished`; `policy_soft_failed` and `errored` are final failures, and cancellation is a separate outcome. Active stages remain in progress. Run inventory is paginated and, by default, excludes plan-only runs: the operation filter must include `plan_only` when inspecting these runs. The published list-runs rate limit is 30 requests per minute, so it is not a high-frequency polling substitute for a specific run lookup.

## Cancel run

Before interrupting a planning or applying run, **stop and confirm with the operator before proceeding**. The ordinary cancellation request queues an interrupt; acceptance does not prove the process stopped. Read run establishes the eventual state. A conflict means the run is not in a cancellable stage. This procedure does not escalate to force-cancel or claim cancellation rolled back changes.

## Safe-delete workspace

Before deletion, **stop and confirm with the operator before proceeding**, including loss of workspace records. The safe-delete operation refuses workspaces still managing resources. Successful deletion returns no content; a conflict is a refusal and must not be retried as force-delete. Not-found can also mean unauthorized access, so it is not by itself proof of successful deletion.

## Patterns

A plan-only run cannot later be applied. Workspace deletion is different from infrastructure destruction. Every run/report retains workspace and configuration identity.

## Known limitations

This procedure deliberately does not apply runs or modify variable values. A stored workspace variable value may be secret even without the sensitive flag. Error responses and response codes remain native; authentication/authorization, malformed requests, conflicts, throttling and server failures are not normalized to empty results.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read workspace/variables | Reads workspace identity and authorized metadata | Read |
| Create/update workspace | Changes the workspace record | Write |
| Create plan-only run | Queues a speculative plan | Execution |
| Read runs | Reads paginated history or a particular status | Read |
| Cancel run | Queues a normal interrupt | Execution control |
| Safe-delete workspace | Removes only a workspace without managed resources | Destructive |

## Verification checklist

- Organization, workspace ID, and configuration version are recorded.
- Speculative plan completion is distinct from infrastructure apply.
- Cancellation is verified through the resulting run status.
- Safe-delete conflicts preserve the resource-protection gate.
