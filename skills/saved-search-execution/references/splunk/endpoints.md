# Splunk saved-search execution: bindings

Use an authenticated, TLS-verifying management client. The prefix `/servicesNS/{owner}/{app}` makes namespace explicit.

| Operation | Binding | Parameters/result |
|---|---|---|
| Catalogue | `GET /servicesNS/{owner}/{app}/saved/searches` | Pagination/filtering, optional `f` field restriction |
| Read selected definition | `GET /servicesNS/{owner}/{app}/saved/searches/{name}` | Definition and action/dispatch configuration |
| Dispatch | `POST /servicesNS/{owner}/{app}/saved/searches/{name}/dispatch` | `trigger_actions=false`; optional `dispatchAs=owner|user`, `dispatch.*`, `args.*`; returns `sid` |
| Job | `GET /services/search/jobs/{sid}` | Dispatch state, completion/failure, messages |
| Results | `GET /services/search/v2/jobs/{sid}/results` | `count`, `offset`, `output_mode=json`; rows and preview flag |

The named dispatch response example contains an SID although its reference's returned-values section says none; the documented response is used. Native job states are reported without converting every terminal state to success.

## Sources

- [Splunk search endpoint reference 10.2](https://help.splunk.com/en/splunk-enterprise/leverage-rest-apis/rest-api-reference/10.2/search-endpoints/search-endpoint-descriptions). Retrieved 2026-10-09.
- [REST export workflow](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.4/export-search-results/export-data-using-the-splunk-rest-api). Retrieved 2026-10-09.
