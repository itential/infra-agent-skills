# openpyxl new value workbook

The openpyxl API creates a new XLSX workbook containing supplied non-formula values.

## Common Sequences

- Create a workbook: **Create workbook → Populate cells → Save workbook → Read saved values**.

### Create workbook

The new-workbook constructor produces one initial worksheet. The active worksheet receives the requested title; additional requested sheets are created explicitly. Success is a workbook whose worksheet names match the intended set.

### Populate cells

The cell-value operation assigns each supplied value at its explicit one-based row and column position. Success is matching in-memory values. Formula strings are outside this scope: the library treats formula expressions as formulas, so untrusted text must not be passed through as a formula. The procedure does not claim the NetClaw renderer's automatic string-sanitization guarantee. Invalid cell values or positions remain library failures.

### Save workbook

The save operation serializes the workbook to an XLSX path. The publisher explicitly warns that an existing file is replaced without warning. Immediately before replacing an existing file, **stop and confirm with the operator before proceeding**. The normal output is a new workbook. A save error is reported without declaring an artifact complete.

### Read saved values

The workbook loader opens the result and the worksheet value iterator returns stored values for comparison with the supplied rows. Success is matching sheet names and values. An invalid OOXML file can be rejected by the loader; that diagnostic is reported rather than treated as an empty workbook. Readback does not calculate formulas or render the workbook.

## Patterns

Accessing otherwise unused cell coordinates creates cells in memory, so the operation binds only the supplied range. The file extension must correspond to the intended format. Loading and resaving an arbitrary existing workbook can lose unsupported shapes; this procedure creates a new file instead.

## Known limitations

Values-only XLSX output. No formulas, macros, templates, existing-workbook preservation, charts, images, visual rendering, or provenance schema. The selected source does not establish a safe automatic transformation for arbitrary untrusted formula-like strings; such inputs require a separate verified text-handling binding.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create workbook | Initialize workbook and sheets | Local SDK |
| Populate cells | Set supplied values | Local SDK |
| Save workbook | Serialize XLSX to file | File write |
| Read saved values | Reopen and inspect values | Local SDK read |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Sheet names and supplied ranges match the request.
- The saved file reopens and contains the expected values.
- No formula, visual-rendering, or provenance guarantee is inferred.
