# Splunk: Run a Search Job and Read Its Results

Sources: Splunk Enterprise REST API Reference 10.2, Search endpoint descriptions; Splunk Search Manual 10.4, export via REST (retrieved 2026-10-26).

## Common Sequences

- **Retrieve events:** Submit search job → Poll job state → Read result pages.
- **Quick small query:** Submit a one-shot search (results come back directly; no job to poll).

## Prerequisites

The platform's management REST interface must be reachable and the account must be allowed to search the target indexes. Splunk Cloud needs REST access enabled through a support request, and free trial accounts cannot use it. Assumption: the search is a retrieval search; Splunk does not label searches as read-only, so inspect the supplied search for commands that write data (for example into a lookup or index) and stop and confirm with the operator before submitting one that does.

## Submit search job

Create a job from the caller's search text with explicit earliest and latest times. Default mode returns a job identifier immediately and the search keeps running in the background. Blocking mode waits for completion before returning the identifier. One-shot mode runs without a persistent job and returns results in the response.
- Success: a job identifier (or, in one-shot mode, results).
- Auth, namespace, or permission errors: access is unresolved; do not report an empty result.

## Poll job state

Read the job's status until it reports done. Its dispatch state moves through queued, parsing, running, finalizing and ends at done or failed; a paused state also exists. Unverified: the full list of dispatch values (the sources read name queued, parsing, running, paused, finalizing, done, failed); report any other value verbatim and treat it as not complete.
- Done flag set and no failure flag: complete.
- Failure or finalized-early flags: report the job as failed or truncated, with its messages.
- Still queued, running, or finalizing: not complete; poll again after a pause.

## Read result pages

Fetch results for the finished job using a page size and a zero-based offset, repeating with the offset advanced until a page returns fewer rows than requested. The default page size is 100; a page size of zero asks for all available rows. Preview results can be returned while a job is unfinished and are not final.
- An empty set while the job is still running is not a zero-match result.
- A bounded page is not the full result set; report the page size and offset used.

## Patterns

- A job identifier proves only that submission worked; completion is a separate check.
- Version 1 search endpoints for parsing, results, and export are off by default from Splunk 9.0.1; use the version 2 forms listed in the endpoints file and do not re-enable the old ones as a fallback.
- Not documented in the sources read: search quotas and rate limits. On HTTP 429 or a busy-search error, back off and honor any `Retry-After` header.

## Known limitations

No search export streaming, parse-only validation, job cancellation, or saved searches. Result row caps and retention depend on the deployment.

## Tools

| Operation | Description | Category |
|---|---|---|
| Submit search job | Start a search from supplied text and time bounds | REST API |
| Poll job state | Read dispatch state and flags | REST API |
| Read result pages | Fetch rows by page size and offset | REST API |

## Verification checklist

- [ ] Search text, index scope, and time bounds are recorded with the result.
- [ ] The job reached done with no failure flag before results were treated as final.
- [ ] Page size, offset, and any preview indicator are reported.
- [ ] Empty or partial output is not reported as no matching events.
