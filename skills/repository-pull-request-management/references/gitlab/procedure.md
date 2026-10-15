# GitLab — Merge Request Management Procedure

Creates, reads, updates, approves, merges, or closes a merge request against a GitLab project through
the Merge Requests and Merge Request Approvals REST resources.

Scope: open/list/get/edit a merge request, record an approval or unapprove, merge a merge request, or
close one without merging. Does not cover creating the project or the branches involved, configuring
approval rules/protected-branch settings, or CI/CD pipeline configuration beyond noting where merge
behavior can depend on pipeline state. Assumes an authenticated REST client against the GitLab API (a
personal/project/group access token or OAuth token carrying at minimum Developer-level write access
to merge requests on the target project) is already available.

Source: GitLab REST API reference, "Merge requests" and "Merge request approvals" pages under
`docs.gitlab.com/ee/api/`, retrieved 2026-09-29.

## Operational procedure

1. **Confirm the project and both branches are reachable** — resolve the project by numeric ID or
   URL-encoded path, and confirm the `source_branch` and `target_branch` both exist. If either can't
   be found, stop and report FAILED with "branch not found" (see `endpoints.md`).
2. **Create the merge request** — submit `source_branch`, `target_branch`, and `title` as the minimum
   required set, plus optional `description`, `assignee_ids`, `reviewer_ids`, `labels`, `milestone_id`,
   and squash preference. If the source and target branches don't diverge, or an open MR already
   exists for that pair, report REJECTED_VALIDATION_FAILED with the API's returned error detail.
3. **To list or inspect existing requests** — list at the project, group, or instance level with
   filters including `state` (`opened`/`closed`/`locked`/`merged`/`all`), `labels`, `author_id`,
   `assignee_id`, `reviewer_id`, `milestone`, `search`, and `draft`. Fetch one by its
   `merge_request_iid` (the project-scoped display number, not the global `id`). Treat
   `detailed_merge_status` as the authoritative mergeability field; the older `merge_status` is
   deprecated and should not be relied on for a new integration.
4. **To update an open request** — submit only the fields being changed among `title`, `description`,
   `target_branch`, `assignee_ids`, `reviewer_ids`, `labels`, `milestone_id`, and `state_event`. Do not
   resend unrelated existing values.
5. **To close a request without merging** — update it with `state_event: close`. This is a distinct,
   separately-invoked outcome from merging (see step 8); GitLab does not treat closing as an implicit
   merge, and a merge request can later be reopened with `state_event: reopen` unless the source
   branch has since been deleted.
6. **To record an approval** — submit an approve call against the merge request; optionally supply a
   `sha` to guard against approving a stale version of the diff (a mismatch returns a conflict). To
   remove your own prior approval, submit the separate unapprove call. Fetch the approval state (which
   includes an `approved_by` list) to confirm how many/which eligible approvers have approved, if the
   calling tool needs that before merging. Approval here is deliberately separate from GitLab's
   optional approval-rules configuration (required approver counts, eligible approver groups) — this
   procedure records a decision within whatever rules the project already has configured; it does not
   create or change those rules.
7. **Before merging: stop and confirm with the operator.** Merging moves the source branch's commits
   into the target branch's history — a production-affecting, hard-to-reverse action. Confirm the
   target branch, the merge/squash choice, and whether the merge should wait on pipeline success,
   before submitting.
8. **Merge the request** — submit the merge call with optional `merge_when_pipeline_succeeds` (defer
   the merge until the project's CI pipeline for that commit passes), `squash` (combine into one
   commit), and `should_remove_source_branch`. A merge request whose `draft` flag is still set, or
   whose `detailed_merge_status` reports it isn't mergeable (open discussions, failed pipeline, missing
   approvals per configured rules, conflicts), is rejected — report the specific reason GitLab returns
   rather than a generic failure.
9. **Confirm the outcome** — after a merge call, treat a response containing a populated
   `merge_commit_sha` (or, for `merge_when_pipeline_succeeds`, an accepted/pending state) as success;
   re-fetch the MR and confirm `state: merged` if the calling tool needs a definitive check. After a
   close, re-fetch and confirm `state: closed`.
10. **Handle undocumented failures verbatim** — for any error not already covered by a specific step
    above, report FAILED with the underlying response's actual error detail rather than guessing at a
    cause.

## Patterns

- **`merge_request_iid` vs. `id`.** Every project-scoped endpoint in this procedure addresses the
  merge request by its project-local `iid` (the number shown in GitLab's UI), not the global `id` used
  internally — using the wrong one is a common source of "not found" errors.
- **Approval is a separate sub-resource from the MR update call.** Unlike closing/reopening (a field
  on the MR itself via `state_event`), recording an approval is its own dedicated endpoint, and
  GitLab's approval-rules configuration (how many approvals are required, from whom) lives in a
  further separate set of endpoints this procedure does not create or modify.
- **`merge_when_pipeline_succeeds` changes the merge call's immediate outcome.** Submitting it doesn't
  merge synchronously — it accepts the merge request for a deferred merge once CI passes, so a
  "success" response at that point means "accepted for deferred merge," not "merged now." Don't
  conflate the two when reporting outcome.

## Known limitations

- Does not cover project or branch creation, or configuring merge-request approval rules
  (required-approver counts/groups) — this procedure only records approvals within whatever rules are
  already configured on the target project.
- Does not cover CI/CD pipeline configuration, even though `merge_when_pipeline_succeeds` depends on
  pipeline outcome for the target commit.
- The source marks `merge_status` deprecated in favor of `detailed_merge_status`; a caller reading an
  older integration's use of `merge_status` should treat it as legacy, not authoritative.
- The source does not document a fixed catalog of error strings for every validation failure; step 10
  exists because of this.

## Tools

| Operation | Description | Category |
|---|---|---|
| List merge requests | List/filter MRs at project, group, or instance scope | Merge Requests |
| Get a merge request | Fetch one MR by `iid`, including `detailed_merge_status` | Merge Requests |
| Create a merge request | Open a new MR from `source_branch` into `target_branch` | Merge Requests |
| Update a merge request | Change title/description/target/labels/`state_event` | Merge Requests |
| Approve a merge request | Record an approval | Merge Request Approvals |
| Unapprove a merge request | Remove the authenticated user's approval | Merge Request Approvals |
| Get approval state | Fetch `approved_by` and approval status | Merge Request Approvals |
| Merge a merge request | Merge, optionally deferred to pipeline success | Merge Requests |

## Verification checklist

- [ ] Source and target branches confirmed to exist before create
- [ ] For create: `source_branch`, `target_branch`, `title` were present, not guessed
- [ ] For update/close/reopen: correct `state_event` value used, and only intentionally-changed
      fields were sent
- [ ] For merge: operator confirmation obtained before submission (step 7); if
      `merge_when_pipeline_succeeds` was used, outcome reported as "accepted for deferred merge," not
      "merged," until the pipeline actually completes and the MR is confirmed merged
- [ ] Approval state checked via the approvals endpoint, not inferred from the MR object alone, when
      the calling tool needs to confirm approvals before merging
- [ ] `merge_request_iid` (not the global `id`) used to address the request
