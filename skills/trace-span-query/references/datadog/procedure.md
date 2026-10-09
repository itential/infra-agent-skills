# Datadog indexed span search

Datadog's V2 span search returns retained spans matching a caller-supplied search expression and interval.

## Procedure

1. **Define the query.** The request supplies a span-search expression and start/end times. Optional timezone or time offset may be set, but supplying both fails validation. Sorting selects ascending or descending timestamps.
2. **Retrieve a page.** The search returns spans with identifiers and attributes, plus result metadata. Bad input or unprocessable content requires correction using the error detail; denied access stops the query; throttling defers additional requests. The documented limit is300 requests/hour for this endpoint, not an assumption for all Datadog APIs.
3. **Continue the same query.** A continuation cursor leads to another page with the same expression, time interval and options. Success preserves every span and its trace/parent identity returned across pages. An empty result does not establish absence outside the retained data and queried interval.
4. **Evaluate completeness.** Native done status, pagination exhaustion and absence of partial-result warnings support a completed search. Timeout or warnings are reported alongside the available spans; those spans must not be represented as a complete trace. Unexpected errors preserve the failed/incomplete result.

## Patterns

- A span-search result is not a guaranteed full distributed trace; the response can include standalone spans.
- Timezone and numeric offset are alternate options, not additive corrections.
- Partial results can arrive in a successful HTTP response.

## Known limitations

No instrumentation installation, service listing, dependency mapping, service-summary calculation or inferred bottleneck threshold. Retention and indexing determine what is searchable. The exact supported expression is supplied by the requester or current Datadog span-search documentation.

## Tools

| Operation | Description | Category |
|---|---|---|
| Search spans | Retrieve a page of indexed APM spans and query metadata | Read |

## Verification checklist

- Query, site and time window are recorded.
- Continuation cursors retain the original query parameters.
- Native status and warnings qualify the reported result.
- Span search is not described as a verified complete trace.

Source: Datadog [Search spans](https://docs.datadoghq.com/api/latest/spans/search-spans/), APIv2, retrieved 2026-10-09.
