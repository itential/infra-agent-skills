# MemPalace read bindings

Primary publisher source, pinned commit `d439d1e6d01e2680d79fe3f5de5a336722cec779`, inspected 2026-10-09: [schemas](https://github.com/milla-jovovich/mempalace/blob/d439d1e6d01e2680d79fe3f5de5a336722cec779/mempalace/mcp_server/schemas.py), [read handlers](https://github.com/milla-jovovich/mempalace/blob/d439d1e6d01e2680d79fe3f5de5a336722cec779/mempalace/mcp_server/tools_read.py), [protocol](https://github.com/milla-jovovich/mempalace/blob/d439d1e6d01e2680d79fe3f5de5a336722cec779/mempalace/mcp_server/protocol.py), [query implementation](https://github.com/milla-jovovich/mempalace/blob/d439d1e6d01e2680d79fe3f5de5a336722cec779/mempalace/searcher/query.py) and [result assembly](https://github.com/milla-jovovich/mempalace/blob/d439d1e6d01e2680d79fe3f5de5a336722cec779/mempalace/searcher/candidates.py). The portable contract is extracted from publisher implementation, not NetClaw's older tool count.

The existing MCP connection uses JSON-RPC `tools/list` to verify installed schemas, then `tools/call` with `params: {"name":"<tool>","arguments":{...}}`. Tool results are JSON serialized into text content inside `result.content`; decode that content before checking domain success. Installation, transport startup and hub discovery are outside scope.

| Operation | Tool | Arguments |
|---|---|---|
| Read status | `mempalace_status` | `{}` |
| Read taxonomy | `mempalace_get_taxonomy` | `{}` |
| List wings | `mempalace_list_wings` | `{}` |
| List rooms | `mempalace_list_rooms` | Optional `wing` string |
| Search stored text | `mempalace_search` | Required `query` string, at most 250 characters; optional integer `limit` 1–100, default 5; optional `wing`, `room`, `source_file`, `since`, `before` |

This binding keeps the default `candidate_strategy="vector"`, default `max_distance=1.5`, and `cli_compatible=false`. Other search modes are outside scope. A `source_file` filter is an exact full stored path (outer whitespace trimmed), obtained from a result's `source_path`, not its basename-only `source_file`. ISO date/datetime bounds apply to filing time: `since` inclusive, `before` exclusive, compared as stored wall-clock values; records with missing or unparseable filing dates are excluded when bounds are active.

Status returns `total_drawers`, `wings`, `rooms`, `backend` and protocol/dialect content. Organization tools return `wings`, `rooms` (with `wing` scope) or `taxonomy`. Search returns `query`, `filters`, `total_before_filter` and `results`; that count is retrieved candidates, not a complete corpus count. Matches can include `drawer_id`, `text`, `source_path`, `source_file`, `wing`, `room`, filing/authorship/content-date fields, `similarity`, `distance`, and ranking provenance. Vector-disabled fallback may have different ranking metadata; missing values are not fabricated.

Preserved outcome flags include `error`, `partial`, `sqlite_integrity_failed`, `vector_disabled`, `vector_disabled_reason`, `query_sanitized`, `sanitizer`, `index_recovered`, `date_filter_pool_truncated` and `distinct_results_truncated`. A payload error can coexist with an empty `results` array; it is still a failure. `No palace found` is a missing prerequisite, not an instruction to run the accompanying initialization hint.

Protocol failures include `-32601` unknown method/tool, `-32602` missing/unknown/invalid arguments, and `-32000` internal tool error; preflight guards may refuse stale libraries, integrity failures or unavailable backend state with their returned diagnostic. Such failures preserve the exact returned code and sanitized detail; the procedure does not execute repair hints. The search handler's own recognized transient-index retry waits two seconds and occurs at most once; the caller does not add an unbounded outer retry loop.
