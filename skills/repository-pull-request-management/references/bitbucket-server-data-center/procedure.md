# Bitbucket Server & Data Center — Pull Request Management Procedure

Creates, reads, updates, reviews, merges, declines, or reopens a pull request against a Bitbucket
Server or Data Center project repository through the Pull Requests REST resource.

Scope: open/list/get/edit a pull request, set a participant's review status, merge a pull request,
decline one without merging, or reopen a previously declined one. Does not cover creating the
project/repository or the branches involved, configuring default reviewers, or branch-permission
configuration. Assumes an authenticated REST client against the Bitbucket Server/Data Center REST API
(a personal access token or session carrying at minimum write access to pull requests on the target
repository) is already available.

Source: Atlassian's Bitbucket Server REST API reference for the pull-requests resource (documented
at the stable 1.0 REST path (see `endpoints.md`); content retrieved from `docs.atlassian.com`'s generated REST
resource documentation for this resource, retrieved 2026-09-29 — this is the same resource shape
Atlassian's newer per-version `developer.atlassian.com/server/bitbucket/rest/` pages describe; the
version-numbered documentation page retrieved did not correspond to the very latest release line, but
the pull-requests resource and its required-`version` concurrency model have been
stable across the Server/Data Center REST API's documented history — verify against the target
instance's own REST path if it exposes interactive API documentation, since an installation
could be running an older release with a narrower field set).

## Operational procedure

1. **Confirm the project, repository, and both branches are reachable** — resolve `projectKey` and
   `repositorySlug`, and confirm the source (`fromRef`) and target (`toRef`) branches both exist. If
   either can't be found, stop and report FAILED with "branch not found."
2. **Create the pull request** — submit `title`, `fromRef` and `toRef` (each a ref object naming the
   branch, its repository slug, and project key — supporting a cross-repository pull request when the
   `fromRef` repository differs from the destination), plus optional `description` and a `reviewers`
   array of user references. If validation fails (no divergence between branches, an open PR already
   exists for that ref pair), report REJECTED_VALIDATION_FAILED with the returned error detail.
3. **To list or inspect existing requests** — list with pagination, or fetch one by its numeric ID
   within the repository. Every fetched pull request carries a `version` integer that increments on
   every server-side change — capture the current value before any subsequent update/merge/decline/
   reopen call, since this platform requires it as a concurrency guard (see step 4 and Patterns).
4. **To update an open request** — submit the changed fields (`title`, `description`, `reviewers`,
   `toRef` to retarget) together with the pull request's current `version`; a stale `version` (one
   that doesn't match the server's current value, because something else changed the PR since it was
   last read) is rejected as a conflict rather than silently overwritten.
5. **To record a reviewer's decision** — set a participant's status by addressing that user's slug on
   the pull request's participants resource, with a status among the values this platform documents
   (approved, unapproved, needs-work). This is per-reviewer state, not an accumulating list of review
   submissions the way GitHub models reviews.
6. **Before merging: stop and confirm with the operator.** Merging moves the source branch's commits
   into the target branch's history — a production-affecting, hard-to-reverse action. Confirm the
   target branch and current `version`, and that any merge checks the target instance enforces
   (minimum approvals, no outstanding "needs work" status, successful builds if a build-status
   integration is configured) are satisfied, before submitting.
7. **Test mergeability first if the calling tool supports it** — a read-only mergeability check
   against the pull request's merge sub-resource reports whether it can currently merge, whether
   conflicts are present, and any documented vetoes (conditions from configured merge checks blocking
   the merge) — use this to avoid submitting a merge call already known to fail.
8. **Merge the request** — submit the merge call carrying the pull request's current `version`
   (required — this is the platform's concurrency guard, not optional metadata) and, if the target
   instance's configured merge strategy options expose a choice, the selected strategy. A stale
   `version` (the PR changed since it was last read — e.g. a new commit landed, or another reviewer's
   status changed) is rejected with a conflict; re-fetch the current `version` and confirm nothing
   materially changed before retrying, rather than blindly resubmitting the same stale value.
9. **To decline instead of merging** — call the decline endpoint with the pull request's current
   `version`. This platform, unlike Bitbucket Cloud, documents a separate reopen action: a declined
   pull request can be moved back to `OPEN` via the reopen endpoint (again requiring the current
   `version`), rather than declining being permanent.
10. **Confirm the outcome** — after a merge call, treat a response describing the resulting `MERGED`
    state as success; after decline/reopen, re-fetch and confirm the pull request's `state` field
    reflects `DECLINED` or `OPEN` respectively.
11. **Handle undocumented failures verbatim** — for any error not already covered by a specific step
    above, report FAILED with the underlying response's actual error detail rather than guessing at a
    cause.

## Patterns

- **Every mutating call on an existing pull request requires its current `version`.** This is the one
  platform among the four covered by this skill where that's documented as an explicit, required
  field on update/merge/decline/reopen — treat a missing or stale `version` as the most likely cause
  of an otherwise-unexplained conflict response, and always re-fetch to get the current value rather
  than reusing one captured earlier in a long-running process.
- **Decline is not permanent here**, unlike Bitbucket Cloud's documented one-way decline — reopening a
  previously declined pull request is a first-class, separately-documented action on this platform.
- **Reviewer state is per-participant, not an event log.** Setting a participant's status
  (approved/unapproved/needs-work) overwrites that participant's current standing; it does not append
  a new review object the way GitHub's review API does.

## Known limitations

- Does not cover project/repository or branch creation, default-reviewer configuration, or
  branch-permission/merge-check configuration — this procedure only operates within whatever checks
  are already configured on the target repository.
- The exact set of merge strategy options exposed via the API (as opposed to the UI) was not
  enumerated in the source retrieved for this procedure — if the calling tool needs to select a
  non-default merge strategy, verify the accepted values against the target instance before assuming
  parity with another platform's strategy names.
- The retrieved documentation corresponds to an older but structurally stable release line of the
  Server REST API reference generator; a specific target instance's actual installed version may
  expose additional fields or a differently-numbered path (a `latest` alias for the version segment is documented elsewhere
  and some instances also expose it; see `endpoints.md`) — confirm the exact base path against the target instance.
- The source does not document a fixed catalog of error strings for every validation failure beyond
  the general conflict/malformed-request status codes; step 11 exists because of this.

## Tools

| Operation | Description | Category |
|---|---|---|
| List pull requests | List/filter PRs in a repository | Pull Requests |
| Get a pull request | Fetch one PR by ID, including current `version` | Pull Requests |
| Create a pull request | Open a new PR from `fromRef` into `toRef` | Pull Requests |
| Update a pull request | Change title/description/reviewers/`toRef`, with `version` | Pull Requests |
| Set participant status | Record a reviewer's approved/unapproved/needs-work state | Pull Requests |
| Test mergeability | Read-only check for conflicts/vetoes before merging | Pull Requests |
| Merge a pull request | Merge, carrying the current `version` | Pull Requests |
| Decline a pull request | Decline without merging, carrying the current `version` | Pull Requests |
| Reopen a pull request | Move a declined PR back to open, carrying the current `version` | Pull Requests |

## Verification checklist

- [ ] Source and target branches confirmed to exist before create
- [ ] Current `version` re-fetched immediately before every update/merge/decline/reopen call, not
      reused from an earlier read
- [ ] For merge: operator confirmation obtained before submission (step 6); mergeability tested first
      where the calling tool supports it (step 7)
- [ ] Merge outcome confirmed via the pull request's `state` field, not assumed from a 2xx status alone
- [ ] Decline vs. reopen distinguished correctly in the reported outcome — decline is not treated as
      permanent on this platform, unlike Bitbucket Cloud
