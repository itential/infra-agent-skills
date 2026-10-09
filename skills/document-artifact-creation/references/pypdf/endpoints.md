# pypdf form bindings

Official source: [Interactions with PDF forms](https://pypdf.readthedocs.io/en/stable/user/forms.html), documentation version 6.20.0, retrieved 2026-10-09.

Local SDK inputs are `input_path`, approved text-field `field_values`, and `output_path`. Names/types are resolved before filling; only inspected `/Tx` text fields enter this binding.

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader(input_path)
fields = reader.get_fields()
writer = PdfWriter()
writer.append(reader)
for name, value in field_values.items():
    field = fields[name]
    for source_page in reader.get_pages_showing_field(field):
        writer.update_page_form_field_values(
            writer.pages[source_page.page_number],
            {name: value},
            auto_regenerate=False,
        )
writer.write(output_path)
check = PdfReader(output_path)
stored_values = check.get_form_text_fields()
```

The field dictionary exposes `/FT` (type), `/T` (partial name), and `/V` (value); fully qualified hierarchical names join their components with dots. `/XFA` content can override ordinary page content, so it is outside this binding. The library's `flatten` option and removal of `/Widget` annotations are deliberately unused; the form remains a form.
