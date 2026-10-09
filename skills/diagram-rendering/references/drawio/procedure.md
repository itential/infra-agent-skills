# draw.io diagram opening and page access

Use the publisher MCP tool server to open supplied diagram source or access a local diagram page.

## Common Sequences

- Open a diagram: **Select source** → **Open** → **Verify**.
- Change a local page: **Inspect pages** → **Replace page** → **Inspect pages**.

### Select source

The tool server accepts native diagram XML, CSV or Mermaid source. The requested language selects the corresponding operation in the bindings. A local page operation instead requires an existing file ending in `.drawio` or `.xml`.

### Open

The selected opening operation receives the supplied source and returns a diagram URL. Lightbox mode selects a read-only viewer; otherwise the browser opens the editor. A returned URL is an opening result, not proof that an image was exported or a local file saved. Invalid source or a tool failure remains a rendering failure; no complete error catalogue is published in the cited README.

### Verify

The opened editor/viewer displays the supplied diagram. A browser load failure leaves viewing unverified even when URL generation succeeded. Image export and construction of a network model from raw telemetry are outside this procedure.

### Inspect pages

Page listing returns each page's zero-based index, identifier, name and approximate size. Reading a selected page returns its graph-model XML. Selection uses the returned index, exact name or ID, not an assumed one-based page number.

### Replace page

Local page replacement changes the selected file: stop and confirm with the operator before proceeding. The replacement is one graph-model XML element; the publisher tool keeps other pages intact. Reading the same page again confirms the resulting content. A missing file/page or rejected XML ends the operation; the documentation supplies no universal recovery rule.

## Patterns

Opening tools encode diagram content in the URL fragment. Optional layout/routing helpers can fetch runtime code; the tool server is not a blanket guarantee of no network access. Page operations transparently handle compressed pages.

## Known limitations

Only the publisher tool server is covered. The hosted MCP App server is a different interface. Native file export to PNG/SVG/PDF and NetClaw-specific auto-deletion are not included.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Select/open | Open supplied XML, CSV or Mermaid | Rendering |
| Inspect pages | List/read local diagram pages | Local file read |
| Replace page | Replace one selected page | Local file write |

## Verification checklist

- Input language and requested viewer mode match.
- URL generation and browser rendering are distinguished.
- Local replacements target a resolved page and have an explicit gate.
- No saved image is claimed without an export result.

## Sources

- [Publisher tool-server README](https://github.com/jgraph/drawio-mcp/blob/main/mcp-tool-server/README.md). Retrieved 2026-10-09.
