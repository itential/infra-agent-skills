# document-artifact-creation: platform references

| Platform | Procedure | Scope | Notes |
|---|---|---|---|
| python-docx | [python_docx/procedure.md](python_docx/procedure.md) | New DOCX with headings, paragraphs, and text tables | Default document only; explicit save and content readback. |
| openpyxl | [openpyxl/procedure.md](openpyxl/procedure.md) | New XLSX with supplied cell values | No formula creation, macros, template editing, or rendering. |
| python-pptx | [python_pptx/procedure.md](python_pptx/procedure.md) | New PPTX with title/content text slides | Built-in layouts only; no visual layout guarantee. |
| pypdf | [pypdf/procedure.md](pypdf/procedure.md) | Inspect and fill existing named PDF text fields into a new PDF | AcroForm text fields only; no flattening, XFA editing, or signatures. |
