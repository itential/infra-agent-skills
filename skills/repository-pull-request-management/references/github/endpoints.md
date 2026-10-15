# Endpoints — GitHub Pull Request Management

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST
client/adapter is assumed available.

Source: GitHub REST API reference, "Pulls" and "Reviews" pages under `docs.github.com/en/rest/pulls`,
retrieved 2026-09-29.

## List pull requests

```
GET /repos/{owner}/{repo}/pulls
```

Query params: `state` (`open`/`closed`/`all`, default `open`), `head` (`user:ref-name`), `base`,
`sort` (`created`/`updated`/`popularity`/`long-running`), `per_page`, `page`.

**Success:** `200` with an array of pull request objects.

## Get a pull request

```
GET /repos/{owner}/{repo}/pulls/{pull_number}
```

**Success:** `200` with the full PR object, including `mergeable` (`true`/`false`/`null` — `null`
means GitHub hasn't finished computing it), `mergeable_state`, `merged`, `merge_commit_sha`.
**Failure:** `404` not found, `422` validation failed, `304` not modified (conditional request).

## Create a pull request

```
POST /repos/{owner}/{repo}/pulls
```

Body fields:
- `head` (required) — source branch, `username:branch` for cross-repo.
- `base` (required) — target branch.
- `title` or `issue` (one required) — `issue` converts an existing issue number into a PR.
- `body` (optional) — description.
- `draft` (optional, boolean).
- `maintainer_can_modify` (optional, boolean).
- `head_repo` (optional) — required for cross-repo PRs within the same organization.

**Success:** `201` with the created PR object. **Failure:** `403` forbidden (needs write access to
head or source branch on public repos), `422` validation failed (e.g. no diff, PR already exists for
that head/base pair — exact string not enumerated in the source; surface it verbatim).

## Update a pull request

```
PATCH /repos/{owner}/{repo}/pulls/{pull_number}
```

Body fields (send only what's changing): `title`, `body`, `state` (`open` or `closed`), `base`,
`maintainer_can_modify`.

**Success:** `200` with the updated PR object. **Failure:** `403`, `422`.

## Create a review

```
POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
```

Body fields:
- `event` — `APPROVE`, `REQUEST_CHANGES`, or `COMMENT`; omitted creates a pending review requiring a
  later separate submit call.
- `body` — required when `event` is `REQUEST_CHANGES` or `COMMENT`.
- `commit_id` (optional) — SHA the review targets; defaults to the PR's current head commit.
- `comments` (optional) — array of inline comments, each with `path`, `position`, `body`.

**Success:** `200`/`201` with the created review object.

## List reviews

```
GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews
```

**Success:** `200` with an array of review objects, chronological, paginated (`per_page` up to 100).

## Merge a pull request

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge
```

Body fields:
- `merge_method` (required) — `merge`, `squash`, or `rebase`.
- `commit_title` / `commit_message` (optional).
- `sha` (optional) — merge only proceeds if the PR's current head matches this value; mismatch
  returns a conflict.

**Success:** `200` with `{"merged": true, "message": "...", "sha": "..."}`. **Failure:** `merged:
false` with an explanatory `message` (e.g. required checks not satisfied, conflicts present) inside a
`200`/`405` response depending on cause per the source; also `403`, `404`, `409` (sha mismatch), `422`
— surface the response's own `message` rather than a fabricated string.

## Check if a pull request has been merged

```
GET /repos/{owner}/{repo}/pulls/{pull_number}/merge
```

No response body. **Success:** `204` = merged. **Not merged:** `404`.

## List commits / files on a pull request

```
GET /repos/{owner}/{repo}/pulls/{pull_number}/commits
GET /repos/{owner}/{repo}/pulls/{pull_number}/files
```

Supporting reads only — not create/update/merge actions. Commits capped at 250 per the source; files
capped at 3000 total, 30 per page.

## Authentication

`Authorization: Bearer <token>` plus `Accept: application/vnd.github+json` and an
`X-GitHub-Api-Version` header pinned to the API version the calling tool was built against.
