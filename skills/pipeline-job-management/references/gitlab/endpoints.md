# GitLab pipeline bindings

Official sources: [Pipelines](https://docs.gitlab.com/api/pipelines/), [Jobs](https://docs.gitlab.com/api/jobs/), [REST API](https://docs.gitlab.com/api/rest/), API v4, retrieved 2026-10-09.

Base `https://<gitlab-host>/api/v4`; existing authenticated client, such as `PRIVATE-TOKEN: <token>`. Project `{id}` is its number or URL-encoded complete path. Pagination uses response links, `page`, and `per_page` where supported.

| Operation | Literal binding | Inputs | Success |
|---|---|---|---|
| List pipelines | `GET /projects/{id}/pipelines` | Optional `ref`, `status`, `sha`, `source`; pagination | Pipeline array |
| Read pipeline | `GET /projects/{id}/pipelines/{pipeline_id}` | Pipeline ID | Pipeline with `id`, `status`, `ref`, `sha`, `web_url` |
| Create pipeline | `POST /projects/{id}/pipeline` | Required `ref`; optional `inputs`, `variables` array of `key`, `value`, optional `variable_type=env_var\|file` | New pipeline object |
| Retry pipeline | `POST /projects/{id}/pipelines/{pipeline_id}/retry` | Pipeline ID | Pipeline object; no effect if no failed/canceled jobs |
| Cancel pipeline | `POST /projects/{id}/pipelines/{pipeline_id}/cancel` | Pipeline ID | 200 even if already not running; readback required |
| List jobs | `GET /projects/{id}/pipelines/{pipeline_id}/jobs` | Optional `include_retried`, `scope`, pagination | Job array; default 20 per page |
| Read job trace | `GET /projects/{id}/jobs/{job_id}/trace` | Job ID | 200 trace bytes; 404 missing job/log |

`source=parent_pipeline` includes child pipelines on GitLab 17.0 and later. Pipeline `inputs` are generally available in 18.1. The published retry documentation describes 409 concurrent-retry handling introduced in 19.5 behind a feature flag disabled by default; this is version-specific, not a baseline assumption. Retry/cancel 429 responses can include `Retry-After`. General REST error meanings are 400 bad request, 401 unauthenticated, 403 forbidden, 404 missing/inaccessible, 409 conflict, 422 validation failure, 429 rate-limited, or server error.
