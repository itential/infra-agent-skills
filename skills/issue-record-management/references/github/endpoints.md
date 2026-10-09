# GitHub issue bindings

Official sources: [Issues](https://docs.github.com/en/rest/issues/issues), [Issue comments](https://docs.github.com/en/rest/issues/comments), REST API documentation retrieved 2026-10-09. The published examples use API version `2026-03-10`.

Base: `https://api.github.com`. An existing authenticated client supplies `Authorization: Bearer <token>`, `Accept: application/vnd.github+json`, and `X-GitHub-Api-Version: 2026-03-10`. Fine-grained tokens need repository Issues read/write permission as applicable; comment operations also document Pull requests permission as an alternative. The repository owner/name and issue number are resolved inputs.

| Operation | Literal binding | Input | Result |
|---|---|---|---|
| List issues | `GET /repos/{owner}/{repo}/issues` | `state=open\|closed\|all`, `labels` comma-separated, `assignee`, `since` ISO timestamp; `per_page` at most 100; `page` | 200 issue array; a `pull_request` member distinguishes pull requests; 301/404/422 |
| Read issue | `GET /repos/{owner}/{repo}/issues/{issue_number}` | Conditional headers only where the client supports them | 200 issue; 301/304/404/410 |
| Create issue | `POST /repos/{owner}/{repo}/issues` | `title` required; optional `body`, `labels`, `assignees`, `milestone` | 201 issue; 400/403/404/410/422/503 |
| Update issue | `PATCH /repos/{owner}/{repo}/issues/{issue_number}` | Optional `title`, `body`, `state=open\|closed`, `state_reason=completed\|not_planned\|duplicate\|reopened`, `labels`, `assignees`, `milestone` | 200 issue; 301/403/404/410/422/503 |
| List comments | `GET /repos/{owner}/{repo}/issues/{issue_number}/comments` | `since`, `per_page` at most 100, `page` | 200 array; 404/410 |
| Add comment | `POST /repos/{owner}/{repo}/issues/{issue_number}/comments` | `body` required | 201 comment; 403/404/410/422 |

List pagination uses the returned `Link` relations. Returned identifiers, `state`, field values, comment `id` and `body` are the verification data. Authentication, authorization, and rate-limit behavior remain bound to the selected credential and GitHub deployment; no secret appears in the output artifact.
