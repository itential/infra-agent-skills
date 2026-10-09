# Jira Cloud issue bindings

Official sources: [Issues API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/), [Issue search](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/), [Comments](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/), [Rate limiting](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/), Cloud REST v3 and publisher OpenAPI, retrieved 2026-10-09.

Base for site-scoped authentication: `https://<site>.atlassian.net`. An existing authenticated client binds site or OAuth gateway routing as appropriate; the procedure does not construct credentials. JSON request/response media type is `application/json`.

| Operation | Literal binding | Required or material inputs | Success / documented failures |
|---|---|---|---|
| Search issues | `POST /rest/api/3/search/jql` | `jql`, requested `fields`; `maxResults`, `nextPageToken`; optional `reconcileIssues` numeric IDs | 200 issues and `nextPageToken`/`isLast`; 400/401 |
| Read issue | `GET /rest/api/3/issue/{issueIdOrKey}` | Optional `fields`, `expand` | 200 issue with canonical `key`; 401/404 |
| Creation types | `GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes` | `startAt`, `maxResults` (maximum 200) | 200 paginated types; 400/401 |
| Creation fields | `GET /rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}` | `startAt`, `maxResults` (maximum 200) | 200 paginated field metadata; 400/401 |
| Create issue | `POST /rest/api/3/issue` | `fields.project`, `fields.issuetype`, `fields.summary`; remaining required fields from metadata | 201 `id`, `key`, `self`; 400/401/403/422 |
| Read edit metadata | `GET /rest/api/3/issue/{issueIdOrKey}/editmeta` | Resolved issue | 200 `fields`; 401/403/404 |
| Edit issue | `PUT /rest/api/3/issue/{issueIdOrKey}` | `fields` and/or `update` without duplicating one field in both; optional query `returnIssue=true` | 204, or 200 with return option; 400/401/403/404/409/422 |
| Read transitions | `GET /rest/api/3/issue/{issueIdOrKey}/transitions` | `expand=transitions.fields` | 200 `transitions`; 401/404 |
| Transition issue | `POST /rest/api/3/issue/{issueIdOrKey}/transitions` | `transition.id`; required transition `fields`/`update` | 204; 400/401/404/409/413/422 |
| List comments | `GET /rest/api/3/issue/{issueIdOrKey}/comment` | `startAt`, `maxResults`, `orderBy=created\|-created\|+created` | 200 comment page; 400/401/404 |
| Add comment | `POST /rest/api/3/issue/{issueIdOrKey}/comment` | `body` ADF document; optional `visibility` restriction | 201 comment; 400/401/404/413 |

An ADF text document uses `{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"<approved text>"}]}]}`. Metadata supplies field identifiers, required flags, supported operations, and allowed values; no custom field ID is hard-coded. Error bodies use `errorMessages` and/or `errors` where returned. Rate-limit responses can include `Retry-After`; the current rate-limiting documentation governs retries.
