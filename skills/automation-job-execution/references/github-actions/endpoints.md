# Endpoints — GitHub Actions Workflow Dispatch

Sources: GitHub Docs REST API "Workflows" and "Workflow runs"; retrieved 2026-10-26.

Base: `https://api.github.com`. Headers: `Authorization: Bearer <token>`, `Accept: application/vnd.github+json`. Send the `X-GitHub-Api-Version` header (the REST docs show `2026-03-10`).

| Operation | Binding | Inputs | Success |
|---|---|---|---|
| Dispatch workflow | `POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches` | `ref` (required branch or tag); `inputs` object, at most 25 properties; `workflow_id` is the ID or file name | 200 with `workflow_run_id`, `run_url`, `html_url` |
| List runs | `GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs` | Filters `event`, `branch`, `created`, `status`, `head_sha` | 200 |
| Read run | `GET /repos/{owner}/{repo}/actions/runs/{run_id}` | run ID | 200 with `status`, `conclusion` |
| Read logs | `GET /repos/{owner}/{repo}/actions/runs/{run_id}/logs` | run ID | 302, `Location` header holds the link (expires after 1 minute) |
| Cancel run | `POST /repos/{owner}/{repo}/actions/runs/{run_id}/cancel` | run ID | 202; 409 conflict |
| Force cancel run | `POST /repos/{owner}/{repo}/actions/runs/{run_id}/force-cancel` | run ID | 202; 409 conflict |

Permissions: classic tokens need `repo` for private repositories and for dispatch/cancel. Fine-grained permission names: assumption (Actions read for reads, Actions write for dispatch and cancel).

Status values: `queued`, `requested`, `waiting`, `pending`, `in_progress`, `completed`. Conclusion values: `success`, `failure`, `neutral`, `cancelled`, `skipped`, `timed_out`, `action_required`.

Not documented: exact error bodies for 401/403/404/422 on dispatch, rate limits for these calls.
