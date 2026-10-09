# Jira Cloud issue records

Jira Cloud REST v3 procedures for one issue, its configured transition, and its comments.

## Common Sequences

- Inspect: **Search issues → Read issue → List comments**.
- Create: **Read creation metadata → Create issue → Read issue**.
- Change or discuss: **Read issue → Read edit metadata and Edit issue, or Read transitions and Transition issue, or Add comment → Read issue or List comments**.

### Search issues

The enhanced JQL search applies the requested JQL and explicit returned fields. Success returns matching issues and a continuation token when another page exists. Visibility is limited by project browse permission and issue security. Recent writes may not immediately appear in ordinary search; the documented reconciliation option can include specified issue identifiers for stronger consistency. Search is not the sole verification of a recent write. Invalid JQL produces a 400 result, and 401 requires authentication repair.

### Read issue

The issue detail operation resolves the supplied issue identifier or key. Success returns the issue's canonical key and current fields. Jira may resolve moved or case-mismatched keys without a redirect; the returned key is authoritative. A 401 requires authentication repair; 404 requires checking identity and visibility.

### Read creation metadata

For the selected project, the creation metadata operations first enumerate available issue types, then enumerate creation fields for the selected type. Both are paginated. Success identifies the type, required fields, accepted operations, and allowed values where provided. No standard incident type, priority, or required custom field is presumed. A 400 requires correcting the project/type input; 401 requires authentication repair.

### Create issue

The create operation supplies the selected project, issue type, summary, and fields required by the returned metadata. Descriptions and multiline text fields use Atlassian Document Format; single-line text fields use strings. Immediately before creating the live issue, **stop and confirm with the operator before proceeding**. Success returns an issue identifier and key with a 201 result. A 400 or 422 requires correcting validation or field errors; 401 requires authentication repair; 403 requires project creation permission. A timed-out create is reconciled against retrieved issue records before any repeat.

### Read edit metadata

The issue's edit metadata identifies editable fields and supported field operations. Success returns field metadata for the selected issue. A 401, 403, or 404 requires resolving authentication, editing permission, or identity/visibility. The current API documentation states that editability does not rely on screen configuration; this procedure does not try to override screen or workflow restrictions.

### Edit issue

The edit operation submits only approved changes accepted by edit metadata. A field is represented either as a direct value or as update operations as documented for that field. Immediately before changing the live issue, **stop and confirm with the operator before proceeding**. Success is a 204 result, or a 200 issue response when the return-issue option is selected; a subsequent read verifies the actual fields. A transition included in an ordinary edit is ignored: state movement requires the transition operation. A 400 or 422 requires correcting fields; 401/403/404 require authentication/permission/identity review; 409 requires re-reading the conflicting issue before another change.

### Read transitions

The available-transition operation expands transition fields. Success returns the transitions available for the current issue and caller, including the fields required on each transition screen. An empty list can mean the caller lacks transition permission or no matching transition is available; it does not establish that the issue is resolved. A 401 or 404 requires authentication or identity/visibility review.

### Transition issue

The transition operation uses an identifier returned for the issue's current state and supplies its required transition fields. Immediately before moving the live issue, **stop and confirm with the operator before proceeding**. Success is a 204 result, followed by a detail read showing the target status. A 400 or 422 requires refreshing transition metadata and correcting fields; 409 requires re-reading current state; 413 requires reducing the submitted content; 401/404 require authentication or identity/visibility review. No universal open-to-resolved transition is assumed.

### List comments

The comment collection uses its documented pagination and requested creation ordering. Success returns comments that the caller is permitted to see, including any applicable comment restrictions. A 400 requires correcting pagination or ordering; 401/404 require authentication or issue identity/visibility review.

### Add comment

The comment operation submits the approved Atlassian Document Format body and any explicitly requested visibility restriction. Immediately before publishing the comment, **stop and confirm with the operator before proceeding**. Success returns the comment identifier with a 201 result. A 400 requires correcting the body or restriction; 413 requires reducing oversized content; 401/404 require authentication or issue identity/visibility review. When delivery is uncertain, a comments read resolves whether the comment was published before repetition.

## Patterns

Creation, edit, and transition metadata solve different questions and are not substitutes for each other. Transition identifiers and statuses are configuration-dependent. Reads are constrained by project, issue, and comment permissions.

For a 429 response, the documented retry delay governs backoff. A successful write must not be repeated merely because a follow-up search is eventually consistent.

## Known limitations

Cloud REST v3 only; no Data Center bindings. Bulk creation, issue linking, project administration, and customer-specific incident/change approval workflows are outside this procedure. A transition can have business-specific effects that the API reference does not define; the operator supplies the intended available transition.

## Tools

| Operation | Description | Category |
|---|---|---|
| Search issues | Search visible issues with JQL | Read |
| Read issue | Retrieve canonical issue and fields | Read |
| Read creation metadata | Resolve project types and creation fields | Read |
| Create issue | Create one issue from metadata | Write |
| Read edit metadata | Resolve editable fields | Read |
| Edit issue | Update selected issue fields | Write |
| Read transitions | Resolve available state changes | Read |
| Transition issue | Apply a selected workflow transition | Write |
| List comments | Retrieve visible discussion | Read |
| Add comment | Publish one comment | Write |

Bindings and primary citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Project, canonical issue key, and requested operation are unambiguous.
- Required fields and transitions came from that project's or issue's metadata.
- Returned creation/comment identifiers or accepted mutation statuses are retained.
- Readback confirms changed fields or target status; incomplete search visibility is reported.
