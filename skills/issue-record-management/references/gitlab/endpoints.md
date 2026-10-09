# GitLab issue bindings

Official sources: [Issues](https://docs.gitlab.com/api/issues/), [Notes](https://docs.gitlab.com/api/notes/), [REST API](https://docs.gitlab.com/api/rest/), API v4, retrieved 2026-10-09.

Base: `https://<gitlab-host>/api/v4`. An authenticated client supplies the deployment's supported authentication, such as `PRIVATE-TOKEN: <token>`. Project `{id}` is numeric or the URL-encoded complete project path. `{issue_iid}` is project-local.

| Operation | Literal binding | Inputs | Result |
|---|---|---|---|
| List issues | `GET /projects/{id}/issues` | `state=opened\|closed\|all`, `scope=all`, `labels` comma-separated, `assignee_id` OR `assignee_username`; ISO date filters, `page`, `per_page` | Array of issues and pagination headers |
| Read issue | `GET /projects/{id}/issues/{issue_iid}` | Project and IID | Issue object |
| Create issue | `POST /projects/{id}/issues` | Required `title`; optional `description` (maximum 1,048,576 characters), `labels`, `assignee_ids`, `milestone_id`, `confidential` | Created issue with `iid`, `id`, `state`, `web_url` |
| Update issue | `PUT /projects/{id}/issues/{issue_iid}` | At least one change: `title`, `description`, `state_event=close\|reopen`, `labels`, `add_labels`, `remove_labels`, `assignee_ids` | Updated issue object |
| List notes | `GET /projects/{id}/issues/{issue_iid}/notes` | `activity_filter=all_notes\|only_comments\|only_activity`, `order_by`, `sort`, pagination | Notes array, including `id`, `body`, `system` |
| Add note | `POST /projects/{id}/issues/{issue_iid}/notes` | Required `body` (maximum 1,000,000 characters); optional `internal` | Created note |

REST failure meanings documented by GitLab include 400 invalid request, 401 unauthenticated, 403 forbidden, 404 missing/inaccessible resource, 409 conflict, 422 unprocessable input, 429 rate limit, and server failures. Error payloads may expose either `message` or `error`; preserve the platform's text without publishing credentials. Offset pagination follows `Link` headers and the returned page metadata; keyset pagination is not assumed for every operation.
