# Kroki diagram rendering: bindings

Paths are relative to the approved Kroki service base URL.

| Operation | Literal binding | Payload/result |
|---|---|---|
| JSON render | `POST /` with `Content-Type: application/json` | `diagram_source`, `diagram_type`, `output_format`; optional `diagram_options` object; image response |
| Text render | `POST /{diagram_type}/{output_format}` with `Content-Type: text/plain` | Source text; image response |

PlantUML's `no-metadata` option is a flag. Kroki Mermaid options cannot override `maxTextSize`, `securityLevel`, `secure` or `startOnLoad`; these restrictions must not be bypassed. No public service URL is imposed by this skill.

## Sources

- [Kroki usage](https://docs.kroki.io/kroki/setup/usage/). Retrieved 2026-10-09.
- [Diagram options](https://docs.kroki.io/kroki/setup/diagram-options/). Retrieved 2026-10-09.
