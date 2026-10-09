# Auvik device lifecycle query

Retrieve the lifecycle and warranty records associated with selected discovered devices.

## Common Sequences

- Inspect lifecycle/coverage: **Establish tenant scope** → **Read lifecycle and coverage** → **Complete the read or report its error**.

### Establish tenant scope

Credential verification establishes API access; tenant discovery supplies the client identities authorized for the account. The requested tenant is resolved from that result. Each tenant is queried separately so failures retain their scope. A regional redirect requires correction to the account's actual Auvik region, not unrestricted forwarding of credentials.

### Read lifecycle and coverage

The lifecycle collection or selected-device read returns reported sales, software/security maintenance and last-support information. Warranty reads return the separate warranty/service coverage record. Filters select native states; an omitted date or unknown state stays unknown. The response's associated device identity determines which record is being described. A returned end-of-support date does not select a replacement platform or establish a business deadline.

### Complete the read or report its error

A successful empty result is still HTTP 200. Cursor-based lists continue through their returned next links; an intentional stopping point is reported as partial. The result preserves native status, timestamps and missing values. A bad request requires corrected parameters, authentication/authorization failures require corrected access, and not-found requires checking the resource identity. These are not blindly retried. Rate-limit responses pause further requests; the publisher also documents rate-limit blocking that appears as forbidden. Internal service errors use exponential backoff, with persistent failures referred to platform support. No universal retry count is specified.

## Patterns

Warranty, service coverage and lifecycle milestones are independent data. A supported device need not have an active service contract.

## Known limitations

Only records available to Auvik and the caller are represented. Business prioritization and configuration backup content are outside this capability.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Verify/resolve | Resolve tenant scope | Inventory read |
| Lifecycle/coverage | Read lifecycle and warranty records | Asset read |

## Verification checklist

- Device identity and tenant are retained.
- Lifecycle and coverage fields remain separate.
- Missing/unknown values are not inferred.
- Query completion/error state is explicit.

## Sources

- [Auvik OpenAPI v1 specification](https://auvikapi.us1.my.auvik.com/spec). Retrieved 2026-10-09.
- [Auvik integration guide](https://support.auvik.com/hc/en-us/articles/360031007111-Auvik-API-Integration-Guide). Retrieved 2026-10-09.
