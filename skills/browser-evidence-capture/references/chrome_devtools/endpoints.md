# Chrome DevTools MCP bindings

Official sources: [Tool reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md), [Publisher README](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/README.md), [Configuration](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md), [Troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md), retrieved 2026-10-09.

An already configured MCP client calls the official `chrome-devtools-mcp` server. The installed server's tool schemas must match these current documented parameters. No site credentials are supplied by this procedure.

| Operation | Tool binding | Arguments |
|---|---|---|
| List pages | `list_pages` | `{}` |
| Open inspection page | `new_page` | `url` required; optional `isolatedContext`, `background`, `timeout` |
| Wait for expected text | `wait_for` | Required `pageId`, nonempty `text` array; optional `timeout` milliseconds |
| Capture accessibility text | `take_snapshot` | Required `pageId`; optional `verbose`, `filePath` |
| Capture screenshot | `take_screenshot` | Required `pageId`; optional `filePath`, `format=png\|jpeg\|webp`, `fullPage` OR `uid`, JPEG/WebP `quality` |
| List console | `list_console_messages` | Required `pageId`; optional `pageIdx` (zero-based), `pageSize`, `types`, `includePreservedMessages`, `includeStackTraces` |
| Read console detail | `get_console_message` | Required `pageId`, `msgid` from listing |
| List network | `list_network_requests` | Required `pageId`; optional `pageIdx`, `pageSize`, `resourceTypes`, `includePreservedRequests` |
| Read request detail | `get_network_request` | Required `pageId`; explicit `reqid` from listing; optional `requestFilePath`, `responseFilePath` |
| Snapshot audit | `lighthouse_audit` | Required `pageId`; `mode=snapshot`; optional `device=desktop\|mobile`, `outputDirPath` |
| Close inspection page | `close_page` | Required `pageId` |

The request detail can include `Cookie` and `Set-Cookie`; those are sensitive evidence, not ordinary report fields. Preserved console/network history spans the previous three navigations where enabled. A timeout value of zero selects the tool default rather than an unlimited wait.

Publisher configuration includes `--isolated`, `--headless`, `--no-usage-statistics`, and `--no-performance-crux`. `new_page.isolatedContext` is the documented per-context separation mechanism; it is not an assertion that a shared persistent profile became isolated automatically. Initial installation, telemetry preference changes, and remote-debugging setup are outside this sequence.
