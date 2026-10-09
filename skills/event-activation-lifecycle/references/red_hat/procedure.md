# AAP 2.6 rulebook activation lifecycle

Red Hat Automation Decisions creates a rulebook activation and manages its event-processing lifecycle through the platform UI.

Sources: [Define rules that trigger automation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/administer-assembly_eda_rulebook_activations) and [Manage active integrations](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/administer-assembly_eda_manage_active_rulebook_activations), AAP 2.6, retrieved 2026-10-09.

## Common Sequences

- New activation: Inspect prerequisites → Create activation → Inspect activation/output.
- Lifecycle change: Inspect activation/output → Change enabled state or Restart activation → Inspect activation/output.
- Removal: Inspect activation/output → Delete activation.

## Inspect prerequisites

The documented creation flow assumes an authenticated Content Consumer, a prepared project and a decision environment. The selected project determines the rulebook choices. The available organization, rulebook, runtime and permitted credentials are identified before creation. Missing dependencies prevent completing the creation flow; this procedure does not create substitutes.

## Create activation

The Automation Decisions area contains the Rulebook Activations page and its creation form. The form records a name, organization, selected rulebook and decision environment, together with optional description, project, credentials, service name and variables. The requested restart policy, log level, enabled state and audit option are explicit. At most one selected credential may be of the AAP credential type; sensitive values belong in credentials rather than ordinary variables.

Before saving the new activation, **stop and confirm with the operator before proceeding**, including its enabled state and event-driven actions. The creation control saves it and opens its detail page. Success means the record exists; its initial Pending, Running or Failed state is retained. Failed is not operational success, and Pending is not Running.

## Inspect activation/output

The activation list provides status, event-fire count and restart information. Selecting an activation opens its details. For an activation that has executed, History lists execution instances; selecting one displays its output. A Running activation is processing its configured rules, not proof that every action succeeded. Runtime or task errors remain in the selected instance's output.

## Change enabled state

Before changing the row's enabled switch, **stop and confirm with the operator before proceeding**, because it starts or stops event processing. The UI confirmation identifies the affected activation count and requires the explicit confirmation selection and matching enable/disable action. Success is the changed enabled state and its subsequent native status. Redis unavailability blocks a transition to enabled or disabled when it would change the current state; the failure remains unresolved rather than bypassing the control.

## Restart activation

The documented restart is available only for an enabled activation whose restart policy was set to Always. Before invoking Restart from its action menu, **stop and confirm with the operator before proceeding**. The UI confirmation and restart action are both part of the operation. Subsequent status and History show the new execution. Redis unavailability blocks restart. A restart request or Pending state does not prove the activation reached Running.

## Delete activation

Before deleting the selected activation, **stop and confirm with the operator before proceeding**: this permanently removes the activation and its configuration. The action-menu deletion opens the publisher's explicit confirmation, followed by the delete action. The result is removal of that activation from the managed list. Redis unavailability blocks deletion; a failed delete is not reported as removal.

## Patterns

Always policy restarts after process exit, with the publisher's maximum of five restarts. On failure retries only failed processes, after 60 seconds by default, also at most five times. Never disables this automatic restart behavior. These are platform controls, not retry values invented by the skill.

A source-plugin shutdown can end an activation normally and cancel actions still waiting, with an informational log entry. A normal process exit therefore does not establish execution of all queued work.

## Known limitations

Deletion is permanent. Existing project/runtime/rulebook prerequisites are not provisioned here. Enabling creation, lifecycle changes and deletion depend on the documented Redis service. Auto-restart/project-sync setting changes, rulebook catalog operations, decision-environment creation and event-stream inventory are unconverted portions of the source.

## Tools

| Mechanism | Purpose | Category |
|---|---|---|
| Authenticated AAP browser session | Operate documented activation pages and confirmation dialogs | Read/write |

## Verification checklist

- Target organization, rulebook, runtime and credentials match the request.
- Mutation steps preserve the platform's confirmation dialog.
- Native enabled/status/history output is reported; Pending and Failed are not Running.
- Restart eligibility and Redis-related failures remain visible.
