# AWS CloudTrail event history

Retrieve a bounded regional CloudTrail event history using an authenticated AWS API client.

## Common Sequences

- Recent activity evidence: **Define event scope** → **Read event pages** → **Preserve event evidence**.
- Multiple-region evidence: repeat that sequence independently for each explicitly selected account and region.

### Define event scope

The event-history operation uses one region and account, an optional start/end time, and at most one attribute filter. Its management-event history is limited to the preceding 90 days. Insight events require the supported Insight category and enabled Insight collection. The end time must not precede the start time. Success is a valid scoped request; an organization trail does not turn this regional call into an all-region query.

### Read event pages

The first read returns events in descending event-time order and may return a continuation token. Subsequent reads keep all query parameters unchanged while supplying that token. Success is the returned event page; the collection is complete only when no continuation token remains. Page size is one through fifty, with fifty as the default. AWS documents a limit of two requests per second per account per region for this operation.

Invalid category, attribute, page-size, token or time-range errors require correction of the corresponding input. A disallowed or unsupported operation is reported with its native error. Throttling or transient failures leave the query incomplete; the configured SDK retry behavior applies without inventing a retry count or declaring an empty result.

### Preserve event evidence

The returned event identifiers, timestamps, actors and resources remain associated with their account and region. The event-detail payload is decoded as JSON when required. Success is a collection with its original event identity, time bounds and completeness; it is not a determination that the activity was malicious or authorized.

## Patterns

Only one lookup attribute is accepted per query. Combining multiple independently retrieved result sets requires explicit local intersection/union semantics; sending several lookup attributes is not a supported substitute. Empty regional history does not establish that a resource never changed.

## Known limitations

No trail creation, configuration audit, CloudTrail Lake query, remediation or incident-severity decision is included. Event history does not provide arbitrary retention beyond its documented window.

Source: [CloudTrail LookupEvents API](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_LookupEvents.html), current API reference retrieved 2026-10-09. Literal bindings are in [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Read event pages | Read regional event history and continuation pages | Read |

## Verification checklist

- Account, region, event category, attribute and time bounds are recorded.
- Every continuation token was consumed or the result is marked incomplete.
- Original event identity and payload remain attached to their collection scope.
- Regional absence and API errors are not represented as security conclusions.
