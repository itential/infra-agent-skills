# HCP Terraform API v2 bindings

Sources: [workspaces](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces), [runs](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run), [variables](https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables), [API overview](https://developer.hashicorp.com/terraform/cloud-docs/api-docs), retrieved 2026-10-09.

Base `https://app.terraform.io/api/v2`, or the configured Terraform Enterprise API v2 address. Headers: `Authorization: Bearer <token>` and `Content-Type: application/vnd.api+json`.

| Operation | Method/path | Inputs/result |
|---|---|---|
| List workspace | `GET /organizations/{organization}/workspaces` | `page[number]`, `page[size]`, optional `search[name]`; JSON:API `data`, links and pagination metadata |
| Read workspace | `GET /workspaces/{workspace_id}` | Workspace object |
| Create workspace | `POST /organizations/{organization}/workspaces` | `data.type: workspaces`; required `data.attributes.name`; optional approved `description`, `execution-mode`, `terraform-version`, `auto-apply`, other current schema settings |
| Update workspace | `PATCH /workspaces/{workspace_id}` | `data.type: workspaces`, requested `data.attributes`; fields omitted remain unchanged |
| List variables | `GET /workspaces/{workspace_id}/vars` | Variable objects; `sensitive` values are not subsequently readable |
| Safe delete | `POST /workspaces/{workspace_id}/actions/safe-delete` | 204 deleted; 409 manages resources; 404 absent or unauthorized |
| Create speculative run | `POST /runs` | `data.type: runs`, `data.attributes.plan-only: true`, `data.attributes.auto-apply: false`, `data.relationships.workspace.data: {type: workspaces, id: <workspace_id>}`; optional configuration-version relationship |
| Read run | `GET /runs/{run_id}` | `data.attributes.status` and run details |
| List runs | `GET /workspaces/{workspace_id}/runs` | `filter[operation]=plan_only` includes speculative plans; standard pagination |
| Cancel run | `POST /runs/{run_id}/actions/cancel` | Optional `comment`; 202 queued, 409 not planning/applying, 404 absent/unauthorized |

Run creation: 201 returns the run object; 404 workspace/organization absent or unauthorized; 422 malformed payload. Common JSON:API errors carry `errors`; 401/403 require access correction, 404 can conceal access, 422 requires corrected input, 429 requires reducing request pressure, and 5xx is server failure. Unknown mutation completion requires read-back. Exact edition-specific attributes and available versions must be verified against the deployed platform's current schema.
