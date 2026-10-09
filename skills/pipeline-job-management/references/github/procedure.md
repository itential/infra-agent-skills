# GitHub Actions run procedures

GitHub REST procedures for dispatching an existing workflow and reading its execution state.

## Common Sequences

- Inspect execution: **List runs → Read run**.
- Start execution: **Dispatch workflow → Read run**.

### List runs

The run listing applies the requested repository, branch, event, status, commit, or creation-time filters. Success returns the run collection and its count. Pagination follows response links. Filtered searches can return at most 1,000 matching results; that limit is reported rather than represented as a complete repository history. Read access requires the documented Actions read permission for private resources.

### Read run

The run detail operation uses the returned run identifier. Success returns that run's workflow identity, branch/commit, status, conclusion, and URLs. A queued or in-progress run has not completed. A terminal run is reported with its actual conclusion; completion alone does not mean success.

### Dispatch workflow

The configured workflow must support manual workflow dispatch. The request selects a workflow identifier or file name, branch/tag reference, and only inputs declared by that workflow, with at most 25 input properties. Omitted inputs use workflow defaults. Immediately before triggering a workflow that can affect live infrastructure, **stop and confirm with the operator before proceeding**. The current published API returns a 200 result containing a workflow run identifier and URLs. A detail read uses that identifier to observe execution. The accepted dispatch does not establish successful jobs. If the outcome is uncertain, the run list/detail operations resolve matching executions before another dispatch.

### Handle request failures

The operation pages specify the successful responses but do not provide an exhaustive per-operation failure catalogue. Authentication or permission rejection stops the sequence pending correction. Rate-limit responses follow their returned retry guidance. An unrecognized response or server failure is reported with its actual status; it is not relabeled as a failed workflow execution. No fixed polling interval or retry count is established by these operation pages.

## Patterns

Workflow identity and run identity are different. A workflow dispatch can produce production side effects defined in the repository. The returned branch/commit and run identifier tie observations to the intended request.

## Known limitations

This binding targets the currently documented REST API version. Older API dispatch behavior that returns no run body is not silently treated as the current contract. Workflow authoring, deployment approvals, run cancellation/retry, artifacts, and job logs are outside this GitHub procedure.

## Tools

| Operation | Description | Category |
|---|---|---|
| List runs | Find workflow executions | Read |
| Read run | Retrieve one execution's state | Read |
| Dispatch workflow | Start a configured workflow | Write |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Workflow, reference, and submitted inputs match the approved request.
- The dispatch returned a run identifier, and detail read identifies the same run.
- Status and conclusion are reported distinctly; pagination limits remain visible.
