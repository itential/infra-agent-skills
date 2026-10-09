# NetClaw indexed corpus query

The NetClaw rag-mcp read surface inventories an existing corpus and retrieves a requested set of matching chunks.

## Common Sequences

- Inspect corpus: **List corpus → Read statistics**.
- Retrieve evidence: **List corpus → Search collection**.

### List corpus

The corpus listing selects documents, snapshots, replicas, or all categories. Success is a successful response envelope containing the requested category collections and their metadata. Snapshot age and replica origin distinguish retained historical material from local documents. A tool failure remains a failed inventory, not an empty corpus. The current implementation supports replicas in addition to the older README's three listed selection values; the binding uses that verified implementation.

### Read statistics

The statistics operation returns counts of ready documents and snapshots, total chunks, disk usage, collection names, configured models, schema version, and retrieval telemetry. Success is a successful envelope with those actual values. Counts describe ready records, not every attempted ingestion. A storage or tool error stops the observation without inferred zero counts.

### Search collection

A single search submits the requested query, collection, result count, and supported metadata filters. The MCP client awaits the completed task result. Success is a successful envelope containing results and the corpus-empty flag. Each returned chunk carries citation metadata and a low-confidence indicator where applicable. An empty corpus and an empty match set are distinct outcomes. A storage-unavailable error means the corpus contents are unknown; a missing-model error requires restoring the server's configured local models before retrying. Other task/tool failures remain errors, not no-match results.

Returned citations, title, section, page, ingestion time, and snapshot capture/age notices remain attached to their chunks. A snapshot is historical evidence; its text does not establish current device state. Low-confidence matches stay visibly flagged rather than silently accepted as answers.

## Patterns

Metadata filters and collection selection constrain the search; the server applies date-range filtering after candidate retrieval. Result ranking is not an exhaustive enumeration of all potentially relevant documents. The server records query telemetry, so this is read-only with respect to indexed content rather than an absence of every local write.

## Known limitations

This procedure does not start or initialize the server: startup can sweep incomplete ingestion state. It does not import documents, alter the corpus, copy federated content, or implement the source skill's autonomous reasoning loop. Exact live task transport handling is delegated to the configured MCP client; a client unable to await completion is unsupported.

## Tools

| Operation | Description | Category |
|---|---|---|
| List corpus | Retrieve document/snapshot/replica inventory | Read |
| Read statistics | Retrieve corpus and retrieval telemetry | Read |
| Search collection | Retrieve one bounded ranked chunk set | Read/task |

Bindings and pinned publisher sources are in [endpoints.md](endpoints.md).

## Verification checklist

- The successful envelope and completed task result are present.
- Collection, query, filters, and returned result count match the request.
- Empty corpus, no matches, low confidence, and tool failure remain distinct.
- Citations, snapshot age, and replica provenance are retained.
