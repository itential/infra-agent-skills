# Auvik service usage query

Read the published client/device usage records for supplied dates.

## Common Sequences

- Read usage: **Establish tenant scope** → **Read usage** → **Complete the read or report its error**.

### Establish tenant scope

Credential verification establishes API access; tenant discovery supplies the client identities authorized for the account. The requested tenant is resolved from that result. Each tenant is queried separately so failures retain their scope. A regional redirect requires correction to the account's actual Auvik region, not unrestricted forwarding of credentials.

### Read usage

Client usage uses the selected tenant scope; device usage instead resolves a single device ID. Both require start and end dates in the documented calendar-date form. The result is the returned usage record set with its original scope and units. An invalid date or inaccessible device remains a request/access error, not zero usage.

### Complete the read or report its error

A successful empty result is still HTTP 200. Cursor-based lists continue through their returned next links; an intentional stopping point is reported as partial. The result preserves native status, timestamps and missing values. A bad request requires corrected parameters, authentication/authorization failures require corrected access, and not-found requires checking the resource identity. These are not blindly retried. Rate-limit responses pause further requests; the publisher also documents rate-limit blocking that appears as forbidden. Internal service errors use exponential backoff, with persistent failures referred to platform support. No universal retry count is specified.

## Patterns

Client and device usage calls have different scopes. Neither automatically supplies a price schedule.

## Known limitations

This procedure does not derive invoice amounts or compare customers. No universal billing period is imposed.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Verify/resolve | Resolve tenant/device identity | Usage read |
| Read usage | Retrieve client/device usage for dates | Usage read |

## Verification checklist

- Dates and requested scope match the query.
- Native units and records are retained.
- Errors are not converted to zero usage.

## Sources

- [Auvik OpenAPI v1 specification](https://auvikapi.us1.my.auvik.com/spec). Retrieved 2026-10-09.
- [Auvik integration guide](https://support.auvik.com/hc/en-us/articles/360031007111-Auvik-API-Integration-Guide). Retrieved 2026-10-09.
