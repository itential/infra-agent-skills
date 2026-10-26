# Prometheus metric query

Evaluate a PromQL expression against a Prometheus server, instantly or over a range, and check what the server is scraping.

Sources: Prometheus HTTP API reference and management API reference (rolling "latest" docs, retrieved 2026-10-26). Bindings: [endpoints.md](endpoints.md).

Read-only: no confirmation gates apply. Authentication to the server depends on how the deployment is exposed; the HTTP API reference does not define one.

## Common Sequences

- Current value: Check readiness, then Discover series, then Evaluate instant.
- History: Check readiness, then Discover series, then Evaluate range.

## Check readiness

Ask the server whether it is ready to serve queries. Success is an HTTP 200. Any other result or a transport failure means query availability is unknown; it says nothing about the monitored devices.

## Discover series

List metric names (optionally limited by time window and series selectors), read metric metadata (type, help text, unit where exported) for a chosen name, and list scrape targets with their health, last scrape time, and last error.

- A name missing from the list does not prove there are no samples: the time bounds on this lookup are approximate.
- A name can have more than one metadata entry.
- A target with an unhealthy status or a last error explains missing data better than the query result does.

## Evaluate instant

Evaluate the supplied expression at one evaluation time (server time if omitted), with an optional timeout and series limit.

- Success: envelope status success, plus a result type of vector, matrix, scalar, or string with its data. Keep the result type; shapes differ.
- The series limit truncates vectors and matrices only. A limit of 0 means no limit.
- Warnings and informational notes can accompany a successful result; keep them with the data.

## Evaluate range

Evaluate the expression at each step between an inclusive start and end. Start, end, and step are all required; step is a duration or a number of seconds.

- Success: a matrix of series.
- The step is the spacing of evaluation, not the exporter's sampling rate.
- A request timeout is capped by the server's configured query timeout.

## Handle errors

- HTTP 400, missing or malformed parameter: correct the parameter and retry once.
- HTTP 422, the expression cannot be executed: review the expression; do not retry unchanged.
- HTTP 503, query timed out or was aborted: report the query as unsuccessful; narrow the window or series set before retrying.
- Other transport errors: report separately from query results.
- Rate limits and quotas: not documented for the API. On an HTTP 429 from a fronting proxy, back off and honor any Retry-After header.

## Patterns

- A range query re-evaluates the expression at every step, so a counter's raw samples and a rate expression answer different questions.
- Long expressions can be sent as a form-encoded request body to the same query operations when a URL would be too long.
- Results keep their labels and timestamps; report them with the values.

## Known limitations

- The caller supplies the PromQL; this procedure does not build queries or interpret them as health.
- Reload, quit, and other lifecycle operations exist but are disabled unless the server enables them; they are not used here.
- Not documented: any ceiling on points per range query.

## Tools

| Operation | Description | Category |
|---|---|---|
| Check readiness | Confirm the server can answer queries | Read |
| Discover series | List metric names, metadata, and scrape targets | Read |
| Evaluate instant | Evaluate an expression at one time | Read |
| Evaluate range | Evaluate an expression across an interval | Read |

## Verification checklist

- The envelope status is success and any warnings travel with the data.
- Result type, labels, timestamps, series limit, and range step match the request.
- Scrape health is reported separately from the query value.
