# Endpoints — Bitbucket Cloud Pull Request Management

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST
client/adapter is assumed available.

Sources: Atlassian support documentation for Bitbucket Cloud under
`support.atlassian.com/bitbucket-cloud/docs/`, cross-checked against the Bitbucket Cloud API's own
OpenAPI schema for exact field/enum names, retrieved 2026-09-29. See `procedure.md`'s sources note for
why the schema is used for field-level detail here.

## List pull requests

```
GET /2.0/repositories/{workspace}/{repo_slug}/pullrequests
```

**Success:** `200` with a paginated array of pull request objects.

## Get a pull request

```
GET /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}
```

**Success:** `200` with the PR object, including `state` (`OPEN`, `MERGED`, `DECLINED`,
`SUPERSEDED`), `source`, `destination`.

## Create a pull request

```
POST /2.0/repositories/{workspace}/{repo_slug}/pullrequests
```

Body fields (per the `pullrequest` schema):
- `title` — recommended in practice even where the schema doesn't mark it strictly required, since an
  untitled PR is not meaningfully usable.
- `source` — object identifying the source branch (and `source.repository` for a fork).
- `destination` (optional) — object identifying the target branch; defaults to the repository's main
  branch if omitted.
- `description` (optional).
- `reviewers` (optional) — array of account objects.
- `close_source_branch` (optional, boolean) — sets the default used later at merge time if the merge
  call itself omits `close_source_branch`.

**Success:** `201` with the created PR object.

## Update a pull request

```
PUT /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}
```

Send only the fields being changed (`title`, `description`, `destination`, `reviewers`).

**Success:** `200` with the updated PR object.

## Approve / remove approval

```
POST   /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/approve
DELETE /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/approve
```

Toggles the authenticated user's approval on/off. No request body.

**Success:** `200` (approve) / `204` (remove).

## Request changes

```
POST   /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/request-changes
DELETE /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/request-changes
```

Same toggle shape as approve, for the request-changes state instead.

## Merge a pull request

```
POST /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/merge
```

Body fields (per the `pullrequest_merge_parameters` schema):
- `type` (required per schema — literal descriptor of the object; a client library typically fills
  this in automatically rather than a caller supplying a business value).
- `message` (optional) — resulting commit message, capped at 128 KiB per the schema description.
- `close_source_branch` (optional, boolean) — falls back to the value set at PR creation if omitted,
  defaulting to `false` if never set.
- `merge_strategy` (optional) — enum `merge_commit` (default), `squash`, `fast_forward` per the
  schema. The support docs additionally describe rebase-based UI strategies (rebase-merge,
  rebase-fast-forward, squash-fast-forward-only) not present in this schema's enum — verify against
  the live API for the target site before relying on a rebase value here.

**Success:** `200` with the merge result, or an async task reference for large PRs (see the
task-status sub-resource below). **Failure:** merge-checklist not satisfied, conflicts present —
exact error shape not fully enumerated in the sources retrieved; surface the response body verbatim.

## Merge async task status

```
GET /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/merge/task-status/{task_id}
```

Poll for completion of an asynchronously-processed merge.

## Decline a pull request

```
POST /2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/decline
```

No request body documented beyond the standard pull request reference. Per the support docs, this is
permanent — the resulting `DECLINED` state cannot be reverted to `OPEN` on the same PR.

**Success:** `200` with the PR object now showing `state: DECLINED`.
