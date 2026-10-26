# Automation Job Execution — Vendor Index

One row per supported platform. Each directory holds its own `procedure.md` plus wire-level
`endpoints.md`.

| Vendor / Platform | Directory | Scope | Notes |
|---|---|---|---|
| AWX (Ansible) | `awx/` | Launch a job template; poll job; read output; cancel | Documented from the open-source AWX project. Red Hat Ansible Automation Platform's controller is AWX-derived but is **not** documented here (its docs were not reachable) — do not assume AWX routes, auth, or hostnames carry over to it |
| Jenkins | `jenkins/` | Trigger a build (with or without parameters); read build result; stop | Launch/auth/result values are from jenkins.io; queue-to-build lookup and stop route are marked unverified in the file |
| Azure DevOps | `azure-devops/` | Run a pipeline; poll run; read logs; cancel | Run has a state plus a separate result; cancel goes through the Build resource |
| Rundeck | `rundeck/` | Run a job; poll execution; read output; abort | Abort is a GET in the documented API; API version is part of the path |
| Puppet Enterprise | `puppet/` | Run a task or plan through the orchestrator; poll job; read report; stop | Run-Puppet-on-demand (deploy) is a documented sibling command but out of scope here; stop has a graceful and a forced mode |
| GitLab CI/CD | `gitlab-ci/` | Create a pipeline for a branch or tag; poll status; list jobs; read job log; cancel pipeline or job | One status field (no separate result); cancel returns 200 regardless of state, so re-read; retry, manual-job play, and merge request pipelines not covered; declared inputs need GitLab 18.1+ |

**Not in scope for this skill:** authoring job definitions, credentials/inventory management,
scheduling, platform installation — see each vendor's own "Known limitations".
