# RFC Editor document lookup

Locate and contextualize a published RFC through its publisher.

## Common Sequences

- Number/keyword lookup: **Locate document** → **Check publication context** → **Read section and errata**.

### Locate document

The publisher's search interface or RFC browse list resolves the requested number or topic to a document page. The returned RFC number and title establish the selected document. An unavailable page or search rate limit leaves lookup incomplete; it does not establish that the RFC does not exist. The current search interface is linked in the bindings; its automated query schema is unverified.

### Check publication context

The document page supplies stream, status and update/obsolescence relationships. Publication alone does not make an RFC an Internet Standard. Changes appear in other RFCs because the original publication remains fixed. The result retains relevant successor and update identifiers.

### Read section and errata

The requested section is read in document context. Its identifier and publisher link accompany an original summary. Errata are checked separately: Verified corrections have been reviewed; Reported items are unverified; Rejected items are discarded; Held for Document Update items concern a future revision. TXT/PDF/XML downloads do not incorporate errata. A missing section remains a lookup failure, without a guessed replacement.

## Patterns

The answer distinguishes published wording, later RFC relationships and errata status.

## Known limitations

No claim about vendor implementation conformance follows from document retrieval. Search request parameters and service retry limits are unverified; a rate-limited response follows any returned retry guidance.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Search/browse | Resolve a number or topic using publisher navigation | Document read |
| Read document/errata | Retrieve the selected section and publication context | Document read |

## Verification checklist

- Number, title and requested section match.
- Status and relevant relationships are retained.
- Errata are labeled by their actual status.
- Retrieval failures are explicit.

## Sources

- [RFC Editor publication and reading guide](https://www.rfc-editor.org/series/rfc/). Retrieved 2026-10-09.
- [RFC Editor errata guide](https://www.rfc-editor.org/series/rfc-errata/). Retrieved 2026-10-09.
