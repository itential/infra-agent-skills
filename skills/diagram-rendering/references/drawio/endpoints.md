# draw.io diagram opening and page access: bindings

Publisher `@drawio/mcp` tool-server bindings; configured instance selection is an installation concern.

| Operation | Tool and arguments | Result |
|---|---|---|
| Open XML | `open_drawio_xml(content, lightbox?, dark?)` | Editor/viewer URL |
| Open CSV | `open_drawio_csv(content, lightbox?, dark?)` | Editor/viewer URL |
| Open Mermaid | `open_drawio_mermaid(content, lightbox?, dark?)` | Editor/viewer URL |
| List pages | `list_pages(path)` | Page descriptors |
| Read page | `get_page(path, page)` | `mxGraphModel` XML |
| Replace page | `set_page(path, page, content)` | Updated local page |

`lightbox` defaults to false. `dark` accepts `auto`, `true` or `false` strings. `page` can be a zero-based index, exact name or returned ID. The default hosted editor is `https://app.diagrams.net/`; a self-hosted installation can configure `DRAWIO_BASE_URL`.

## Sources

- [Publisher tool-server README](https://github.com/jgraph/drawio-mcp/blob/main/mcp-tool-server/README.md). Retrieved 2026-10-09.
