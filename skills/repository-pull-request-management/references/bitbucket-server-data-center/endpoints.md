# Endpoints — Bitbucket Server & Data Center Pull Request Management

Literal wiring layer. `procedure.md` steps reference these by name; bind them to whatever REST
client/adapter is assumed available.

Source: Atlassian's Bitbucket Server REST API reference for the pull-requests resource, retrieved via
`docs.atlassian.com`'s generated REST resource documentation, retrieved 2026-09-29. See
`procedure.md`'s sources note on version-line coverage — confirm the target instance's exact base path
before relying on this verbatim. Some instances also expose a `latest` alias in place of `1.0` in
the version segment of the paths below (`/rest/api/latest/...`); this is documented elsewhere, not
confirmed for every release.

## List / create pull requests

```
GET  /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests
POST /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests
```

**Create body fields:**
- `title` (required).
- `fromRef` (required) — object: `{ id: "refs/heads/{branch}", repository: { slug, project: { key } } }`.
- `toRef` (required) — same shape, for the target branch.
- `description` (optional).
- `reviewers` (optional) — array of `{ user: { name } }` objects.

**Success:** `201` with the created pull request object, including its initial `version` (typically
`0`). **Failure:** `400` malformed request, `409` conflict (e.g. no divergence between refs, or an
open PR already exists for that ref pair).

## Get a pull request

```
GET /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}
```

**Success:** `200` with the pull request object, including `state` (`OPEN`, `MERGED`, `DECLINED`) and
the current `version` integer — capture this before any mutating call.

## Update a pull request

```
PUT /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}
```

Body must include the pull request's current `version` alongside whichever of `title`, `description`,
`reviewers`, `toRef` are being changed.

**Success:** `200` with the updated object (new `version`). **Failure:** `409` conflict if the
supplied `version` doesn't match the server's current value.

## Set a participant's review status

```
PUT /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/participants/{userSlug}
```

Body fields: `status` (`APPROVED`, `UNAPPROVED`, `NEEDS_WORK`); an `approved` boolean is also accepted
as an older/simpler form of the same toggle.

**Success:** `200` with the updated participant record.

## Test mergeability

```
GET /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/merge
```

Read-only check. **Success:** `200` with `canMerge` (boolean), `conflicted` (boolean), and `vetoes`
(array describing any configured merge check currently blocking the merge).

## Merge a pull request

```
POST /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/merge
```

Requires the pull request's current `version` (as a query parameter or body field per the target
instance's exact contract — confirm against that instance).

**Success:** `200` with the merged pull request object (`state: MERGED`). **Failure:** `409` conflict
— either a stale `version` or an unmet merge check (e.g. "merging an out-of-date pull request" is
documented as a named conflict condition).

## Decline a pull request

```
POST /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/decline
```

Requires the pull request's current `version`.

**Success:** `200` with `state: DECLINED`.

## Reopen a pull request

```
POST /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/reopen
```

Requires the pull request's current `version`.

**Success:** `200` with `state: OPEN`.

## Status codes referenced across this resource

`200` success, `201` created, `204` success with no content, `400` malformed request, `409` conflict
(stale `version`, unmet merge check, or out-of-date branch).
