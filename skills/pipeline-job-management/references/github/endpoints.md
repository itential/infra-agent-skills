# GitHub Actions bindings

Official sources: [Workflow runs](https://docs.github.com/en/rest/actions/workflow-runs), [Workflows](https://docs.github.com/en/rest/actions/workflows), REST API docs, retrieved 2026-10-09.

Base `https://api.github.com`; authenticated client with `Authorization: Bearer <token>`, `Accept: application/vnd.github+json`, `X-GitHub-Api-Version: 2026-03-10`. Fine-grained permission: Actions read for reads, Actions write for dispatch. Classic token dispatch requires `repo` scope.

| Operation | Literal binding | Inputs | Success |
|---|---|---|---|
| List runs | `GET /repos/{owner}/{repo}/actions/runs` | Optional `branch`, `event`, `status`, `head_sha`, `created`; `per_page` at most 100, `page` | 200 `total_count`, `workflow_runs`; pagination via `Link` |
| Read run | `GET /repos/{owner}/{repo}/actions/runs/{run_id}` | Run ID | 200 run with `id`, `status`, `conclusion`, `head_branch`, `head_sha`, `html_url` |
| Dispatch workflow | `POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches` | Required `ref`; optional `inputs` object, at most 25 properties | 200 `workflow_run_id`, `run_url`, `html_url` |

The workflow file declares `workflow_dispatch` and allowed inputs. The current documented dispatch response is materially different from historical 204-only examples; the client must match the selected API version. The cited operation pages do not enumerate every failure status; actual error responses are retained rather than inferred from successful runs.
