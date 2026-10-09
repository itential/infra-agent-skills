# Nornir scoped task execution

Execute an already defined read-only task over an explicit inventory selection.

## Common Sequences

- Fleet read: **Initialize and select** → **Run task** → **Inspect every outcome**.

### Initialize and select

Nornir loads the supplied inventory/configuration and uses its configured runner. The caller selects the inventory subset and explicit concurrency. The task is an already defined read operation with its own documented transport and output contract. Missing inventory or an empty selection does not establish a successful fleet check.

### Run task

The selected inventory executes the task and returns host-keyed aggregate results. Each host can contain a sequence of task/subtask outcomes. Previously failed hosts are skipped by default on later calls; a fleet request must account for that skipped set. Enabling execution on failed hosts is a deliberate rerun after its failure is understood, not an automatic recovery.

### Inspect every outcome

The aggregate's failure state and failed-host mapping identify errors. Each task result retains output, changed/failed flags and exception. Nested failures can stop later subtasks for that host. Printed output may hide low-severity successful tasks, so it is not a complete result inventory. Every selected host is reconciled as returned, failed or skipped; a missing host is not success. Raising the aggregate error preserves failure rather than flattening it to an empty result.

## Patterns

Failed-host state persists within the Nornir object. Clearing it changes eligibility for subsequent calls; it does not repair the host or validate its previous operation.

## Known limitations

No NetClaw requested=returned invariant, fixed timeout or default ten-worker limit is promised by native Nornir. This reference only runs read tasks; a task function remains arbitrary code and is not sandboxed by Nornir.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Initialize/filter | Resolve inventory subset and configured runner | Local orchestration |
| Run/read results | Execute supplied task and inspect per-host outcomes | Parallel execution |

## Verification checklist

- Selected inventory and concurrency are explicit.
- Each target is accounted for, including skipped failed hosts.
- Nested exceptions remain visible.
- No automatic failed-host reset or replay occurred.

## Sources

- [Nornir initialization](https://nornir.readthedocs.io/en/latest/tutorial/initializing_nornir.html). Retrieved 2026-10-09.
- [Nornir result structure](https://nornir.readthedocs.io/en/latest/tutorial/task_results.html). Retrieved 2026-10-09.
- [Nornir failure and skipped-host handling](https://nornir.readthedocs.io/en/latest/tutorial/failed_tasks.html). Retrieved 2026-10-09.
