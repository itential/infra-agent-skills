# pypdf named text-form fill

The pypdf API reads existing AcroForm field names and fills approved text values into a new PDF.

## Common Sequences

- Fill a form: **Read form fields → Copy form structure → Fill named fields → Save new PDF → Read saved fields**.

### Read form fields

The reader opens the supplied PDF and retrieves its field dictionary. Success identifies actual field names/types and values. Hierarchical fields require fully qualified names. The page-widget listing is not interchangeable with the field dictionary, especially for grouped controls. If no editable text fields are returned, or the document relies on XFA, this text-form sequence is unsupported. A reader error stops processing with its actual diagnostic.

### Copy form structure

Appending the source reader to a new writer preserves the form structure for filling. Success is a writer containing the source pages and fields. Copying pages alone is insufficient because fields are stored outside the page collection. Repairing malformed field hierarchies is outside this scope.

### Fill named fields

The field update uses only names returned by inspection and approved values for text fields on their actual pages. Appearance regeneration is disabled as recommended by the publisher, avoiding its legacy default that can provoke a viewer save prompt. Success updates the requested field values in the writer. Unmatched names and unpopulated fields remain explicit; they are not supplied with guessed values. XFA overrides, signatures, and button/choice behavior are outside this text-only operation.

### Save new PDF

The writer serializes the filled form to the selected new PDF path. Immediately before replacing an existing output or the original PDF, **stop and confirm with the operator before proceeding**. The ordinary outcome uses a separate output. A write exception does not establish a completed filled form.

### Read saved fields

The result is reopened and its form text values are read. Success is the approved values at the intended fully qualified names. Missing/mismatched fields are reported as incomplete. This inspection verifies stored values; it does not promise identical appearances across PDF viewers.

## Patterns

Appending the document preserves form-level structures that page copying can omit. A field can have widgets on multiple pages. The publisher's field-page lookup identifies those pages for the update sequence.

## Known limitations

AcroForm text fields only, with the existing form retained. No XFA editing, signatures, flattening, field creation, malformed-form repair, or automatic source/provenance appendix. No universal stable exception catalogue is supplied in the cited form guide; actual errors remain authoritative.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read form fields | Inspect names/types and field pages | Local SDK read |
| Copy form structure | Append source into a new writer | Local SDK |
| Fill named fields | Set supplied text values | Local SDK |
| Save new PDF | Write filled form | File write |
| Read saved fields | Reopen stored text values | Local SDK read |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Every submitted name came from field inspection and is a text field.
- Field structures and intended pages survived the copy.
- Saved values match the approved mapping; unmatched/unfilled fields are reported.
- The original and output paths are distinct unless overwrite was explicitly confirmed.
