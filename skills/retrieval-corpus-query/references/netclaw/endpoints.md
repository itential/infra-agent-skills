# NetClaw RAG query bindings

Primary publisher sources: [rag-mcp README](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/rag-mcp/README.md), [registered tools and implementation](https://github.com/automateyournetwork/netclaw/blob/95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692/mcp-servers/rag-mcp/rag_mcp_server.py), pinned commit `95bb17e27a6a2538fcb0168d0b1d0ab5bbe34692`, inspected 2026-10-09.

Transport is the already configured stdio MCP server. No credential or HTTP base is needed. The client binds these registered tool names using their actual input schema and supports the publisher's task-enabled search registration.

| Operation | Tool | Arguments | Result |
|---|---|---|---|
| List corpus | `rag_list` | `kind=documents\|snapshots\|replicas\|all` (default `all`) | Category collections under `data` |
| Read statistics | `rag_stats` | No arguments | `data.document_count`, `snapshot_count`, `total_chunks`, `disk_usage_bytes`, `collections`, models, `schema_version`, `telemetry` |
| Search collection | `rag_search` | Required `query`; `k=5`, `collection=documents` defaults; optional `filters`, `round`, `sub_query_id` | Completed `data.results`, `corpus_empty`, `collection`, `latency_ms` |

Filters are `doc_type`, `document_id`, `title`, `ingested_after`, `ingested_before`. Results include `chunk_text`, `score`, `chunk_id`, `title`, `doc_type`, `section`, `page`, `ingest_ts`, `low_confidence`, and `citation`; snapshots additionally carry `capture_ts`, `age_human`, and `staleness_notice` where available.

The completed envelope is `{"success":true,"data":{...},"error":null}` or `{"success":false,"data":null,"error":{"code":"<code>","message":"<detail>"}}`. Query-specific implemented error names include `STORAGE_UNAVAILABLE` and `MODELS_NOT_CACHED`. Other uncaught storage/task failures can arrive as MCP tool errors; no complete application error catalogue is asserted.

The README's list selector omits `replicas`; the pinned registered function includes it. Native returned fields govern output. The search records local retrieval telemetry, but these three operations do not invoke the mutation GAIT logging helper.
