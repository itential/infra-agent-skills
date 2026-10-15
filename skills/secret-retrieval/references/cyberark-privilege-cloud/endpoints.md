# Endpoint Wiring — CyberArk Privilege Cloud Secret Retrieval

Literal API calls behind each capability named in `procedure.md`. All calls are the Privilege Cloud
REST API, JSON request/response bodies unless noted, against the tenant's own Privilege Cloud
hostname.

Sourcing caveat: CyberArk does not publish a static, versioned OpenAPI/Swagger spec for Privilege
Cloud — only a live, per-tenant Swagger UI (`https://<subdomain>.privilegecloud.cyberark.com/
PasswordVault/Swagger/`, per CyberArk's own documented access instructions). Paths and field names
below are drawn from CyberArk's hosted documentation pages (docs.cyberark.com/privilege-cloud-
standard — "REST APIs / Authentication," "Get password value," "Change credentials in Privilege
Cloud") as confirmed via their own published page titles and search-indexed excerpts, retrieved
2026-09-29, since the docs pages themselves returned no content to direct automated fetch. **Verify
every path and field below against your own tenant's Swagger UI before production use.**

## Logon (Authenticate)

`POST /PasswordVault/API/auth/Cyberark/Logon` (or the equivalent path for the tenant's configured
authentication method — LDAP, SAML, RADIUS variants exist per CyberArk's own auth documentation;
Cyberark-native is the default shown here)

Body: `{ "username": "<login>", "password": "<password>" }`

Response (200, `text/plain` or JSON depending on tenant config): a session token string.

## Authenticated calls (all operations below)

Header: `Authorization: <session token exactly as returned by Logon>`

## List/Search Accounts

`GET /PasswordVault/API/Accounts`

Optional query parameters: `search` (keyword list), `searchType` (`contains`/`startswith`),
`filter` (e.g. `safeName eq mySafe`), `sort`, `offset`, `limit`.

Response (200): a list of account summary objects, each including an `id` (the `accountID` used by
every other call below).

## Retrieve Password Value

`POST /PasswordVault/API/Accounts/{accountID}/Password/Retrieve`

Body (optional): `{ "reason": "<string>", "TicketingSystem": "<string>", "TicketId": "<string>",
"ActionType": "show|copy|connect", "Machine": "<target address, if the account is provisioned for
multiple remote machines>" }`

Response (200, `text/plain`): the raw credential value.

CyberArk's own documentation notes this call is intended for interactive/human retrieval; see
`procedure.md` for when to raise the Credential Provider alternative instead.

## Change Credentials

`POST /PasswordVault/API/Accounts/{accountID}/Password/Update`

Body: `{ "NewCredentials": "<new value>", "ChangeEntireGroup": <boolean, optional> }`

Sets the vault's stored value for the account; does not by itself push the value to the managed
device (see `procedure.md` step 4/5 for the distinction from Reconcile).

## Verify Credentials

`POST /PasswordVault/API/Accounts/{accountID}/Verify`

No request body. Asynchronous — a 200 response confirms the request was accepted, not that
verification against the live device has completed.

## Reconcile Credentials

`POST /PasswordVault/API/Accounts/{accountID}/Reconcile`

No request body. Asynchronous — resets the account's credential via the platform's configured
reconcile/logon account. **Confirm with the operator before calling — this changes the live
credential on the target system.**
