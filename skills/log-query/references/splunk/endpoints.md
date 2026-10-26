# Splunk: Search Job Wiring

Sources: Splunk Enterprise REST API Reference 10.2, Search endpoint descriptions; Splunk Search Manual 10.4, export via REST (retrieved 2026-10-26).

The base is the instance's management service address (placeholder `{splunk_mgmt}`). Authentication and TLS verification come from the existing client. Owner and app scoping use the `/servicesNS/{owner}/{app}` prefix in place of `/services`.

| Operation | Method and path | Notes |
|---|---|---|
| Submit search job | `POST {splunk_mgmt}/services/search/jobs` | Form fields `search`, `earliest_time`, `latest_time`, `exec_mode` (`normal`, `blocking`, `oneshot`), `output_mode`. Returns a search ID. |
| Poll job state | `GET {splunk_mgmt}/services/search/jobs/{sid}` | Fields `dispatchState`, `isDone`, `isFailed`, `isFinalized`, `messages`. |
| Read result pages | `GET {splunk_mgmt}/services/search/v2/jobs/{sid}/results` | Query `count` (default 100, `0` = all), `offset`, `f`, `output_mode`, `preview`. |

Output formats documented for REST retrieval: `atom`, `csv`, `json`, `json_cols`, `json_rows`, `raw`, `xml`.

Unverified: the exact error body shape and the HTTP status for a job that failed. Assumption: the search text starts with a generating command or the `search` keyword as in the platform's documentation examples.
