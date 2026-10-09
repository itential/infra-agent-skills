# GitHub issue records

GitHub REST procedures for one repository issue and its comments.

## Common Sequences

- Inspect issues: **List issues → Read issue → List comments**.
- Create an issue: **Create issue → Read issue**.
- Modify or discuss an issue: **Read issue → Update issue or Add comment → Read issue or List comments**.

### List issues

The repository issue listing applies the requested state, labels, assignee, and updated-since filters. Pagination follows the response links until the requested range is complete. A successful response is an array of issue objects. Entries carrying a pull-request marker are pull requests, even on this issue operation. The default state is open; all-state requests must be explicit. A 301 follows the documented moved-resource location after validating the repository target; 404 requires checking identity and access; 422 means invalid filters or abuse protection, not an empty result.

### Read issue

The issue detail operation uses the repository and issue number. Success returns the issue number, state, title, and current fields. A 304 means a conditional request found no change. A 301 indicates transfer; 404 can mean an unreadable or deleted/transferred issue; 410 can mean a deleted issue. These are not proof that an inaccessible issue never existed.

### Create issue

The create operation requires a title and accepts the requested body, labels, assignees, and milestone. Immediately before creating the live record and its notifications, **stop and confirm with the operator before proceeding**. Success returns the new issue with a 201 result. The subsequent read compares the requested fields with stored fields: GitHub can silently omit labels, assignees, or milestone without sufficient repository permission. A 400 or 422 requires correcting the submitted data; 403 requires resolving permission or rate-limit details; 404 requires checking the repository; 410 means issues are disabled for that repository; 503 is a service failure. A timed-out create has an unknown outcome; the issue listing must resolve whether a record was created before any repeat.

### Update issue

The update operation sends only the requested field changes. Label and assignee arrays replace their existing sets; empty arrays clear them. A null milestone removes that association. Immediately before changing the live issue, **stop and confirm with the operator before proceeding**. Success returns the issue with a 200 result; a read verifies the state and every requested field, including fields that insufficient permissions can silently drop. A 301 requires resolving the transferred issue; 403, 404, 410, 422, and 503 use the same handling as above. Closing uses the documented closed state and an applicable state reason; reopening uses the open state. The optional state reason does not invent a workflow transition.

### List comments

The comment list returns comments ordered by increasing identifier, with updated-since filtering and pagination. Success is an array of comment objects, including an empty array. A 404 or 410 requires checking issue existence/access rather than reporting that there are no comments.

### Add comment

The comment operation requires the approved comment body. Immediately before publishing the comment and its notifications, **stop and confirm with the operator before proceeding**. Success returns a comment identifier and body with a 201 result. A 403, 404, 410, or 422 requires resolving permission, issue availability, validation, or abuse protection respectively. If delivery is uncertain, the comment list resolves whether the body was stored before another publication.

## Patterns

- Issue numbers are repository-scoped; pull-request and issue identifiers are not interchangeable.
- Writes can generate notifications and incur secondary rate limits. Rate-limit responses require following GitHub's response guidance rather than a locally invented fixed retry rate.
- A successful issue write can omit optional fields for which the caller lacks permission; readback is material.

## Known limitations

This procedure does not manage pull-request reviews, issue links, projects, bulk operations, or issue deletion. A repository issue is not a predefined ITSM incident workflow. Exact retry timing is response-dependent.

## Tools

| Operation | Description | Category |
|---|---|---|
| List issues | Retrieve repository issue candidates | Read |
| Read issue | Retrieve one issue's current state | Read |
| Create issue | Create one issue | Write |
| Update issue | Change specified issue fields | Write |
| List comments | Retrieve issue discussion | Read |
| Add comment | Publish one issue comment | Write |

Bindings and source citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Repository and issue number identify the requested issue, with pull requests distinguished.
- Pagination and conditional responses are represented accurately.
- The returned issue or comment identifier was retained.
- Stored optional fields and final state match the requested operation, or omissions are reported.
