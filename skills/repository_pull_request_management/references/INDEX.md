# Repository Pull/Merge Request Management — Vendor Index

One row per supported vendor. Each vendor directory holds its own `procedure.md` (the full
step-by-step) plus wire-level `endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| GitHub | `github/` | Create/list/get/update a pull request; create a review (approve/request changes/comment); merge; close without merging | Review is a first-class object separate from the PR update call; merge strategy is chosen per merge call, not fixed per repo |
| GitLab | `gitlab/` | Create/list/get/update a merge request; approve/unapprove; merge; close without merging | Approval is a dedicated API (`merge_request_approvals`), separate from the merge-request update call; `state_event` param drives close vs. reopen |
| Bitbucket Cloud | `bitbucket_cloud/` | Create/list/get/update a pull request; approve/unapprove (toggle); request changes; merge; decline | Approve is a toggle endpoint, not an object with history like GitHub's reviews; decline is terminal — a declined PR cannot be reopened via source docs, only recreated |
| Bitbucket Server & Data Center | `bitbucket_server_data_center/` | Create/list/get/update a pull request; set a participant's review status; merge; decline; reopen | Every mutating call (update, merge, decline, reopen) requires the PR's current `version` number to prevent concurrent-modification conflicts — the one platform here with that requirement documented explicitly |

**Not in scope for this skill:** repository/branch creation, branch-protection or merge-check rule
configuration, CI/pipeline configuration, webhook management — see each vendor's own
`procedure.md` "Known limitations" for exact boundaries.

## Adding a new vendor

See `AGENTS.md`, "Adding a vendor to an existing capability."
