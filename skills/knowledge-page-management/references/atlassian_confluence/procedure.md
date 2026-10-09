# Confluence Cloud published pages

Confluence Cloud REST v2 procedures for published pages in an existing space.

## Common Sequences

- Read content: **List pages → Read page**.
- Create a page: **Read space → Create page → Read page**.
- Change or remove a page: **Read page → Update page or Trash page → Read page or List pages**.

### Read space

The space read resolves an existing space identifier and its visible details. Success returns the selected space. A 400 requires correcting the identifier; 401 requires authentication repair; 404 requires checking identity and space visibility. Creation requires permission to view the space and create pages there.

### List pages

The page listing uses requested space identifiers, title, or status filters. Success returns visible pages and continuation information. The next link supplied by the response governs pagination; a partial collection is not presented as a complete space inventory. A 400 requires correcting filters; 401 requires authentication repair.

### Read page

The detail operation selects a page identifier and an explicit body format. Success returns its identifier, title, status, space, body, and version number. A 400 requires correcting parameters; 401 requires authentication repair; 404 requires resolving identity and content visibility. A trashed page can be queried by the documented status option when the caller has access.

### Create page

The creation operation supplies the selected space, published status, title, and approved body representation/value. The parent is explicit when placement matters; otherwise the documented space-homepage placement applies. Immediately before publishing the page, **stop and confirm with the operator before proceeding**. Success returns the new page with a 200 result; a detail read verifies its title, content, status, and containing space. A 400 requires correcting content/placement; 401 requires authentication repair; 404 requires resolving the target space or parent; 413 requires reducing the payload. An uncertain creation is reconciled against page listings before another publish operation.

### Update page

The update operation uses the retrieved identifier, approved complete title/body, published status, and current version plus one. Confluence attempts to reconcile published content with an existing draft; significantly diverged draft content can be overwritten. Immediately before replacing published content and possibly affecting its draft, **stop and confirm with the operator before proceeding**. Success returns the page with a 200 result and new version. A detail read verifies content and version. A 409 requires re-reading the latest version and reconciling the proposed edit; 400/401/404 require parameter, authentication, or identity/visibility correction. This procedure does not convert a published page into a draft, which could delete an existing draft.

### Trash page

The deletion operation for a published non-draft page moves it to the trash. Immediately before removing the live page from normal visibility, **stop and confirm with the operator before proceeding**. The operation uses neither permanent purge nor draft deletion. Success is a 204 result; a status-aware detail/list read verifies its trashed state where visible. A 400, 401, or 404 requires parameter, authentication, or identity/visibility review. A normal visibility read returning 404 alone does not distinguish trash from loss of permission.

## Patterns

Version numbers are concurrency controls, not arbitrary labels. Published-page updates can affect draft reconciliation, so a conflict or diverged draft must not be treated as permission to overwrite another author's work. Pagination and permissions limit list completeness.

On a rate-limit response, the server's retry guidance controls backoff. The cited API does not define a fixed safe retry count for mutations; uncertain writes require state reconciliation.

## Known limitations

Published pages only. Permanent purge, draft deletion, draft conversion, restore, cross-space moves, ownership transfer, live docs, comments, CQL search, and attachments are outside this procedure. Trash is recoverable through a separate platform procedure; this skill does not promise retention duration.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read space | Resolve target space | Read |
| List pages | Retrieve visible page candidates | Read |
| Read page | Retrieve content and version | Read |
| Create page | Publish a new page | Write |
| Update page | Replace approved content at next version | Write |
| Trash page | Move a published page to trash | Delete |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Space, page identity, parent, content format, and status match the request.
- Created/updated content and version are confirmed from the page response/readback.
- Trash is distinguished from permanent deletion and inaccessible content.
- Conflicts, draft overwrite risks, pagination, and visibility limitations are reported.
