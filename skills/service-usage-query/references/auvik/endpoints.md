# Auvik service usage query: bindings

The authenticated client uses HTTPS with TLS verification and Basic authentication: account username plus API key as password. Base URL follows the account region; the published example is `https://auvikapi.us1.my.auvik.com`. No credential value is included here. Dates use the publisher ISO timestamp form where timestamp parameters are specified.

| Shared operation | Binding | Result |
|---|---|---|
| Verify access | `GET /v1/authentication/verify` | 200 accepted, 401 rejected |
| Resolve tenants | `GET /v1/tenants` | `data` with tenant identities |

Cursor pagination uses `page[first]` with `page[after]`, or `page[last]` with `page[before]`; list schemas expose continuation links where supported. HTTP 400/401/403/404/429/500 remain distinct errors. The integration guide publishes 2,500 requests per five-minute window and also describes a per-IP block that can return 403. That status must be interpreted with the response error rather than presumed to be only an ACL failure.

| Operation binding | Required parameters | Other supported parameters |
|---|---|---|
| `GET /v1/billing/usage/client` | `filter[fromDate]`; `filter[thruDate]` | `tenants` |
| `GET /v1/billing/usage/device/{id}` | `id`; `filter[fromDate]`; `filter[thruDate]` | None |


## Sources

- [Auvik OpenAPI v1 specification](https://auvikapi.us1.my.auvik.com/spec). Retrieved 2026-10-09.
- [Auvik integration guide](https://support.auvik.com/hc/en-us/articles/360031007111-Auvik-API-Integration-Guide). Retrieved 2026-10-09.
