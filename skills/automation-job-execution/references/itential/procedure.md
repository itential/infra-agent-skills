# Itential existing-workflow execution

Itential MCP discovers an enabled workflow endpoint, starts it with its declared inputs and reads its job state.

Sources: [publisher tool reference](https://github.com/itential/itential-mcp/blob/devel/docs/tools.md) and [Operations Manager tools](https://github.com/itential/itential-mcp/blob/devel/src/itential_mcp/models/operations_manager.py), current devel, retrieved 2026-10-09. Literal bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- Launch workflow: Discover workflows → Review inputs → Start workflow → Read job.
- Inspect prior execution: List jobs → Read job.

## Discover workflows

Discovery returns enabled workflow endpoints with their route names and input schemas. Success identifies the requested existing workflow and its endpoint. No matching enabled endpoint is not a reason to expose one automatically. An agent automation is a different component type and is outside this workflow-only procedure.

## Review inputs

The selected endpoint schema determines required fields and types. The publisher's trigger can coerce some values from strings, but it also logs a warning and continues if schema lookup for coercion fails. This procedure treats unavailable required input semantics as unresolved before starting a job, rather than depending on that fallback. Credentials stay in the configured platform integration, not in an execution report.

## Start workflow

Before starting the workflow, **stop and confirm with the operator before proceeding**, including endpoint, input values and affected systems. Success returns a workflow job identifier and native job state. A session identifier instead indicates an agent automation, which is outside this route; it is not a workflow job success. Permission, validation or transport failures retain their details. An ambiguous response requires checking jobs before replay because the workflow might already be running.

## List jobs

Job discovery can filter by workflow and project. Success returns job identifiers, names and native statuses. Missing jobs and failed list requests remain separate outcomes. The supplied source does not establish a complete paging/error contract; the deployed tool schema and returned result determine completeness.

## Read job

The returned job identifier retrieves tasks, metrics and execution state. Native complete indicates workflow completion; running or paused remains unfinished. Error, canceled/cancelled and incomplete states are reported as returned. The publisher's list and detail descriptions use different cancellation spellings; no spelling is normalized away. Success of the query is distinct from success of the workflow. A missing or failed job read does not establish completion.

## Patterns

A route name comes from discovery rather than the human-readable workflow title. The current workflow-specific start tool delegates to a generic trigger; component identity therefore remains part of verification.

## Known limitations

Only existing workflow execution and inspection are covered. Definition authoring, endpoint exposure, agent sessions, templates, device changes, platform services, inventory, lifecycle resources, integrations and performance metrics from the broad source remain outside this procedure. Job side effects and rollback belong to the selected workflow's own contract.

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Discover workflows | Read enabled endpoints and input schemas | Read |
| Start workflow | Start selected existing workflow | Write |
| List jobs / Read job | Retrieve execution identity and native state | Read |

## Verification checklist

- Selected component is a workflow with a discovered enabled endpoint.
- Inputs match its schema and the start gate is satisfied.
- Returned job identifier is retained and monitored.
- Native job state and task evidence are reported without claiming external system health.
