# Google Cloud Logging: entries.list Wiring

Sources: Google Cloud Logging API reference, entries.list (v2) (retrieved 2026-10-26).

`POST https://logging.googleapis.com/v2/entries:list` (regional endpoints also exist). Credentials come from the existing client with one of the scopes `logging.read`, `logging.admin`, `cloud-platform.read-only`, or `cloud-platform` (under `https://www.googleapis.com/auth/`), and the IAM permission `logging.logEntries.list`, `logging.privateLogEntries.list`, or `logging.views.access`.

| Body field | Meaning |
|---|---|
| `resourceNames` | Up to 100 parents, for example `projects/{project_id}` or a log view name |
| `filter` | Logging query language, up to 20,000 characters |
| `orderBy` | `timestamp asc` (default) or `timestamp desc` |
| `pageSize` | Default 50; negative is invalid |
| `pageToken` | Previous `nextPageToken` |

Response: `entries` and `nextPageToken`. Empty `entries` with a token means the search is unfinished.
