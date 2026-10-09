# Splunk SPL search and export

Validate and run an explicitly supplied SPL search, retaining job completion and result scope.

## Common Sequences

- Validate only: **Resolve scope** → **Parse**.
- Run and retrieve: **Resolve scope** → **Parse** → **Run search** → **Read completion/results**.
- Stream export: **Resolve scope** → **Parse** → **Stream export**.

### Resolve scope

The supplied search, owner/app namespace, time interval and intended output format define the request. This retrieval procedure covers approved read-only queries only; parsing is not a guarantee that a query has no side effects. A pipeline that writes data or whose effects are unknown is outside this procedure, including when executed through the export operation. Splunk Cloud requires enabled REST access, and free trial accounts do not supply it. Authentication, namespace or permission errors leave access unresolved.

### Parse

The current parser operation returns a semantic map. Parse-only mode prevents expansion through subsearch evaluation, lookups and related search-time expansion. A syntax/parse failure ends execution. Passing this operation establishes parse acceptance only, not the correctness or safety of the search.

### Run search

Search submission supplies the approved read-only SPL and explicit time bounds. Normal asynchronous mode returns a search ID; blocking mode returns an ID after execution, while one-shot mode returns its results directly. A timeout with no confirmed completion is not a successful empty query.

### Read completion/results

For an identified job, inspection preserves native dispatch state, failure flags and messages. Queued/running/finalizing states are not complete. Failed, canceled or prematurely finalized jobs remain failed/incomplete; only the native completed result is described as finished. Final result retrieval uses the result count and offset, preserving preview indicators and diagnostic messages. A bounded page is not the full result set. Before overwriting a local export: stop and confirm with the operator before proceeding.

### Stream export

The current export operation streams the approved read-only search's results using the chosen format. Streaming and transforming searches can produce different preview behavior; previews are not final totals. Large results can use the job-and-paginated-results sequence instead. Interrupted streams remain incomplete, even if some valid rows were received. Before overwriting a local export: stop and confirm with the operator before proceeding. The procedure does not re-enable deprecated search endpoints as a fallback.

## Patterns

The v2 parser and export interfaces use submission operations; their old read-operation forms are deprecated/disabled. Job creation itself retains the documented unversioned endpoint. A search ID and a completed search are different results.

## Known limitations

No arbitrary query construction, data-changing SPL, index deletion, schedule changes or automatic alert actions. Search duration, quotas and index permissions depend on deployment. Publisher examples disable certificate checking and show inline passwords; this procedure requires a TLS-verifying authenticated client instead.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Parse | Validate SPL without expansion | Search validation |
| Run/inspect | Execute and monitor an approved query | Search execution |
| Retrieve/export | Read final rows or a stream | Search read |

## Verification checklist

- Search, namespace and time bounds are retained.
- Parser acceptance is not called execution success.
- Native completion/failure and preview state are preserved.
- Pagination/stream completeness and output format are explicit.

## Sources

- [Splunk search endpoint reference 10.2](https://help.splunk.com/en/splunk-enterprise/leverage-rest-apis/rest-api-reference/10.2/search-endpoints/search-endpoint-descriptions). Retrieved 2026-10-09.
- [REST export workflow](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.4/export-search-results/export-data-using-the-splunk-rest-api). Retrieved 2026-10-09.
