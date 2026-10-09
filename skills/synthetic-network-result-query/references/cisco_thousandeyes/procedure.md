# ThousandEyes existing network and path results

Read existing network measurements or trace details for a known ThousandEyes test and account group.

Sources: Cisco API v7.0.110 [network results](https://developer.cisco.com/docs/thousandeyes/get-network-test-results/), [path summaries](https://developer.cisco.com/docs/thousandeyes/get-path-visualization-network-test-results/), [path detail by agent/round](https://developer.cisco.com/docs/thousandeyes/get-path-visualization-test-results-by-agent-and-round/), retrieved 2026-10-09. Bindings and response fields are in [endpoints.md](endpoints.md).

## Common Sequences

- Network evidence: Select query scope → Read network results → Follow result pages.
- Trace evidence: Select query scope → Read path summaries → Follow result pages → Read agent/round path detail.

### Select query scope

A known test ID and accessible account group select the test. The request uses either a relative window or explicit UTC start/end timestamps, never both. Omission retrieves the latest round. Network-result ranges can include a round beginning just before the requested start; the returned timestamps define actual coverage.

Direction follows the test's supported mode. For bidirectional agent-to-agent tests, network measurements can be reported per direction or combined. Path queries return separate directions, and omitting their direction selects both. An incompatible direction produces an error rather than a synthesized reverse path.

### Read network results

The network-result read returns observations grouped by agent and round, with native measurement values and any test-level error detail. Success is the result collection and scope metadata. An omitted loss measurement is unavailable, not zero. Negative health-score values are error indications; the documented insufficient-data value is not a low but valid health score. No severity threshold is invented from those measurements.

### Read path summaries

The path-summary read returns each observed agent/round/direction and trace summary, including trace identifiers, hop counts and destination response time where measured. Success is the summary collection. This operation does not return every hop's full detail; a known agent and round select the next read.

### Follow result pages

The publisher directs clients to the returned next link rather than constructing a cursor. The same authenticated API origin and requested account/test scope apply to subsequent pages. Success means all requested pages were read or a bounded partial result is identified. An error on a later page does not erase already retrieved evidence or turn it into a complete collection.

### Read agent/round path detail

The detail read uses the summary's test, agent and round identifiers with the intended direction. Each returned trace contains ordered hop records with available address, prefix, reverse-DNS, network, location, MPLS and hop RTT evidence. Missing optional values remain missing. The schema describes RTT to a hop; it does not establish that subtraction of adjacent RTTs measures one-way link delay or proves the device responsible for an outage.

For every read: invalid input requires correction of the request; unauthenticated/forbidden responses require valid access to the selected group; a missing resource remains not found; organizational rate-limit exhaustion requires backoff and any returned retry guidance. Server/bad-gateway errors remain failed reads with the reported detail. None of these errors mean zero packet loss or a healthy path.

## Patterns

- Path summary and hop detail are distinct reads.
- Result directions are not inferred from source/destination labels alone; those labels remain fixed for the documented bidirectional test relationship.
- Network health scores include negative error values, unlike an ordinary normalized score.

## Known limitations

- Existing test IDs are required. This procedure does not deploy probes or run instant tests.
- BGP routes, alerts/events/outages, endpoint tests and dashboards need their own API procedures.
- The deprecated NetClaw community MCP's parameter names are not reused as native API query fields.
- The sources specify organization-level rate exhaustion but no universal numerical rate limit for this procedure.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read network results | Retrieve per-agent/per-round existing measurements | Read |
| Read path summaries | Retrieve observed trace summaries | Read |
| Follow result page | Retrieve the next response-linked page | Read |
| Read agent/round path detail | Retrieve ordered hop evidence | Read |

## Verification checklist

- Test and account-group authorization match the requested scope.
- Time window, actual round timestamps and direction are recorded.
- Every requested page was read or incomplete coverage is explicit.
- Missing metrics, negative score codes and test errors remain distinct from valid measurements.
- Path summaries were expanded through the detail operation before reporting individual hops.
