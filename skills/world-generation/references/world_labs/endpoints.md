# World Labs text-to-world generation: bindings

API base: `https://api.worldlabs.ai/marble/v1`. Existing secret is sent in `WLT-Api-Key`; JSON requests use `Content-Type: application/json`.

| Operation | Binding | Request/result |
|---|---|---|
| Generate | `POST /worlds:generate` | `world_prompt: {type: "text", text_prompt: approved_text}`, explicit `model`, optional `display_name` (max64 characters) |
| Track | `GET /operations/{operation_id}` | `operation_id`, `done`, `error`, `metadata`, `response`, optional timestamps |
| Read | `GET /worlds/{world_id}` | Generated world, viewer/assets metadata |

Retrieved schema model names: `marble-1.0-draft`, `marble-1.0`, `marble-1.1`, `marble-1.1-plus`; verify against the installed/current schema before use. Legacy names are deprecated. Default permissions are private; this procedure does not set sharing fields.

Error handling:400 invalid/policy-rejected request;402 insufficient API credits;404 nonexistent or inaccessible resource;422 field-specific `detail[]`;429 rejected start with backoff/Retry-After;500 server failure. Authentication rejection does not disclose the key. Terminal operation errors use `error.code` and `error.message`. A returned `request_id` is a support trace identifier, not a queryable operation.

## Sources

- [World generation API](https://docs.worldlabs.ai/api/reference/worlds/generate). Retrieved 2026-10-09.
- [Operation API](https://docs.worldlabs.ai/api/reference/operations/get). Retrieved 2026-10-09.
- [World retrieval API](https://docs.worldlabs.ai/api/reference/worlds/get). Retrieved 2026-10-09.
- [Error behavior](https://docs.worldlabs.ai/api/errors). Retrieved 2026-10-09.
- [Generation rate-limit behavior](https://docs.worldlabs.ai/api/rate-limits). Retrieved 2026-10-09.
