# Bitbucket Cloud — Pull Request Management Procedure

Creates, reads, updates, approves, merges, or declines a pull request against a Bitbucket Cloud
repository through the Pull Requests REST resource.

Scope: open/list/get/edit a pull request, toggle an approval or record a request-changes action,
merge a pull request, or decline one without merging. Does not cover creating the workspace/repository
or the branches involved, configuring default reviewers or merge checklists, or branch-permission
configuration. Assumes an authenticated REST client against the Bitbucket Cloud API (an API token,
app password, or OAuth token carrying at minimum write access to pull requests on the target
repository) is already available.

Sources: Atlassian support documentation for Bitbucket Cloud ("Create a pull request," "Merge a pull
request," "Decline a pull request" under `support.atlassian.com/bitbucket-cloud/docs/`) for the
conceptual/UI-adjacent behavior, cross-checked against the Bitbucket Cloud API's own OpenAPI schema
(`api-group-pullrequests` resource, `pullrequest` and `pullrequest_merge_parameters` objects) for
exact field names — the interactive `developer.atlassian.com` reference page itself did not render
retrievable text content at retrieval time (2026-09-29), so the field-name-level detail below is
drawn from that schema rather than from prose on that page; treat any field not corroborated by the
support docs as schema-only and verify against the target site before relying on it in production.

## Operational procedure

1. **Confirm the repository and both branches are reachable** — resolve `workspace`/`repo_slug`, and
   confirm the source branch and destination branch both exist (a fork's repository can also serve as
   the source, per the API's own request-URL convention: the URL you POST to is always the
   destination repository). If either can't be found, stop and report FAILED with "branch not found."
2. **Create the pull request** — submit at minimum a `title` and a `source` branch reference (and
   `source.repository` if pulling from a fork); `destination` defaults to the repository's main branch
   if omitted, but should be set explicitly whenever the caller has a specific target in mind. Add
   `description` and `reviewers` as needed — descriptions can reference `{{commit_messages}}` as a
   literal placeholder Bitbucket Cloud expands into the source branch's commit list. If Bitbucket
   returns a validation error (no diff between branches, PR already open for that pair), report
   REJECTED_VALIDATION_FAILED with the returned error detail.
3. **To list or inspect existing requests** — list with pagination, or fetch one by its numeric
   `pull_request_id`. The response's `state` field is the authoritative status (`OPEN`, `MERGED`,
   `DECLINED`, `SUPERSEDED`).
4. **To update an open request** — submit only the fields being changed (title, description,
   destination, reviewers) via the update call; declining/merging are separate dedicated calls, not
   state values sent through this one.
5. **To record an approval or a request-changes decision** — call the dedicated approve endpoint to
   toggle the authenticated user's approval on, or its delete form to remove it; call the dedicated
   request-changes endpoint similarly. Unlike GitHub's review objects, Bitbucket Cloud's approval is a
   simple per-user toggle, not an accumulating history of distinct review submissions — check the
   target repository's configured merge checklist (minimum approvals, no unresolved request-changes,
   build status) separately if the calling tool needs to confirm a PR is actually eligible to merge,
   since none of that is enforced by the approve call itself.
6. **Before merging: stop and confirm with the operator.** Merging moves the source branch's commits
   into the destination branch's history — a production-affecting, hard-to-reverse action. Confirm the
   destination branch, the chosen merge strategy, and whether the source branch should be closed
   (deleted) as part of the merge, before submitting.
7. **Merge the request** — submit the merge call with a `merge_strategy` (`merge_commit`, `squash`, or
   `fast_forward` — plus rebase-based variants documented in the support docs as available in the
   Bitbucket Cloud UI; confirm the exact set of strategy values the API accepts for the target
   workspace's plan before relying on a rebase variant programmatically, since the schema referenced
   here only enumerates the three listed), an optional `message` (the resulting commit message, capped
   at 128 KiB), and `close_source_branch` (defaults to whatever was set at PR creation if omitted). If
   the repository enforces a merge checklist (minimum approvals, passing build, resolved tasks) and it
   isn't satisfied, Bitbucket Cloud rejects the merge — report that rejection using the API's own
   returned reason rather than a generic failure.
8. **To decline instead of merging** — call the dedicated decline endpoint. This is permanent per the
   source docs: a declined pull request cannot be reopened through the platform; a new pull request
   must be opened if the change should be reconsidered. Comments and tasks on the declined PR remain
   visible, but further commits to the source branch no longer update it.
9. **Confirm the outcome** — after a merge call, treat a response describing the resulting merge
   commit (or an accepted async task reference — Bitbucket Cloud can process a merge asynchronously
   for large PRs, exposing a task-status endpoint) as success; re-fetch the PR and confirm
   `state: MERGED` if the calling tool needs a definitive synchronous check. After a decline, re-fetch
   and confirm `state: DECLINED`.
10. **Handle undocumented failures verbatim** — for any error not already covered by a specific step
    above, report FAILED with the underlying response's actual error detail rather than guessing at a
    cause.

## Patterns

- **Approval is a toggle, not a log.** Re-approving after already approving is idempotent from the
  caller's perspective; there is no separate "list all review events" concept the way GitHub models
  reviews — only the current approved/not-approved state per user plus separate request-changes state.
- **Declining is one-way.** Unlike GitHub's close-then-reopen or GitLab's `state_event: reopen`,
  Bitbucket Cloud's own support documentation states a decline can't be undone on the same PR — plan
  accordingly before calling decline instead of update.
- **Merge strategy availability can be workspace/plan-dependent.** The exact set of merge strategies
  documented in the support docs (merge commit, fast forward, rebase-merge, rebase-fast-forward,
  squash, squash-fast-forward-only) is broader than the three values (`merge_commit`, `squash`,
  `fast_forward`) found in the API's own request schema at retrieval time — verify which values the
  target site actually accepts before assuming a rebase-based strategy is available via the API.

## Known limitations

- Does not cover workspace/repository or branch creation, default-reviewer configuration, or
  merge-checklist/branch-permission configuration — this procedure only operates within whatever rules
  are already configured on the target repository.
- The primary interactive API reference page for this resource did not return retrievable prose at
  retrieval time; endpoint paths and field names here are corroborated against the API's own OpenAPI
  schema instead (see the sources note above) — verify field names against the live API response for
  the target site before depending on an exact, uncommon field.
- The full set of UI-documented merge strategies vs. the API's own accepted `merge_strategy` values is
  not fully reconciled in the sources retrieved (see Patterns above) — confirm accepted values for the
  target workspace before scripting a rebase-based merge.
- Decline is documented as permanent/non-reopenable; this procedure does not attempt a workaround.

## Tools

| Operation | Description | Category |
|---|---|---|
| List pull requests | List/filter PRs in a repository | Pull Requests |
| Get a pull request | Fetch one PR by `pull_request_id` | Pull Requests |
| Create a pull request | Open a new PR from a source branch into a destination branch | Pull Requests |
| Update a pull request | Change title/description/destination/reviewers | Pull Requests |
| Approve a pull request | Toggle the authenticated user's approval on | Pull Requests |
| Remove approval | Toggle the authenticated user's approval off | Pull Requests |
| Request changes | Record a request-changes decision | Pull Requests |
| Merge a pull request | Merge with a chosen `merge_strategy` | Pull Requests |
| Decline a pull request | Decline without merging (permanent) | Pull Requests |

## Verification checklist

- [ ] Source and destination branches confirmed to exist before create
- [ ] For create: `title` and `source` were present; `destination` set explicitly rather than left to
      default when a specific target branch is intended
- [ ] For merge: operator confirmation obtained before submission (step 6); `merge_strategy` value
      confirmed valid for the target workspace rather than assumed
- [ ] Merge outcome confirmed via a re-fetched `state: MERGED`, not assumed from a 2xx status alone
      (accounting for Bitbucket Cloud's async merge path on large PRs)
- [ ] Decline treated as permanent — operator understands a new PR is required to reconsider the
      change, not a reopen call
