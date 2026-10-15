# Salesforce — Contact Record CRUD Procedure

Create, read, update, and delete a Contact record on Salesforce using the platform's generic REST
"sobjects" resource, the same generic path Salesforce documents for any standard or custom object.
Covers the four basic operations only — not upsert-by-external-ID, bulk/batch jobs, or Account
records (a different object, out of scope for this file). Assumes an OAuth 2.0 access token for the
target Salesforce org is already available — this procedure does not obtain or refresh one; see
`endpoints.md` for the token-vs-API-host distinction the calling tool must respect.

Sources: Salesforce's own REST API Developer Guide (create/retrieve/update/delete record pages under
`developer.salesforce.com/docs/platform/api-rest/guide/`, retrieved 2026-09-29), the REST API "Status
Codes and Error Responses" reference, the Object Reference "Required Fields" page, and the Salesforce
Help "Contact Fields" article. Retrieved via Salesforce's own published documentation rather than any
third-party mirror; where a specific page could not be loaded directly, the same fact was
cross-checked against another current Salesforce-authored page before being treated as confirmed.

## Operational procedure

1. **Confirm an access token and org host are available.** Salesforce's REST endpoints sit under the
   org's own instance or My Domain hostname, which is a separate value from wherever the token was
   obtained — using the wrong host for the API call is a common integration mistake, not a Salesforce
   error condition (see `endpoints.md`). If no token/host pair is available, stop and report FAILED
   with "no authenticated session."
2. **Build the Contact field payload for a create.** The only structurally-required field on a
   standard Contact is the last name — Salesforce's own object reference lists it as the sole
   required field at the platform level; an org can still layer its own validation rules (e.g.
   requiring an email or phone) on top, so a REQUIRED_FIELD_MISSING-style rejection naming a field
   other than last name means an org-specific rule fired, not a platform default. Do not invent or
   assume any other field is mandatory. If the caller supplied an email address, it must be a
   syntactically valid address — Salesforce enforces email-format validation on that field.
3. **Create the record** — submit the field payload to the Contact create resource (see
   `endpoints.md`). Treat HTTP 201 with a response body containing `"success": true` and an `id` as
   success; report CREATED with that id. Treat `"success": false` with a populated `errors` array as
   a rejection — report REJECTED with the array's `errorCode`/`message` content verbatim rather than
   normalizing it into a generic message.
4. **Read a record** — submit a retrieve call against the target Contact's record id (see
   `endpoints.md`). Optionally narrow to specific fields; omitting the field list returns every field
   the authenticated user has access to. Treat HTTP 200 with a field/value body as success; treat
   HTTP 404 as NOT_FOUND (either the id doesn't exist or the caller lacks visibility — Salesforce's
   own docs don't distinguish the two cases in the response, so don't claim to either).
5. **Update a record** — submit only the fields being changed against the target Contact's record id
   (see `endpoints.md`); this is a partial update, not a full replacement — fields left out of the
   payload keep their current stored values. Treat HTTP 204 with an empty body as success and report
   UPDATED. Treat a 4xx response the same way as step 3 (surface `errorCode`/`message` verbatim).
6. **Delete a record — stop and confirm with the operator before proceeding.** Deleting a Contact is a
   real, hard-to-reverse action against live customer/prospect data (Salesforce's Recycle Bin gives a
   time-limited undo window in the UI, but this procedure does not assume the calling tool has any
   path to that UI, so treat the deletion as final for planning purposes). Once confirmed, submit the
   delete call against the target Contact's record id (see `endpoints.md`). Treat HTTP 204 with an
   empty body as success and report DELETED; treat HTTP 404 as NOT_FOUND (already deleted or never
   existed).
7. **Handle failures verbatim.** For any 4xx/5xx response not already covered by a step above, report
   FAILED using the response's own `errorCode` and `message` fields (see `endpoints.md`) rather than
   guessing at a cause — Salesforce's error-response documentation does not enumerate every possible
   `errorCode` value, so don't assume a code not seen before is invalid; surface it as-is.

## Patterns

- **Token host and API host are two different values.** The host used to request the OAuth token
  (commonly a login/authorization host) is not necessarily the host the Contact endpoints live on —
  the token response itself carries the correct API host to use; see `endpoints.md`. Using the token
  host for API calls is a frequent integration error, not a Salesforce-documented failure mode.
- **A missing required field almost always means an org customization, not a platform default,**
  once last name is confirmed present — Salesforce's own required-fields reference names only last
  name as structurally required on Contact.
- **Update is inherently partial.** There is no "replace the whole record" semantics on this
  resource — sending a subset of fields is the normal and correct way to change just those fields.

## Known limitations

- Covers Contact only — Account and any other standard/custom object are out of scope for this skill.
- Does not cover upsert-by-external-ID, the Bulk API for batch operations, or SOQL/SOSL query — only
  the four single-record CRUD calls against the generic `sobjects/Contact` resource.
- Does not cover obtaining, refreshing, or revoking the OAuth access token itself — this procedure
  assumes a valid token and correct API host are already available to the calling tool.
- Salesforce's own documentation does not give an exhaustive list of `errorCode` values or per-field
  validation-rule error text — those are org-specific once past the platform's own baseline
  (last-name-required, email-format). Report whatever the response actually contains; don't fabricate
  a code or message the source doesn't document.
- Deleting a Contact is a real, hard-to-reverse action against live CRM data — see step 6's
  confirmation gate; this procedure does not treat the UI Recycle Bin as a safety net available to an
  API-driven delete.

## Tools

| Operation | Description | Category |
|---|---|---|
| `sObject Basic Information` → Create | Create a new Contact record | sObjects |
| `sObject Rows` → Retrieve | Read a Contact record by id | sObjects |
| `sObject Rows` → Update | Partially update a Contact record by id | sObjects |
| `sObject Rows` → Delete | Delete a Contact record by id | sObjects |

## Verification checklist

- [ ] Access token and the correct API host (from the token response, not the token/login host) were
      both confirmed available before the first call
- [ ] Create payload contained at minimum a last name; any other "required" field enforced came from
      an org-specific rule, not assumed as a platform default
- [ ] Any supplied email value was checked for valid email format before submission
- [ ] Update payload contained only the fields intended to change, not a full-record resend
- [ ] Delete was confirmed with the operator before submission
- [ ] Outcome reported using the response's own `success`/`errorCode`/`message` content, not a
      normalized or guessed status
