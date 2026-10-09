# Splunk saved-search execution

Dispatch an existing saved search with explicit namespace and action behavior.

## Common Sequences

- Execute a saved search: **Resolve definition** → **Dispatch** → **Inspect job** → **Retrieve results**.

### Resolve definition

The saved-search catalogue in the requested owner/application namespace resolves the exact search name and its definition, dispatch parameters and action settings. Names are not assumed unique across namespaces. The reference allows field filtering because the full definition is large and can contain action configuration, including credential-related fields; those are not report content. Missing or inaccessible definitions end this branch.

### Dispatch

Execution consumes search resources and can invoke configured actions: stop and confirm with the operator before proceeding. The selected definition, time overrides and execution identity are explicit. Alert actions remain disabled for this retrieval procedure; enabling delivery requires a separately authorized action. The response search ID identifies the job, not its final outcome. Forcing an additional dispatch while one is running is not automatic.

### Inspect job

Job inspection retains dispatch state, errors and completion flags. Pending/running states remain pending, and failed/canceled/finalized states remain distinct. A completed job is required before the output is reported as final. A missing/expired job cannot be reconstructed by pretending a new dispatch is the original.

### Retrieve results

The final result operation reads rows with a count and zero-based offset. All pages required by the requested scope are collected or the report is labeled partial. The returned preview flag and messages remain visible. Before replacing a local result file: stop and confirm with the operator before proceeding.

## Patterns

Execution identity can be the owner or current user and affects access/quota. Disabling alert actions does not prove that an arbitrary SPL pipeline is free of writes; the definition still requires approval.

## Known limitations

No definition edits, scheduler changes or automatic retries after ambiguous dispatch. The cited reference lists action credential fields in saved-search responses; full definitions should not be dumped into reports.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Resolve definition | List/read a namespaced saved search | Search read |
| Dispatch | Start the selected approved search | Search execution |
| Inspect/retrieve | Track job and read final rows | Search read |

## Verification checklist

- Owner/app/name resolve uniquely.
- Definition and dispatch identity are known.
- Action behavior and execution have an inline gate.
- Native job completion and result pagination are preserved.

## Sources

- [Splunk search endpoint reference 10.2](https://help.splunk.com/en/splunk-enterprise/leverage-rest-apis/rest-api-reference/10.2/search-endpoints/search-endpoint-descriptions). Retrieved 2026-10-09.
- [REST export workflow](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.4/export-search-results/export-data-using-the-splunk-rest-api). Retrieved 2026-10-09.
