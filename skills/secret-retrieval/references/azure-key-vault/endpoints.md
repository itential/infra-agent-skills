# Endpoint Wiring — Azure Key Vault Secret Retrieval

Literal API calls behind each capability named in `procedure.md`. All calls target
`{vaultBaseUrl}` = `https://<vault-name>.vault.azure.net`, JSON request/response bodies,
authenticated with an Azure AD OAuth2 bearer token (`Authorization: Bearer <token>`) scoped to
`https://vault.azure.net/.default`. `api-version` is a required query parameter on every call.

Source: learn.microsoft.com/en-us/rest/api/keyvault/secrets/, API version `2025-07-01`, retrieved
2026-09-29.

## Get Secret

`GET {vaultBaseUrl}/secrets/{secret-name}/{secret-version}?api-version=2025-07-01`

`{secret-version}` is optional (the trailing path segment can be omitted) — omitted returns the
latest version.

Response (200), `SecretBundle`:
```
{
  "value": "string",
  "id": "https://<vault>.vault.azure.net/secrets/<name>/<version>",
  "contentType": "string",
  "attributes": {
    "enabled": true,
    "created": <unixtime>,
    "updated": <unixtime>,
    "exp": <unixtime, optional>,
    "nbf": <unixtime, optional>,
    "recoveryLevel": "Purgeable | Recoverable+Purgeable | Recoverable | ..."
  },
  "tags": { "<key>": "<value>" }
}
```

Errors: `KeyVaultError` envelope on any non-200; common causes are a missing secret/version or an
authorization gap on `secrets/get`.

## Get Secrets (List, vault-scoped)

`GET {vaultBaseUrl}/secrets?api-version=2025-07-01&maxresults={1-25, optional}`

Response (200), `SecretListResult`:
```
{
  "value": [
    { "id": "string", "contentType": "string", "attributes": {...}, "tags": {...}, "managed": false }
  ],
  "nextLink": "string, present if more results exist"
}
```
No `value` field is present per item here (that's what distinguishes list from get) — only
identifiers and attributes.

## Set Secret

`PUT {vaultBaseUrl}/secrets/{secret-name}?api-version=2025-07-01`

`{secret-name}` must match pattern `^[0-9a-zA-Z-]+$`.

Request body, `SecretSetParameters`:
```
{
  "value": "string",
  "contentType": "string, optional",
  "attributes": { "enabled": true, "exp": <unixtime>, "nbf": <unixtime> },
  "tags": { "<key>": "<value>" }
}
```
Always creates a new, immutable version — never modifies an existing version's value.

Response (200): a `SecretBundle` identical in shape to Get Secret's response, describing the newly
created version.

## Delete Secret

`DELETE {vaultBaseUrl}/secrets/{secret-name}?api-version=2025-07-01`

Applies to the entire secret (all versions) — cannot target one version individually.

Response (200), `DeletedSecretBundle`:
```
{
  "recoveryId": "https://<vault>.vault.azure.net/deletedsecrets/<name>",
  "deletedDate": <unixtime>,
  "scheduledPurgeDate": <unixtime>,
  "id": "string",
  "attributes": { "recoveryLevel": "...", ... },
  "tags": {...}
}
```
`scheduledPurgeDate` and `recoveryId` are only meaningful if the vault's `recoveryLevel` includes
soft-delete protection — check `recoveryLevel` on the secret's own attributes beforehand to know
whether this delete is recoverable within a window or immediate.

## Error envelope (shared across all operations above)

`KeyVaultError`:
```
{
  "error": {
    "code": "string",
    "message": "string",
    "innererror": { "code": "string", "message": "string" }
  }
}
```
