# Auvik configuration backup query

Locate and retrieve an authorized stored configuration backup.

## Common Sequences

- Retrieve a backup: **Establish tenant scope** → **List backups** → **Read selected backup** → **Complete the read or report its error**.

### Establish tenant scope

Credential verification establishes API access; tenant discovery supplies the client identities authorized for the account. The requested tenant is resolved from that result. Each tenant is queried separately so failures retain their scope. A regional redirect requires correction to the account's actual Auvik region, not unrestricted forwarding of credentials.

### List backups

The backup collection is filtered by resolved device ID, backup time window and requested running/startup selection. Returned record identities and timestamps establish available backups. A empty result means no matching accessible records, not that the live device has no configuration.

### Read selected backup

The selected backup ID resolves a single stored configuration record. Content is handled as potentially sensitive configuration; credentials are not reproduced in the report. The selected record and backup timestamp confirm retrieval. Reading the record does not apply it to a device or prove it is the newest running state.

### Complete the read or report its error

A successful empty result is still HTTP 200. Cursor-based lists continue through their returned next links; an intentional stopping point is reported as partial. The result preserves native status, timestamps and missing values. A bad request requires corrected parameters, authentication/authorization failures require corrected access, and not-found requires checking the resource identity. These are not blindly retried. Rate-limit responses pause further requests; the publisher also documents rate-limit blocking that appears as forbidden. Internal service errors use exponential backoff, with persistent failures referred to platform support. No universal retry count is specified.

## Patterns

A configuration record has its own identity; the device ID is a list filter, not a substitute for the backup ID in a single-record read.

## Known limitations

Backup availability and collection coverage depend on Auvik discovery and permissions. Restore and business retention policy are outside scope.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Verify/resolve | Resolve tenant and device scope | Inventory read |
| List/read backups | Retrieve stored configuration history/content | Configuration read |

## Verification checklist

- Device and backup IDs are not confused.
- Timestamp and selected backup type are retained.
- Sensitive configuration is not echoed.
- Retrieval is not reported as restore.

## Sources

- [Auvik OpenAPI v1 specification](https://auvikapi.us1.my.auvik.com/spec). Retrieved 2026-10-09.
- [Auvik integration guide](https://support.auvik.com/hc/en-us/articles/360031007111-Auvik-API-Integration-Guide). Retrieved 2026-10-09.
