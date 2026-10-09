# GitLab pipeline and job procedures

GitLab REST procedures for pipeline execution and job-log retrieval.

## Common Sequences

- Inspect execution: **List pipelines → Read pipeline → List jobs → Read job trace**.
- Start execution: **Create pipeline → Read pipeline → List jobs**.
- Control execution: **Read pipeline → Retry pipeline or Cancel pipeline → Read pipeline → List jobs**.

### List pipelines

The listing applies the requested project, reference, status, commit, or source filters and follows response pagination. Success returns pipeline identifiers and state. Child pipelines are omitted by default; querying the parent-pipeline source includes them on supporting versions. A branch/tag scope filter yields the latest matching pipeline per reference rather than an unrestricted history.

### Read pipeline

The detail operation resolves one project pipeline identifier. Success returns its identifier, reference, commit, status, and URL. The recorded status is the pipeline outcome; a successful API call is not a successful pipeline.

### Create pipeline

The creation operation selects a branch or tag reference and optional declared inputs or pipeline variables. Immediately before starting a pipeline that can change live infrastructure, **stop and confirm with the operator before proceeding**. Success returns the new pipeline identifier and state. Inputs are generally available from GitLab 18.1; unsupported target versions must not receive them. A timeout leaves creation uncertain, requiring a matching pipeline read/list before another creation.

### Retry pipeline

The retry operation reruns failed or canceled jobs. Immediately before executing these jobs again, **stop and confirm with the operator before proceeding**. Success returns the pipeline object; when no eligible jobs exist the operation has no effect. The job list verifies whether eligible executions actually restarted. A 429 uses the returned retry guidance. Concurrent-retry conflict behavior is version/feature-dependent in the published documentation; a conflict requires re-reading current state rather than forcing another retry.

### Cancel pipeline

Immediately before canceling the pipeline's jobs, **stop and confirm with the operator before proceeding**. The cancellation operation returns a 200 result regardless of the pipeline's prior state, so acceptance alone does not prove that running work was interrupted. Detail and job reads establish the resulting state. A 429 requires honoring the returned retry delay.

### List jobs

The pipeline job list returns job identifiers and statuses in descending identifier order. Pagination is required beyond the default page. Retried jobs are excluded unless the include-retried option is requested. Success is a job array; the selected job identifier, not the pipeline identifier, is used for its trace.

### Read job trace

The trace operation returns the job's log bytes on success. A 404 can mean a missing job or an unavailable log, so it is not treated as an empty successful log. Log content can contain application-provided sensitive values; the output remains constrained to the requested authorized artifact.

### Handle other request failures

GitLab's general REST meanings apply: invalid requests require correction; authentication/permission failures require access repair; missing resources require identity/visibility review; validation or conflict responses require current-state review; rate limits use response guidance. Server failures and uncertain writes do not prove that pipeline side effects were absent. Exact polling intervals and retry counts are not established by these source pages.

## Patterns

A retried pipeline is not a new arbitrary execution of every job. A cancellation response can be successful even when there was nothing to cancel. Readback preserves both pipeline and individual job states.

## Known limitations

No CI configuration editing, secrets management, manual-job play, pipeline deletion, artifacts, or merge-request pipeline creation. Child-pipeline listing support begins in GitLab 17.0. Deployment effects are defined by the existing pipeline, not this procedure.

## Tools

| Operation | Description | Category |
|---|---|---|
| List pipelines | Find project pipeline executions | Read |
| Read pipeline | Retrieve pipeline state | Read |
| Create pipeline | Start a branch/tag pipeline | Write |
| Retry pipeline | Rerun failed/canceled jobs | Write |
| Cancel pipeline | Cancel pipeline jobs | Write |
| List jobs | Retrieve pipeline jobs and status | Read |
| Read job trace | Retrieve a selected job's log | Read |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Project, pipeline identifier, reference, and commit match the request.
- Creation/retry/cancel response is distinguished from eventual execution outcome.
- Job pagination and retried-job inclusion are explicit.
- Trace bytes or the native missing-log error are reported accurately.
