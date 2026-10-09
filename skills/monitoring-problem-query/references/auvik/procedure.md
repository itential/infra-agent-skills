# Auvik alert history query

Read alert history for an identified tenant and optional entity.

## Common Sequences

- Alert review: **Establish tenant scope** → **Read history** → **Complete the read or report its error**.

### Establish tenant scope

Credential verification establishes API access; tenant discovery supplies the client identities authorized for the account. The requested tenant is resolved from that result. Each tenant is queried separately so failures retain their scope. A regional redirect requires correction to the account's actual Auvik region, not unrestricted forwarding of credentials.

### Read history

Alert-history reads select the requested severity, lifecycle state, dismissed/dispatched flags or entity/definition identity. Dismissal and resolution are separate properties. The returned native state is retained; the skill does not acknowledge or dismiss alerts.

The published schema incorrectly types both detection-time filters as booleans while their descriptions require date/time values. These two filters remain unverified for typed clients: this procedure does not send guessed booleans or timestamps. When a bounded interval is essential, the executor needs corrected platform-specific guidance; an unbounded response is not reported as the requested interval.

### Complete the read or report its error

A successful empty result is still HTTP 200. Cursor-based lists continue through their returned next links; an intentional stopping point is reported as partial. The result preserves native status, timestamps and missing values. A bad request requires corrected parameters, authentication/authorization failures require corrected access, and not-found requires checking the resource identity. These are not blindly retried. Rate-limit responses pause further requests; the publisher also documents rate-limit blocking that appears as forbidden. Internal service errors use exponential backoff, with persistent failures referred to platform support. No universal retry count is specified.

## Patterns

Created, resolved, paused and unpaused are native history states. They are not generic incident statuses.

## Known limitations

No alert dismissal or automated incident priority. Detection-time filter type inconsistency is unresolved in the retrieved v1 schema.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Verify/resolve | Resolve tenant/entity scope | Monitoring read |
| Read history | Query alert records | Monitoring read |

## Verification checklist

- Tenant and any entity filter are explicit.
- Native alert lifecycle and dismissal are separate.
- Time-filter uncertainty is disclosed.
- Pagination and failures remain visible.

## Sources

- [Auvik OpenAPI v1 specification](https://auvikapi.us1.my.auvik.com/spec). Retrieved 2026-10-09.
- [Auvik integration guide](https://support.auvik.com/hc/en-us/articles/360031007111-Auvik-API-Integration-Guide). Retrieved 2026-10-09.
