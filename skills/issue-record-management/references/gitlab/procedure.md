# GitLab project issue records

GitLab REST procedures for project issues and discussion notes.

## Common Sequences

- Inspect: **List issues → Read issue → List notes**.
- Create: **Create issue → Read issue**.
- Modify or discuss: **Read issue → Update issue or Add note → Read issue or List notes**.

### List issues

The project issue list uses an explicit project and the requested state, labels, assignee, and date filters. Success returns an issue array; response pagination links establish whether more results remain. Assignee identifier and assignee username filtering are alternatives, not simultaneous inputs. Label matching requires all supplied labels. Access limits private and confidential issue visibility.

### Read issue

The single-issue operation uses the project and project-local issue IID. Success returns that issue's IID, global identifier, state, title, and description. A global identifier does not replace the project-local IID in this operation. A 404 requires resolving identity and visibility rather than declaring a confidential issue absent.

### Create issue

The create operation supplies a title and only the selected optional description, labels, assignee identifiers, milestone, or confidentiality. The description must fit the documented limit. A label not already present can be created as a side effect of setting labels. Immediately before creating the record and any labels, **stop and confirm with the operator before proceeding**. Success returns the created issue with its IID and stored fields. Issue creation returns 403 if the project's issue feature is disabled. If the request outcome is uncertain, the listing resolves whether the issue already exists before another creation.

### Update issue

The update operation uses at least one supported change. A close or reopen request uses the state-event operation; changing an issue's description is separate from a state change. Replacing labels with an empty value removes them; additive and subtractive label fields avoid replacing the full set. Immediately before changing the live issue, **stop and confirm with the operator before proceeding**. Success returns the modified issue. A detail read verifies its title, label set, assignees, and opened/closed state as applicable.

### List notes

The issue's notes collection is paginated. The requested activity filter distinguishes comments from system activity; an unfiltered collection can contain both. Success returns note identifiers, bodies, author information, and the system-note flag. A filtered empty page does not justify skipping pagination supplied by the server.

### Add note

The note creation operation supplies the approved body within the documented size limit. Internal-note visibility is explicit; the deprecated confidentiality option is not substituted for it. Immediately before publishing the note, **stop and confirm with the operator before proceeding**. Success returns the new note object. When a timeout leaves the outcome unknown, listing notes determines whether the note was stored before another publication.

### Handle request failures

For each operation, 400 means the request must be corrected; 401 means authentication must be repaired; 403 means permission or feature access must be resolved; 404 requires checking project, IID, and visibility; 409 is a conflict requiring current-state review; 422 requires correcting validation failures; 429 requires waiting according to response guidance. A server error is not success, and uncertain writes are reconciled before repetition. The endpoint reference lists these general REST meanings; it does not assert that every operation returns every code.

## Patterns

Project paths with nested groups require complete URL encoding in the binding. Native project issue IIDs avoid ambiguity between projects. Labels and assignment behavior are not identical to GitHub: new labels may be created, and multiple-assignee support depends on the GitLab tier.

## Known limitations

No bulk issue creation, issue links, merge-request workflow, deletion, project discovery, labels/milestones/releases administration, or business-specific ITSM policy. The supported version is the published GitLab REST API v4; feature availability depends on the target deployment.

## Tools

| Operation | Description | Category |
|---|---|---|
| List issues | Retrieve filtered project issues | Read |
| Read issue | Retrieve one project issue | Read |
| Create issue | Create a project issue | Write |
| Update issue | Change issue content or state | Write |
| List notes | Read issue comments/activity | Read |
| Add note | Publish an issue note | Write |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Project identity and local IID are correct.
- Pagination and visibility limits are included in the result.
- A returned IID or note identifier confirms creation.
- Stored fields and opened/closed state reflect the approved change.
