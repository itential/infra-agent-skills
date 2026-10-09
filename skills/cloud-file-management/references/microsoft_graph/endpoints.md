# Microsoft Graph v1.0 file bindings

Base URL: the tenant's Graph cloud endpoint; global cloud uses `https://graph.microsoft.com/v1.0`. Authentication uses `Authorization: Bearer <access-token>`. Delegated reads require `Files.Read`; uploads require `Files.ReadWrite`. Application reads require `Files.Read.All`; uploads require `Files.ReadWrite.All`. Additional SharePoint Embedded permissions are outside this binding.

| Operation | Method and route | Input / expected output |
|---|---|---|
| List folder children | `GET /drives/{drive-id}/items/{item-id}/children` | Optional `$select`, `$top`, `$orderby`; `value` collection and possible `@odata.nextLink` |
| Get item metadata | `GET /drives/{drive-id}/items/{item-id}` | Optional `$select`, `$expand`; 200 driveItem |
| Resolve by path | `GET /drives/{drive-id}/root:/{item-path}` | 200 driveItem |
| List versions | `GET /drives/{drive-id}/items/{item-id}/versions` | 200 version collection; newest first, no `$orderby` |
| List permissions | `GET /drives/{drive-id}/items/{item-id}/permissions` | 200 permission collection; `inheritedFrom` identifies inherited entries; cannot expand permissions from metadata |
| List thumbnails | `GET /drives/{drive-id}/items/{item-id}/thumbnails` | 200 thumbnailSet collection, potentially empty |
| Download | `GET /drives/{drive-id}/items/{item-id}/content` | 302 `Location` to preauthenticated content; no Authorization on redirected request |
| Upload new content | `PUT /drives/{drive-id}/items/{parent-id}:/{filename}:/content` | Binary body, suitable content type; returned driveItem |
| Replace content | `PUT /drives/{drive-id}/items/{item-id}/content` | Binary body; returned driveItem |

`If-None-Match` on documented read operations can produce 304. File paths require Graph-compatible path encoding; identifiers must come from the selected tenant. `Range` applies to the download URL, not the Graph content route. A successful range may return206; a full-stream fallback may return200.

## Error conditions

The response's `error.code`, nested `innererror.code` and `details` identify failures. Message text is variable and is not a matching contract.

| Condition | Handling |
|---|---|
| 400/405/406/411/415/416/422 | Correct input, method, headers, size/range or representation before continuing |
| 401 | Restore authentication |
| 402/403 | Resolve license, permission or conditional-access requirements; `insufficient_claims` requires the relevant access flow |
| 404/410 | Target is missing or gone; end that lookup |
| 409/412/423 | Resolve conflict, changed precondition or lock; concurrency violations can use delayed retry with any `Retry-After` |
| 413/507 | Content exceeds supported size or storage capacity; stop transfer |
| 429/509 | Defer calls according to throttling guidance |
| 500/501/503/504 | Preserve the failure; temporary unavailability can retry after the supplied delay, but an uncertain upload first needs reconciliation |

Sources: the Microsoft Learn method and error references linked in [the procedure](procedure.md), v1.0, retrieved 2026-10-09. The upload reference's replacement example returns201; this binding therefore checks the returned driveItem rather than assuming replacement always returns200.
