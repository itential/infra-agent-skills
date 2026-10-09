---
name: document-artifact-creation
description: >-
  Create a local document artifact from supplied content or fill an existing PDF form into a new file. Use for basic new Word text/table documents, Excel value workbooks, PowerPoint text slides, or named PDF text-form fields. Covers python-docx, openpyxl, python-pptx, and pypdf. Assumes a local Python environment with the selected library installed and an authorized output path.
---

# Document artifact creation

Create a local document artifact from supplied content or fill an existing PDF form into a new file.

## When to use this skill

Use for basic new Word text/table documents, Excel value workbooks, PowerPoint text slides, or named PDF text-form fields.

## Universal concepts

No common wire protocol is implied by this capability. Content population and saving are separate operations. A saved file does not prove visual correctness or establish the truth of its supplied content.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No report-writing judgment, automatic provenance tagging, source-data collection, NetClaw runtime, templates, formulas, charts, image layout, delivery, or production system updates. Each library reference defines its limited format support.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes a local Python environment with the selected library installed and an authorized output path. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
