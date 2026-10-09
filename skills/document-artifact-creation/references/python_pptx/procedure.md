# python-pptx text presentation

The python-pptx API creates a new presentation from supplied title and bullet text.

## Common Sequences

- Create a presentation: **Create presentation → Add text slides → Save presentation → Read saved text**.

### Create presentation

The default constructor creates a presentation from the library's built-in empty-slide starting file. Success is a presentation with available built-in layouts. The library's default template is a presentation file, not an arbitrary customer template contract.

### Add text slides

A title-and-content layout is selected from the built-in layout collection for each supplied slide. Its title and body receive the approved text. The first body paragraph is populated before subsequent paragraphs are appended. Success is the intended slide order and text in the in-memory model. Setting an entire shape/text-frame text value replaces its previous paragraphs; the binding avoids doing that after appending the requested paragraphs. Missing layouts/placeholders or library exceptions stop content population.

### Save presentation

The save operation writes the PPTX path. Saving over an existing path overwrites it without a prompt. Immediately before replacing an existing file, **stop and confirm with the operator before proceeding**. The intended normal outcome is a new presentation. A save failure is reported without declaring a completed deck.

### Read saved text

Opening the saved presentation and iterating the text-bearing shapes returns each slide's stored text. Success is the expected slide order and supplied text. Load failures or mismatches are failed verification. The API text model does not establish that text fits visually or that the deck is presentation-ready.

## Patterns

Not every shape contains text; the documented text-frame indicator distinguishes text-bearing shapes. Default-layout indices apply to the built-in starting presentation and are not portable to arbitrary templates.

## Known limitations

Basic PPTX text slides only. No legacy PPT, customer template support, figures/images, notes, charts, slide design, source attribution, or visual rendering. The older document guide's broad unsupported-feature statements are not treated as current API limitations beyond this deliberately narrow scope.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create presentation | Initialize built-in presentation | Local SDK |
| Add text slides | Populate supplied titles and text | Local SDK |
| Save presentation | Serialize PPTX | File write |
| Read saved text | Reopen text-bearing shapes | Local SDK read |

Bindings and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- The selected default layout supplies the expected placeholders.
- Saved slide count/order and text match supplied inputs.
- Save/load failures and visual-layout limitations are explicit.
