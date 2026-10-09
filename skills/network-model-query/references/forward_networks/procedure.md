# Forward Networks stored-model queries

Read network/snapshot inventory, device evidence, library NQE results and modeled paths using Forward Networks' MCP server 3.0.0.

## Common Sequences

- Model inventory: **Select network and snapshot** → **Read devices**.
- Library analysis: **Select network and snapshot** → **Select library query** → **Run library query**.
- Modeled packet path: **Select network and snapshot** → **Search modeled paths**.

### Select network and snapshot

The network list identifies the intended network; its snapshot list or latest-snapshot read identifies a stored model. Success is the exact network and snapshot identifiers with collection/processing metadata where returned. List reads have bounded output and report their total and remaining items; offset advances until the requested selection is found or the collection is exhausted. The selected identifier is supplied to later operations, avoiding a moving latest-snapshot target.

### Read devices

The device collection returns matching device records and a total count. Success is a returned page tied to the network/snapshot, including any collection or processing errors on devices. Offset and limit control pages. Incomplete collection evidence remains part of the result; a listed device does not prove its configuration was collected and processed without error.

### Select library query

The library listing supplies a query identifier and path, optionally restricted to a directory. Success is a returned executable query identifier matching the requested analysis. A label, semantic search suggestion or library path alone is not substituted for the query identifier.

### Run library query

The selected library query runs with its documented parameter values against the selected model. A returned native result includes items and snapshot identity; the publisher can also return a warning instead of executing a request whose output is unbounded or too large. That warning is not a query result.

For unfiltered/unordered complete-result requests, the publisher's batch mode fetches pages and returns a total plus a preview, optionally storing the full data in local MCP memory. A preview is not the full result. The batch branch does not carry sorting/filter options into its API requests, so those options are not combined with this mode here. The current single-page cache key omits pagination/options; repeated pages with different options can reuse earlier cached evidence. Complete pagination therefore requires a separately verified cache-disabled client configuration or native API contract; it is not assumed here.

Outdated module or runtime-code errors leave the query failed. A size-limit error may invoke the publisher's batch fallback; the returned summary/preview and storage outcome must remain explicit. Service/authentication failures remain unavailable evidence.

### Search modeled paths

A path request supplies a destination IP/prefix and either a source device or source IP, plus the required protocol/port constraints. Success is the returned path evidence with forwarding/security outcomes, hops, total-hit metadata, return-path evidence and any timeout or unrecognized-value information. A timed-out or bounded search is incomplete, not proof that no path exists. Invalid destinations or missing source/destination fields fail validation. A missing processed snapshot leaves the analysis unavailable.

## Patterns

The MCP server can write local caches, query-result memory and tracking data while reading the Forward platform. The returned evidence may be a compact result or a summary/preview; those representations have different completeness. Modeled paths are not live packet tests.

## Known limitations

No network/snapshot/location mutation, collection triggering, arbitrary NQE source execution, local memory administration, semantic-index rebuilding or custom policy verdict is included. This focused reference does not claim all 54 MCP tools. Pagination/cache and batch-option defects above are explicit limitations of the inspected publisher implementation.

Source: Forward Networks [MCP 3.0.0 publisher repository](https://github.com/forwardnetworks/forward-mcp/tree/f9f6f9e8f38b45c804d845ead949a43f7d2dc566), especially the tool schemas, service handlers and API client, retrieved 2026-10-09. Bindings are in [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Select network and snapshot | Read model identity and timing | Read |
| Read devices | Read device records and collection errors | Read |
| Select library query | Identify an existing library query | Read |
| Run library query | Query the selected stored model | Analyze |
| Search modeled paths | Retrieve modeled forwarding/security paths | Analyze |

## Verification checklist

- Network and snapshot identifiers are pinned and retained.
- Native collection/processing errors and timing remain visible.
- Query warnings, previews, cached pages and complete datasets are distinguished.
- Path timeout, unknown values and search bounds qualify conclusions.
