---
name: repository-pull-request-management
description: Open, review, update, merge, or close a pull request (GitHub, Bitbucket) or merge request (GitLab) on a source-control hosting platform — GitHub, GitLab, Bitbucket Cloud, or Bitbucket Server & Data Center. Use when a change needs to move from a source branch into a target branch through a reviewed request, when an open request needs its title/description/target branch updated, when a reviewer needs to approve/request changes, or when a request needs to be merged or closed/declined without merging. Assumes an authenticated API client (personal access token, OAuth app token, or app installation token as the target platform requires) for the target platform is already available; this skill does not provision or authenticate that client. Does not cover repository/branch creation, branch protection rule configuration, CI/pipeline configuration, or webhook management.
argument-hint: "[platform] [action] [repo/project] [source_branch] [target_branch]"
---

# Repository Pull/Merge Request Management

Opens, reviews, updates, merges, or closes a pull request (GitHub, Bitbucket) or merge request
(GitLab) on one of the supported source-control hosting platforms, following that platform's own
documented API procedure, field rules, and merge/approval model.

## When to use this skill

- A code change on a source branch needs to be proposed for review and integration into a target
  branch on GitHub, GitLab, Bitbucket Cloud, or Bitbucket Server & Data Center.
- An existing open request's title, description, target branch, or reviewer list needs updating.
- A request needs a review decision recorded (approve, request changes, comment) where the platform
  exposes that as its own action.
- A request needs to be merged, or closed/declined without merging.
- Not for creating the repository or the branches themselves (the source and target branches must
  already exist before a request can be opened), configuring branch-protection/merge-check rules,
  configuring CI pipelines that gate a merge, or managing webhooks — those are separate concerns.

## Universal concepts (apply regardless of platform)

- **Every request has a source and a target branch, and represents the diff between them.** All four
  platforms require both branches to exist first and require them to actually diverge — an attempt to
  open a request with no difference between source and target is rejected everywhere, though the
  exact rejection behavior (error vs. silently empty diff) is platform-specific.
- **Closing without merging and merging are distinct, separately-invoked outcomes everywhere.** No
  platform in this skill treats "close" as an implicit merge or vice versa; each is its own action
  with its own resulting state, and a closed/declined request that was never merged leaves the target
  branch untouched.
- **A merge is not a single fixed operation** — every platform offers more than one merge strategy
  (e.g. a real merge commit, squashing into one commit, or fast-forwarding/rebasing), and the caller
  must pick one; there is no universal default that's safe to assume without checking the target
  platform's own procedure.
- **Review/approval is where these platforms genuinely diverge — do not assume one model fits all.**
  Each platform models a reviewer's stance (approve, request changes, comment) as its own distinct
  kind of object or field, with its own API shape and its own relationship to branch-protection/
  merge-check rules. Treat approval as a platform-specific step every time — see that platform's own
  `procedure.md` for exactly how it represents it.
- **Merging a request is a hard-to-reverse, production-affecting action** — once merged, the change is
  in the target branch's history; undoing it is a new revert commit/PR, not an in-place undo. Every
  platform procedure below requires operator confirmation before a merge call is submitted (see
  "Known limitations" and rule enforced in each `procedure.md`).

There is no single wire-level standard (no RFC) governing pull/merge requests the way DNS has
RFC 1035 — every concept above is a pattern observed consistently across all four platforms' own
documentation, not a standardized protocol; treat any additional platform added later as capable of
invalidating one of these claims (see each vendor's own notes in `references/INDEX.md`).

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. If it
   isn't one of the platforms in `references/INDEX.md`, stop: this skill doesn't cover it, and does
   not improvise a generic procedure for an unsupported platform.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist. This file is intentionally the router; the real steps live per platform because the
   platforms' approval and merge models genuinely do not share one procedure (see "Universal
   concepts" above).
3. **Report the outcome** using that platform procedure's own status vocabulary (e.g. `CREATED`,
   `MERGED`, `DECLINED`/`CLOSED`, `REJECTED_*`, `FAILED`) — don't normalize it away.

## Known limitations

- Does not cover repository or branch creation — every platform procedure assumes both the source and
  target branches already exist.
- Does not cover branch-protection/merge-check rule configuration (required-approval counts, required
  status checks) — this skill only operates within whatever rules are already configured on the
  target repository/project.
- Does not cover CI/pipeline configuration or webhook management, even where a platform's merge
  behavior (e.g. GitLab's merge-when-pipeline-succeeds) references pipeline state.
- **Merging is treated as a destructive/hard-to-reverse action on every platform** — each
  `procedure.md` requires operator confirmation before the merge call is submitted; never skip that
  gate because the API call would otherwise succeed.
- Platform coverage is exactly the four vendors in `references/INDEX.md` — a platform not listed there
  needs a new `references/<platform>/procedure.md` before this skill can be used for it.

## Contributing to this skill

**`SKILL.md` itself should only ever change for two reasons: a bug in the universal-concepts/router
content above, or adding a pointer to a newly-supported platform.** Platform-specific procedure
changes — a new error code, a corrected field name, a changed API path, a revised approval model —
belong in that platform's own `references/<platform>/procedure.md` and `endpoints.md`, never here. If
you're about to add vendor-specific detail to this file, put it in the platform's reference file
instead.

## Tools

Each platform assumes its own authenticated REST client — see `references/INDEX.md` for which, and
that platform's `procedure.md` for the specific operations/mechanisms used.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates and error
      handling — not a generic/improvised sequence
- [ ] Merge (or any other hard-to-reverse action) was confirmed with the operator before submission
- [ ] Outcome reported using the platform procedure's own status vocabulary
