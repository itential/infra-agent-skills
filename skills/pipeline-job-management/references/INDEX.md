# pipeline-job-management: platform references

| Platform | Procedure | Scope | Notes |
|---|---|---|---|
| GitHub Actions | [github/procedure.md](github/procedure.md) | List/read workflow runs and dispatch a configured workflow | REST API version 2026-03-10 dispatch returns run identity. |
| GitLab CI/CD | [gitlab/procedure.md](gitlab/procedure.md) | List/read/create/retry/cancel pipelines, list jobs and retrieve trace | API v4; ordinary branch/tag pipelines, not merge-request creation. |
