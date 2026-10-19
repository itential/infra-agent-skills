# Delinea Secret Server — Secret Retrieval Procedure

Reads, or overwrites a field of, a secret stored in Delinea Secret Server (self-hosted or Secret
Server Cloud) through its native REST API. Assumes the caller already has an application account
in Secret Server with permission on the target secret, and that the secret already exists;
creating accounts, secret templates, folders or the secret itself is out of scope. Calls routed
through the Delinea Platform use a different base path and a different token source, and are not
covered (see Known limitations).

Sources: Delinea Secret Server 11.6.x online help, "Script Authentication Using Tokens" and "REST
API Python Scripts", plus the Secret Access Workflow and Checking Out Secrets pages, retrieved
2026-10-19. The field-level read call, the string-literal shape of its response and the optional
domain parameter are not in those pages and are marked (unverified) below.

## Common Sequences

- **Read one field of a secret:** Get token (step 1) -> Get secret (step 2), select the item by
  slug -> use the value without logging it.
- **Overwrite one field of a secret:** Get token (step 1) -> Get secret (step 2) -> operator
  confirmation -> Update secret (step 3) -> Get secret (step 2) to confirm the stored value.

## Operational procedure

### 1. Authenticate — password-grant token

Exchange the application account's username and password for an access token at the token
endpoint, as a form-encoded POST with the grant type set to password. If the account uses
two-factor authentication, the one-time password goes in a separate request header. The response
carries the token in an `access_token` field. A token's lifetime is governed by the instance's
"Session Timeout for Webservices" setting, which Delinea recommends keeping at 20 minutes or less;
the documented lifetime is therefore instance-specific, so request a new token when a call is
rejected as unauthorized instead of assuming a fixed duration.

- Sending a domain value for a non-default domain is (unverified).
- The header format for presenting the token on later calls is not stated on the authentication
  page; the REST examples present it as a Bearer authorization header.
- Delinea's cautions apply: never keep the password or token in plain text, use a least-privilege
  application account rather than an administrator or domain-admin account, and do not hardcode
  credentials in scripts.

### 2. Read a secret

Fetch the secret by its numeric ID. The ID is the only addressing form shown in the source; no
lookup by name is documented here, so resolve the ID before calling. The response is a JSON object
with the secret's ID, name and active flag and an `items` list; each item has an item ID, a `slug`
(the field's short name, such as the one for a password) and an `itemValue`. Select the wanted
field by matching its slug.

- To read one field without the whole secret, the field-level read call takes the secret ID and
  the field slug. Its response is (unverified) a JSON-encoded string literal, so decode it with a
  JSON parser instead of using the raw bytes.
- A secret can be configured to require check-out, an approval workflow, or a comment before access.
  Delinea warns that integrations using the API may fail when "Require Comment" is enabled,
  because the API has no way to supply a comment at check-out. The source does not document the
  exact error returned or a check-out call; if a read is refused for this reason, report that the
  secret's access workflow blocks API retrieval and consult platform-specific guidance. Do not
  attempt to bypass it.

### 3. Update a secret's field

Read the secret (step 2), change the target item's `itemValue` in the returned structure, then
submit the modified secret to the same secret ID as an update. The response is the updated secret.
The source does not say whether a partial body is accepted, so send the full structure read in
step 2 with only the intended change.

**Confirm with the operator before overwriting a field whose current value is in active use.**
The source documents no version history or undo for an overwrite, and no way to read a prior
value; treat the change as hard to reverse.

### 4. Handle errors

The source documents success responses only. Treat any other status as a failure and consult
platform-specific guidance for it; in particular:

- **Unauthorized after a previously accepted token** — the token has likely expired; re-run step 1.
- **Forbidden or not found for a secret ID that should exist** — the account lacks permission on
  that secret, or the ID is wrong; do not guess another ID.
- **Refusal tied to check-out, approval or comment requirements** — see step 2.

## Patterns

- **Secrets are addressed by numeric ID, and values live in an `items` list keyed by slug.** There
  is no single "value" field; reading "the password" means selecting the item whose slug names it.
- **A single-field read and a whole-secret read return differently shaped payloads** (a string
  literal versus an object), so parse each accordingly.

## Known limitations

- Does not cover calls made through the Delinea Platform, which the source describes as using a
  different base path (API version 2), a token from Delinea's identity service, and a platform
  service account. Those need their own procedure.
- Does not cover creating secrets, templates or folders, check-out and check-in calls, approval
  requests, or listing and searching secrets.
- The source states no rate limits and no maximum token lifetime; both are unknown. On an
  HTTP 429 response, back off and honor any `Retry-After` header.
- Overwriting a field is irreversible through this procedure.

## Tools

Every operation maps to the Secret Server REST API; see `endpoints.md` for the literal calls.

| Operation | Description | Category |
|---|---|---|
| Get token | Exchange application account credentials for an access token | Authentication |
| Get secret | Read a secret and its fields by numeric ID | Secret Read |
| Get secret field | Read one field of a secret by slug (unverified) | Secret Read |
| Update secret | Submit a modified secret to overwrite a field value | Secret Write |

## Verification checklist

- [ ] The secret was addressed by numeric ID and the field selected by slug
- [ ] A least-privilege application account was used, with no password or token stored in plain text
- [ ] Any check-out, approval or comment requirement on the secret was reported, not bypassed
- [ ] Any overwrite of an in-use value was confirmed with the operator first
- [ ] The retrieved value was not written into any log, report or status message
