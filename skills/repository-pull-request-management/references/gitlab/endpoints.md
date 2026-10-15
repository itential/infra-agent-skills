# Endpoints — GitLab Merge Request Management

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST
client/adapter is assumed available.

Source: GitLab REST API reference, "Merge requests" and "Merge request approvals" pages under
`docs.gitlab.com/ee/api/`, retrieved 2026-09-29.

## List merge requests

```
GET /merge_requests                         # all accessible to the caller
GET /groups/:id/merge_requests               # group-scoped
GET /projects/:id/merge_requests             # project-scoped
```

Query params include `state` (`opened`/`closed`/`locked`/`merged`/`all`), `labels`, `author_id`,
`assignee_id`, `reviewer_id`, `milestone`, `search`, `draft`.

**Success:** `200` with an array of MR objects.

## Get a merge request

```
GET /projects/:id/merge_requests/:merge_request_iid
```

Optional params: `include_diverged_commits_count`, `include_rebase_in_progress`, `render_html`.

**Success:** `200` with the MR object, including `detailed_merge_status`, `has_conflicts`, `draft`,
`merge_commit_sha` (populated only once merged).

## Create a merge request

```
POST /projects/:id/merge_requests
```

Body fields:
- `source_branch` (required).
- `target_branch` (required).
- `title` (required).
- `description`, `assignee_ids`, `reviewer_ids`, `labels`, `milestone_id`, squash-preference fields
  (optional).

**Success:** `201` with the created MR object. **Failure:** `409` conflict (e.g. an open MR already
exists for the branch pair), `422` unprocessable entity.

## Update a merge request

```
PUT /projects/:id/merge_requests/:merge_request_iid
```

Body fields (send only what's changing): `title`, `description`, `target_branch`, `assignee_ids`,
`reviewer_ids`, `labels`, `milestone_id`, `state_event` (`close` or `reopen`).

**Success:** `200` with the updated MR object.

## Approve a merge request

```
POST /projects/:id/merge_requests/:merge_request_iid/approve
```

Body fields: `sha` (optional — mismatch against the MR's current head returns `409`),
`approval_password` (optional, only if project re-authentication for approvals is enabled).

**Success:** `201` with the updated approval state.

## Unapprove a merge request

```
POST /projects/:id/merge_requests/:merge_request_iid/unapprove
```

Removes the authenticated user's own approval.

**Success:** `201`.

## Get approval state

```
GET /projects/:id/merge_requests/:merge_request_iid/approvals
```

**Success:** `200` with `approved_by` (array of approvers) and overall approval status.

## Merge a merge request

```
PUT /projects/:id/merge_requests/:merge_request_iid/merge
```

Body fields (all optional): `merge_when_pipeline_succeeds` (boolean), `squash` (boolean),
`should_remove_source_branch` (boolean), `merge_commit_message`, `squash_commit_message`, `sha`
(guard against merging a stale diff).

**Success:** `200` with the merged (or pending-on-pipeline) MR object. **Failure:** `405` not
mergeable (draft, conflicts, failed pipeline, unmet approval rules — exact reason in the response
body), `401`/`403` unauthorized/forbidden, `409` conflict (`sha` mismatch or already merged).

## Status codes referenced across this resource

`200` success, `201` created, `401` unauthorized, `403` forbidden, `404` not found, `408` request
timeout, `409` conflict, `422` unprocessable entity.
