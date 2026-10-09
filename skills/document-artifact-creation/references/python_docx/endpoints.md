# python-docx bindings

Official sources: [Quickstart](https://python-docx.readthedocs.io/en/latest/user/quickstart.html), [Working with documents](https://python-docx.readthedocs.io/en/latest/user/documents.html), [Document API](https://python-docx.readthedocs.io/en/latest/api/document.html), documentation version 1.2.0, retrieved 2026-10-09.

This is a local SDK, not REST. Input strings and rectangular table rows are already supplied; `output_path` is the operator-selected destination subject to the procedure's overwrite gate.

```python
from docx import Document

document = Document()
document.add_heading(title_text, level=0)
for text in paragraph_texts:
    document.add_paragraph(text)
if table_rows:
    table = document.add_table(rows=len(table_rows), cols=len(table_rows[0]))
    for row_index, row in enumerate(table_rows):
        for column_index, text in enumerate(row):
            table.cell(row_index, column_index).text = text
document.save(output_path)
check = Document(output_path)
paragraph_values = [paragraph.text for paragraph in check.paragraphs]
table_values = [
    [[cell.text for cell in row.cells] for row in table.rows]
    for table in check.tables
]
```

`title_text`, `paragraph_texts`, `table_rows`, and `output_path` are input variables, not values generated from inferred network state. The publisher quickstart's tuple-based table sample subsequently uses attribute access on those tuples; the binding above uses explicit indexed iteration instead of reproducing that inconsistent example.
