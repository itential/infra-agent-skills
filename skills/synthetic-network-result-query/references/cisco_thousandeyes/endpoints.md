# ThousandEyes network-result REST bindings

Sources: Cisco API v7.0.110 [network](https://developer.cisco.com/docs/thousandeyes/get-network-test-results/), [path summary](https://developer.cisco.com/docs/thousandeyes/get-path-visualization-network-test-results/), [path detail](https://developer.cisco.com/docs/thousandeyes/get-path-visualization-test-results-by-agent-and-round/), retrieved 2026-10-09.

Base: `https://api.thousandeyes.com/v7`; authentication: `Authorization: Bearer <token>`.

| Operation | Binding | Parameters |
|---|---|---|
| Network results | `GET /test-results/{testId}/network` | String `testId`; optional `aid`, time range, `direction` = to-target/from-target/bidirectional (default to-target) |
| Path summary | `GET /test-results/{testId}/path-vis` | String `testId`; optional `aid`, time range, `direction` = to-target/from-target; omission returns both where supported |
| Path detail | `GET /test-results/{testId}/path-vis/agent/{agentId}/round/{roundId}` | String identifiers; optional `aid`, `direction` = to-target/from-target |

Time range: `window` must contain a number and unit `s`, `m`, `h`, `d` or `w`, for example `30m`. Alternatively `startDate` and `endDate` use UTC ISO8601 timestamps with seconds; `endDate` defaults to the request time. They cannot be combined with `window`. Native `window` is not an untyped seconds argument.

Paged results have `results`, `test`, `startDate`, `endDate`, `_links`; continuation follows `_links.next` rather than authoring a `cursor`. The detail result has `results`, `test`, `_links`.

Network result examples of schema fields: `agent`, `roundId`, `date`, `startTime`, `endTime`, `server`, `serverIp`, `direction`, `avgLatency`, `minLatency`, `maxLatency`, `jitter`, `loss`, `healthScore`, `errorDetails`. `loss` is a percentage and absent when unavailable. `healthScore` normally lies from 0–1; negative values are error codes and `-1` means insufficient data. The cited latency field descriptions do not state a unit, so this binding does not invent one.

Path summary `pathTraces[]` contains `pathId`, `numberOfHops`, `responseTime` (destination RTT in milliseconds), `mss`, `pathMtu`, `ipAddress`. Path detail `pathTraces[]` adds `hops[]` with `hop`, `ipAddress`, `prefix`, optional `rdns`, `network`, `location`, `mpls`, and `responseTime` (hop RTT in milliseconds). No per-hop loss field is defined by this detail schema.

Responses: 200 success; 400 invalid request; 401 unauthenticated; 403 insufficient permission; 404 missing resource; 429 organizational limit exhausted; 500 server failure; 502 gateway failure; other errors remain unclassified. Problem responses contain `type`, `title`, `status`, `detail`, `instance`; returned diagnostics govern handling without fabricating retry counts or availability conclusions.
