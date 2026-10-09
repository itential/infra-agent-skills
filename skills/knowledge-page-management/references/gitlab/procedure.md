# GitLab project wiki pages

GitLab REST procedures for content in an existing project wiki.

## Common Sequences

- Read content: **List pages → Read page**.
- Create content: **Create page → Read page**.
- Change or remove content: **Read page → Update page or Delete page → Read page or List pages**.

### List pages

The project wiki listing optionally includes page content. Success returns page titles, slugs, formats, and content when requested. The returned slug identifies the page; a display title is not substituted for the slug.

### Read page

The page read uses the URL-encoded slug, including encoded directory separators. An optional version SHA selects a historical version; otherwise the current page is retrieved. Success returns title, slug, format, encoding, and content. Rendered HTML is a separate requested representation and is not the original editable body.

### Create page

The creation operation supplies a title, content, and selected supported format. Markdown is the default; other documented formats are RDoc, AsciiDoc, and Org. Immediately before publishing the page, **stop and confirm with the operator before proceeding**. Success returns the created page with its generated slug and content. The returned slug is used for readback. Submitted text is encoded correctly so special characters and line breaks survive transport. An uncertain create is reconciled against the wiki listing before another publication.

### Update page

The update operation addresses the current slug and supplies at least a title or content change. Immediately before replacing live page content or title, **stop and confirm with the operator before proceeding**. Success returns the updated page, including a potentially changed slug after a title edit. Readback uses that returned slug and checks the submitted content. The API does not document a version precondition for this update, so concurrent-edit protection is unknown; a previous read alone must not be represented as an atomic compare-and-set.

### Delete page

Immediately before deleting the selected wiki page, **stop and confirm with the operator before proceeding**. Success is a 204 result with an empty body; the project page list verifies that the selected slug is no longer present. This operation's documentation does not promise a retention or undo mechanism.

### Handle request failures

The wiki page reference does not enumerate a per-operation error catalogue. GitLab's REST guide gives the general meanings: 400 invalid input; 401 unauthenticated; 403 forbidden; 404 missing/inaccessible; 409 conflict; 422 validation failure; 429 rate-limited; server errors are failures. These require parameter, access, identity, current-state, or response-guided backoff handling as appropriate. An uncertain write is reconciled before repetition; a failed read is not an empty successful page.

## Patterns

A page title can change its slug. URL encoding preserves slashes in nested wiki identifiers. The wiki source's create/update examples request RDoc but show Markdown in the sample response; this procedure follows the documented format parameter and verifies the actual returned format rather than adopting that inconsistent example.

## Known limitations

Project wikis only; no group wiki, attachment upload, comments, page-history enumeration, or guaranteed concurrent-edit control. Deletion is destructive and has no documented undo guarantee in the cited operation.

## Tools

| Operation | Description | Category |
|---|---|---|
| List pages | Enumerate project wiki pages | Read |
| Read page | Retrieve current or specified-version content | Read |
| Create page | Publish a project wiki page | Write |
| Update page | Change wiki title/content | Write |
| Delete page | Remove a wiki page | Delete |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Project and encoded slug identify the requested page.
- Returned title, format, and content match the requested publication or edit.
- A changed slug is retained; deleted pages are absent from the visible list.
- Concurrency and restoration guarantees are not invented.
