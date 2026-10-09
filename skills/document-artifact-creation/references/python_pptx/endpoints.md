# python-pptx bindings

Official sources: [Getting started](https://python-pptx.readthedocs.io/en/latest/user/quickstart.html), [Working with presentations](https://python-pptx.readthedocs.io/en/latest/user/presentations.html), documentation version 1.0.0, retrieved 2026-10-09.

This is a local SDK. `slides` contains supplied `title` and nonempty `paragraphs` arrays; `output_path` is the selected new-file destination or a destination approved at the overwrite gate.

```python
from pptx import Presentation

presentation = Presentation()
for content in slides:
    slide = presentation.slides.add_slide(presentation.slide_layouts[1])
    slide.shapes.title.text = content['title']
    frame = slide.placeholders[1].text_frame
    frame.text = content['paragraphs'][0]
    for text in content['paragraphs'][1:]:
        frame.add_paragraph().text = text
presentation.save(output_path)
check = Presentation(output_path)
stored_text = [
    [shape.text for shape in slide.shapes if shape.has_text_frame]
    for slide in check.slides
]
```

Layout index 1 and body placeholder 1 follow the publisher's built-in title/content example. They are not asserted for arbitrary supplied templates. Exact layout and typography decisions are outside this operation.
