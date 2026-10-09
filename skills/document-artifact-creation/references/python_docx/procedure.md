# python-docx new document

The python-docx API creates a DOCX containing supplied headings, paragraphs, and text tables.

## Common Sequences

- Create a document: **Create document → Add content → Save document → Read saved content**.

### Create document

The empty-document constructor loads the library's built-in starting document. Success is a document object ready for content. A library/load exception stops creation with its actual diagnostic.

### Add content

Heading creation selects the requested level, with level zero representing a title. Paragraph creation appends supplied text. A table uses explicit row/column counts and zero-based cell coordinates; each requested cell receives its supplied text. Success is the in-memory paragraph/table content matching those inputs. Invalid dimensions or unsupported values are reported as library errors without substituting content.

### Save document

The save operation writes the document to the selected DOCX path. The publisher warns that saving over an existing path replaces it without a prompt. Immediately before replacing any existing file, **stop and confirm with the operator before proceeding**. The intended normal outcome is a new file. A save exception means no successful artifact is claimed.

### Read saved content

Opening the written document and reading its paragraph text and table cells verifies that the expected supplied content survived serialization. Success is matching content in the reopened file. A load error or content mismatch is reported as failed verification; no visual quality conclusion follows from text readback alone.

## Patterns

Setting content in memory does not persist it; the save operation finishes the sequence. Table indices begin at zero. Text/table readback uses the same document model as population.

## Known limitations

DOCX only; no older binary DOC files, existing template editing, images, footnotes, report composition, or automatic source attribution. Detailed exception classes for every invalid content case are not specified by the quickstart; actual library errors are preserved. The older document tutorial contains outdated feature statements; this scope relies only on its constructor/save behavior and the current API's content accessors.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create document | Initialize a new document | Local SDK |
| Add content | Populate approved text and tables | Local SDK |
| Save document | Serialize DOCX to file | File write |
| Read saved content | Reopen paragraphs/table cells | Local SDK read |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- The output path identifies the requested new DOCX.
- Reopened paragraph/table content matches the supplied values.
- Save/load failures and lack of visual rendering verification remain explicit.
