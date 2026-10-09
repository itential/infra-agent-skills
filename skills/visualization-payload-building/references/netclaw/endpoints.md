# NetClaw Canvas envelope construction: bindings

Local JavaScript bindings in `lib/a2ui-renderer.js`; no network authentication is involved.

| Operation | Binding | Result |
|---|---|---|
| Build envelope | `buildA2UIEnvelope({component, title, dataSources, scope, warnings, content})` | `a2ui.version="1.0"`, `type="canvas"`, `component`, and `props` |
| Source metadata | `createDataSourceRef({server, tool, status, latencyMs})` | Status is `ok`, `partial`, or `unavailable`; absent status defaults to `ok`, so supply observed status explicitly |
| Warning | `createWarning(level, message, source)` | Supplied warning metadata |
| Error envelope | `buildErrorCard({title, message, suggestion})` | `component="error-card"`, message/suggestion/timestamp |
| Source status | `determineStatus(dataSources, content)` | `failed`, `degraded`, `complete`; `content` is not inspected |

Registered components: `topology-map`, `dashboard-panel`, `alert-card`, `change-timeline`, `diff-view`, `path-trace`, `health-scorecard`. Registration alone supplies a default title, not a content validator.


## Sources

- [NetClaw Canvas envelope implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/canvas-network-viz/lib/a2ui-renderer.js). Retrieved 2026-10-09.
- [Local audit implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/workspace/skills/canvas-network-viz/lib/gait-logger.js). Retrieved 2026-10-09.
