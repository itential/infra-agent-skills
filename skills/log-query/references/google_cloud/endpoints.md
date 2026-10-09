# Cloud Logging v2 entry binding

Source: [entries.list](https://docs.cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list),
retrieved 2026-10-09.

`POST https://logging.googleapis.com/v2/entries:list` with JSON body:

```json
{
  "resourceNames": ["projects/<PROJECT_ID>"],
  "filter": "timestamp >= \"2026-01-01T00:00:00Z\" AND timestamp < \"2026-01-02T00:00:00Z\"",
  "orderBy": "timestamp desc",
  "pageSize": 100
}
```

The date window and project are placeholders, not defaults. An existing authenticated client has a
supported OAuth scope such as `https://www.googleapis.com/auth/logging.read` and the applicable
`logging.logEntries.list`, `logging.privateLogEntries.list`, or `logging.views.access` permissions.
`resourceNames` supports up to 100 parent/view names. `projectIds` is deprecated.

Success returns `entries` and optional `nextPageToken`. The next request adds `pageToken` equal to
that token, keeping all other inputs identical. Empty `entries` with a token requires continuation.
`orderBy` supports only `timestamp asc` and `timestamp desc`; the default is ascending. A negative
`pageSize` is invalid. A filter is limited to 20,000 characters.
