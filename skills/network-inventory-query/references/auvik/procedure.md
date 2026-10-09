# Auvik network inventory query

Read tenant-scoped discovered devices and related network inventory.

## Common Sequences

- Device inspection: **Establish tenant scope** → **Read inventory** → **Read related context** → **Complete the read or report its error**.

### Establish tenant scope

Credential verification establishes API access; tenant discovery supplies the client identities authorized for the account. The requested tenant is resolved from that result. Each tenant is queried separately so failures retain their scope. A regional redirect requires correction to the account's actual Auvik region, not unrestricted forwarding of credentials.

### Read inventory

Device information resolves the requested device identifiers. Detail and extended-detail reads add the corresponding discovery/platform information; the extended collection requires a device-type filter. Network, interface and component reads retain their own resource IDs and relationships. Online/operational states are observations from Auvik, not a new active connectivity test.

### Read related context

Entity-note and entity-audit reads use the selected entity and requested filters. They describe stored notes and audit entries, not a universal change-approval record. Authentication material or secrets present in collected inventory are not report fields.

### Complete the read or report its error

A successful empty result is still HTTP 200. Cursor-based lists continue through their returned next links; an intentional stopping point is reported as partial. The result preserves native status, timestamps and missing values. A bad request requires corrected parameters, authentication/authorization failures require corrected access, and not-found requires checking the resource identity. These are not blindly retried. Rate-limit responses pause further requests; the publisher also documents rate-limit blocking that appears as forbidden. Internal service errors use exponential backoff, with persistent failures referred to platform support. No universal retry count is specified.

## Patterns

Info, detail and extended-detail responses are different views. A device name or IP supplied by a wrapper must first resolve to an unambiguous native ID.

## Known limitations

API v1 only; a separate v2 device API exists. This procedure does not reconcile a source of truth, create tickets or infer replacement priority. Billing reads are a separate usage capability.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Verify/resolve | Establish accessible tenant identities | Inventory read |
| Read inventory | Query device/network/interface/component records | Inventory read |
| Read context | Query entity notes/audits | Inventory read |

## Verification checklist

- Requested tenant and entities resolve.
- Selected view and filters are reported.
- Pagination is complete or explicitly partial.
- Native statuses and access failures remain distinct.

## Sources

- [Auvik OpenAPI v1 specification](https://auvikapi.us1.my.auvik.com/spec). Retrieved 2026-10-09.
- [Auvik integration guide](https://support.auvik.com/hc/en-us/articles/360031007111-Auvik-API-Integration-Guide). Retrieved 2026-10-09.
