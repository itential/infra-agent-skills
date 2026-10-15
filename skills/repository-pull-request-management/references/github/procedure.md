# GitHub — Pull Request Management Procedure

Creates, reads, updates, reviews, merges, or closes a pull request against a GitHub repository
through the Pulls and Pull Request Reviews REST resources.

Scope: open/list/get/edit a pull request, record a review decision, merge a pull request, or close
one without merging. Does not cover creating the repository or the branches involved, configuring
branch protection or required-status-check rules, CI workflow configuration, or GitHub's separate
merge queue feature beyond noting it exists (see "Known limitations"). Assumes an authenticated REST
client against the GitHub API (a token — personal access, OAuth app, or GitHub App installation token
— carrying at minimum write access to pull requests on the target repository) is already available.

Source: GitHub REST API reference, "Pulls" and "Reviews" pages under `docs.github.com/en/rest/pulls`,
retrieved 2026-09-29.

## Operational procedure

1. **Confirm the repository and both branches are reachable** — resolve `owner`/`repo`, and confirm
   the source branch (`head`, as `username:branch` for a cross-repository/fork request) and target
   branch (`base`) both exist. If either branch can't be found, stop and report FAILED with "branch
   not found" (see `endpoints.md`).
2. **Create the pull request** — submit `head`, `base`, and either a `title` or an existing `issue`
   number to convert into a PR, plus optional `body`, `draft`, and `maintainer_can_modify`. If GitHub
   returns a validation failure (e.g. no diff between branches, or a PR already open for that
   head/base pair), report REJECTED_VALIDATION_FAILED with the returned error detail rather than
   retrying blindly.
3. **To list or inspect existing requests** — list with optional `state` (`open`/`closed`/`all`),
   `head`, `base`, and `sort` filters, or fetch one by its number. Treat the `mergeable` field on a
   fetched PR as three-valued: `true`, `false`, or `null` (GitHub is still computing it — if the
   calling tool needs a determinate answer, re-fetch after a short delay rather than treating `null`
   as failure).
4. **To update an open request** — submit only the fields being changed among `title`, `body`,
   `state` (see step 6 for what `state: closed` means), `base`, and `maintainer_can_modify`. Do not
   resend unrelated existing values as if they were being changed.
5. **To record a review decision** — submit a review against the PR with an explicit `event`:
   `APPROVE`, `REQUEST_CHANGES`, or `COMMENT`. A `body` is required for `REQUEST_CHANGES` and
   `COMMENT`; omitting `event` entirely creates a pending review that isn't visible to other
   participants until separately submitted — if the caller's intent is an immediate, visible review
   decision, always include `event` explicitly. This review object is independent of the PR's own
   `state`/merge fields; recording a review does not merge or close the PR by itself.
6. **To close a request without merging** — update it with `state: closed`. This leaves the source
   branch's commits out of the target branch entirely; it is a distinct outcome from merging, not a
   failed-merge fallback. Report CLOSED, not MERGED, and don't imply the change landed.
7. **Before merging: stop and confirm with the operator.** Merging moves the source branch's commits
   into the target branch's history — a production-affecting, hard-to-reverse action (undoing it
   afterward is a new revert commit, not an in-place undo). Confirm the target branch, the chosen
   merge method, and that any organization-configured required reviews/status checks the calling tool
   can observe are satisfied, before submitting.
8. **Merge the request** — submit the merge call with a required `merge_method` (`merge`, `squash`,
   or `rebase`), and optionally `commit_title`/`commit_message` and a `sha` to guard against merging a
   different commit than the one reviewed (GitHub rejects the merge with a conflict if the PR's
   current head doesn't match the supplied `sha`). Treat a response with `merged: true` as success;
   `merged: false` with a `message` describing why (e.g. required status checks not met, merge
   conflict) as a documented rejection, not a generic failure — surface that message verbatim.
9. **Confirm the outcome** — after a merge call, treat `merged: true` in the response body as the pass
   criterion; optionally re-fetch the PR and confirm its `merged` field. After a close, re-fetch and
   confirm `state: closed` and `merged: false`.
10. **Handle undocumented failures verbatim** — for any error not already covered by a specific step
    above, report FAILED with the underlying response's actual error detail rather than guessing at a
    cause.

## Patterns

- **`mergeable` is asynchronous.** GitHub computes it as a background job after certain PR state
  changes; a `null` value means "not yet known," not "not mergeable." Don't treat `null` as a
  rejection.
- **Review and merge are separate objects with separate write paths.** A PR can accumulate any number
  of reviews with different `event` values; none of them changes the PR's own `state` or triggers a
  merge — a merge is always its own explicit call (step 8).
- **`state: closed` via update and an actual merge produce different terminal states** — closing does
  not merge, and merging does not require closing first (a successful merge implicitly resolves the
  PR without a separate close call).

## Known limitations

- Does not cover repository or branch creation, branch-protection/required-status-check
  configuration, or CI workflow setup — this procedure only operates within whatever rules are
  already configured on the target repository.
- Does not cover GitHub's merge-queue / stacked-PR asynchronous merge endpoint in depth — the source
  documents it as a distinct, newer mechanism from the synchronous merge call in step 8; if the
  calling tool specifically needs merge-queue behavior, that is a materially different flow not
  detailed here.
- Draft-PR toggling (`draft: true`/`false`) is available via create/update, but the source does not
  document every downstream effect (e.g. exact interaction with required reviewers) — verify against
  the target repository's own configuration before relying on draft state to block a merge.
- The source does not document a fixed catalog of error strings for every validation failure beyond
  the generic `{"message": ..., "errors": [...]}` shape — step 10 exists because of this.

## Tools

| Operation | Description | Category |
|---|---|---|
| List pull requests | List/filter PRs in a repository | Pull Requests |
| Get a pull request | Fetch one PR by number, including `mergeable`/`mergeable_state` | Pull Requests |
| Create a pull request | Open a new PR from `head` into `base` | Pull Requests |
| Update a pull request | Change title/body/state/base/maintainer_can_modify | Pull Requests |
| Create a review | Record APPROVE/REQUEST_CHANGES/COMMENT against a PR | Pull Request Reviews |
| List reviews | List existing reviews on a PR | Pull Request Reviews |
| Merge a pull request | Merge with a chosen `merge_method` | Pull Requests |
| Check if merged | Confirm merged status via a dedicated GET | Pull Requests |

## Verification checklist

- [ ] Source and target branches confirmed to exist before create
- [ ] For create: `head`/`base` and a `title` or `issue` were present, not guessed
- [ ] For review: `event` was set explicitly (not left blank as a pending review) unless a pending
      review was actually intended
- [ ] For merge: operator confirmation obtained before submission (step 7), and `merge_method` was
      explicit, not defaulted silently
- [ ] Merge outcome confirmed via `merged: true` in the response, not assumed from a 2xx status alone
- [ ] Close vs. merge outcome reported using the correct distinct status
