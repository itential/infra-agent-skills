# AWS CloudWatch Logs: Logs Insights Wiring

Sources: Amazon CloudWatch Logs API Reference, StartQuery and GetQueryResults (retrieved 2026-10-26).

The calls are JSON-protocol operations of the CloudWatch Logs service (target prefix `Logs_20140328`), normally made through an SDK or CLI client that supplies the region, request signing, and credentials.

| Operation | API action | Parameters and result |
|---|---|---|
| Start query | `StartQuery` | Required `queryString` (up to 10,000 characters), `startTime`, `endTime` (epoch seconds). Optional `limit` (1 to 100,000), `queryLanguage` (`CWLI`, `SQL`, `PPL`), and exactly one of `logGroupName`, `logGroupNames`, `logGroupIdentifiers` (up to 50). Result `queryId`. |
| Get query results | `GetQueryResults` | `queryId`; optional `nextToken`, `maxItems` (up to 10,000). Result `status`, `results` (rows of field/value pairs, plus `@ptr`), `statistics`, `nextToken`. |

Errors for both: `InvalidParameterException`, `ResourceNotFoundException` (HTTP 400), `ServiceUnavailableException` (500). Start query also returns `LimitExceededException` and `MalformedQueryException` (400).
