# openpyxl bindings

Official sources: [Tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html), [Simple usage](https://openpyxl.readthedocs.io/en/stable/usage.html), documentation line 3.1, retrieved 2026-10-09. Both sources were verified. The usage guide distinguishes stored formula expressions from evaluation; this capability excludes formula creation and formula-like untrusted text.

This is a local SDK. `sheet_name`, rectangular `rows`, and `output_path` are approved inputs. Formula-like text is unsupported; it is not silently sanitized or passed through.

```python
from openpyxl import Workbook, load_workbook

workbook = Workbook()
worksheet = workbook.active
worksheet.title = sheet_name
for row_index, values in enumerate(rows, start=1):
    for column_index, value in enumerate(values, start=1):
        worksheet.cell(row=row_index, column=column_index, value=value)
workbook.save(output_path)
check = load_workbook(output_path)
stored_names = check.sheetnames
stored_values = list(check[sheet_name].values)
```

The tutorial documents that `data_only` changes how formula cells are loaded: formula expressions versus the last stored calculation result. It does not provide formula evaluation. This binding keeps the ordinary loader behavior and excludes formula creation.
