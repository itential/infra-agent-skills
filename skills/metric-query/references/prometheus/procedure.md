# Prometheus metric query

Retrieve PromQL results and the metadata needed to interpret a requested series.

Primary sources: [HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/),
[query semantics](https://prometheus.io/docs/prometheus/latest/querying/basics/), and
[management API](https://prometheus.io/docs/prometheus/latest/management_api/), rolling documentation,
retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Current observation: Check readiness → Discover series → Evaluate expression → Interpret response.
- Historical observation: Check readiness → Discover series → Evaluate range → Interpret response.

## Check readiness

The readiness operation returns 200 when the server can answer queries. A transport or readiness
failure leaves query availability unknown; it does not describe a monitored device's condition.

## Discover series

Metric-name discovery reads the metric-name label's values. Metadata supplies metric types, help,
and units where exported; multiple metadata descriptions can exist for the same name.
Target discovery provides scrape health, last scrape, and scrape errors for the selected scope.
An absent label value is not proof of absent samples: metadata time bounds are approximate.

## Evaluate expression

An instant evaluation uses the supplied expression and evaluation time; an omitted time uses the
server's current time. Success includes the returned result type and value. Scalar, string, vector,
and matrix results have different shapes and retain those distinctions.

## Evaluate range

A range evaluation uses the expression, inclusive start/end times, and an explicit step.
Success is a matrix of evaluated series. The step describes evaluation spacing; it is not a promise
that the underlying exporter sampled at that frequency. A request timeout cannot exceed the server's
configured query timeout. Any chosen series limit remains part of the reported scope.

## Interpret response

A successful API envelope can still contain warnings and informational annotations; these accompany
the returned data. Invalid input (400) requires parameter correction. An unevaluable expression (422)
requires expression review. Aborted or timed-out evaluation (503) is an unsuccessful query;
consult server guidance before changing the query budget. Other transport failures remain separate
from PromQL results. Literal envelope names are in the binding reference.

## Patterns

PromQL range evaluation repeatedly evaluates the expression. A counter's raw samples and a rate
expression answer different questions. Query results retain their labels and timestamps.

## Known limitations

Metric metadata is an experimental API. This procedure does not enable lifecycle/admin operations,
change scrape configuration, or establish device-wide health from a scrape result.

## Tools

| Operation | Description | Category |
|---|---|---|
| Check readiness | Determine whether queries can be served | Read |
| Discover series | Retrieve metric names, metadata, and scrape targets | Read |
| Evaluate expression | Evaluate at one instant | Read |
| Evaluate range | Evaluate across a bounded interval | Read |

## Verification checklist

- The API envelope indicates success and any warnings remain attached.
- The result type, labels, timestamps, limits, and range step match the selected query.
- Scrape status is reported separately from the query value and from device health.
