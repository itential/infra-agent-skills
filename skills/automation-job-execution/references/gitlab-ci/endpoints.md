# Endpoints — GitLab CI Pipeline Run

Literal wiring layer for `procedure.md`.

Source: GitLab Docs, REST API "Pipelines" and "Jobs" (API v4); retrieved 2026-10-26.
Base: `https://<gitlab-host>/api/v4`. `{id}` is the numeric project id or the URL-encoded full path.

## Authentication

Header `PRIVATE-TOKEN: <token>`. Inside a running CI job the job token is used instead. Required
token scopes: Not documented.

## Operations

| Operation | Binding | Inputs | Success |
|---|---|---|---|
| Create pipeline | `POST /projects/{id}/pipeline` | `ref` (required); `variables` array of `key`, `value`, optional `variable_type` (`env_var` default, or `file`); `inputs` hash | Pipeline object (`id`, `iid`, `sha`, `ref`, `status`, `web_url`, ...) |
| Read pipeline | `GET /projects/{id}/pipelines/{pipeline_id}` | pipeline id | Pipeline object with `status` |
| List pipeline jobs | `GET /projects/{id}/pipelines/{pipeline_id}/jobs` | optional `scope`, `include_retried` (default false); `page`, `per_page` | Job array, id descending |
| Read job log | `GET /projects/{id}/jobs/{job_id}/trace` | job id | 200 log text; 404 job missing or no log |
| Cancel pipeline | `POST /projects/{id}/pipelines/{pipeline_id}/cancel` | pipeline id | 200 regardless of pipeline state; 429 with `Retry-After` when rate limited |
| Cancel job | `POST /projects/{id}/jobs/{job_id}/cancel` | job id; optional `force` (boolean, for a job already in `canceling`) | Job object; 429 when rate limited |

Pipeline and job status values: `created`, `waiting_for_resource`, `preparing`, `waiting_for_callback`,
`pending`, `running`, `success`, `failed`, `canceling`, `canceled`, `skipped`, `manual`, `scheduled`.
Which of these are terminal is the classification in `procedure.md` step 5 (the docs list the values
without marking them terminal; that split is an assumption).

Unverified: token scopes; whether `inputs` and `variables` may
be combined. General REST statuses apply: 400, 401, 403, 404, 422, 429.
