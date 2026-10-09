# Splunk SPL search and export: bindings

An authenticated, TLS-verifying client targets the configured Splunk management service. Paths below use `/services`; owner/app scoping uses the documented `/servicesNS/{owner}/{app}` prefix instead. Path components are encoded as components, not concatenated unescaped.

| Operation | Literal binding | Parameters/result |
|---|---|---|
| Parse | `POST /services/search/v2/parser` | Form `q`, `parse_only=true`, `output_mode=json`; semantic map or parse failure |
| Submit | `POST /services/search/jobs` | `search`, `earliest_time`, `latest_time`, `exec_mode=normal|blocking|oneshot`, `output_mode` |
| Inspect | `GET /services/search/jobs/{sid}` | `dispatchState`, `isDone`, `isFailed`, `isFinalized`, `messages`, `resultCount` |
| Results | `GET /services/search/v2/jobs/{sid}/results` | `count`, zero-based `offset`, optional `f`, `output_mode`; `preview`, `results`, `messages` for JSON |
| Stream | `POST /services/search/v2/jobs/export` | `search`, time bounds, `output_mode` |

Result formats include `csv`, `json`, `json_cols`, `json_rows`, `raw`, `xml`, `atom`. A result `count=0` requests all available rows; explicit bounded pagination can instead limit each read. Native dispatch values include `QUEUED`, `PARSING`, `RUNNING`, `FINALIZING`, `DONE`, `PAUSE`, `INTERNAL_CANCEL`, `USER_CANCEL`, `BAD_INPUT_CANCEL`, `QUIT`, `FAILED`. No generic retry on failed query submission is assumed.

## Sources

- [Splunk search endpoint reference 10.2](https://help.splunk.com/en/splunk-enterprise/leverage-rest-apis/rest-api-reference/10.2/search-endpoints/search-endpoint-descriptions). Retrieved 2026-10-09.
- [REST export workflow](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.4/export-search-results/export-data-using-the-splunk-rest-api). Retrieved 2026-10-09.
