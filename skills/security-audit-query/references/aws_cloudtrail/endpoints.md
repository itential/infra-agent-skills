# CloudTrail event-history bindings

The AWS SDK operation is `LookupEvents`, with its client bound to the requested account and region. Request fields are `StartTime`, `EndTime`, `LookupAttributes`, `MaxResults`, `NextToken` and optional `EventCategory="insight"`.

`LookupAttributes` contains at most one object with `AttributeKey` and `AttributeValue`. The API documents supported keys: `AccessKeyId`, `EventId`, `EventName`, `EventSource`, `ReadOnly`, `ResourceName`, `ResourceType`, `Username`. `MaxResults` is 1–50, default 50. Start/end boundaries are inclusive. Pagination reuses all parameters with the returned `NextToken`.

The response has `Events` and optional `NextToken`. Each event includes native identity/time metadata and `CloudTrailEvent`, a string containing the event JSON. `EventCategory` omitted selects management events; `insight` selects Insights events.

## Native conditions

The API lists these HTTP 400 error types: `InvalidEventCategoryException`, `InvalidLookupAttributesException`, `InvalidMaxResultsException`, `InvalidNextTokenException`, `InvalidTimeRangeException`, `OperationNotPermittedException`, `UnsupportedOperationException`. Invalid-parameter failures are not empty collections. The documented operation limit is two requests per second per account per region.

Source: [LookupEvents](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_LookupEvents.html), retrieved 2026-10-09.
