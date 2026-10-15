# CyberArk Privilege Cloud — Secret Retrieval Procedure

Retrieves or changes the credential value held by a privileged **account** in CyberArk Privilege
Cloud — CyberArk's SaaS privileged access management offering. Assumes the caller already holds a
valid Privilege Cloud session token (obtained via the platform's Logon call) with sufficient
permission on the target Safe/account; obtaining that session or provisioning the account/Safe
itself is out of scope here.

Source: CyberArk's own hosted Privilege Cloud documentation (docs.cyberark.com/privilege-cloud-
standard), specifically the REST API Authentication, "Get password value," and "Change credentials"
pages — confirmed via CyberArk's own published page titles/URLs and search-indexed excerpts of
their content, since the docs site itself returned no content to direct automated fetch at the time
of writing; treat any field name below not independently re-confirmed against a live tenant's own
Swagger UI as provisional. CyberArk does not publish a static, versioned OpenAPI/Swagger file for
Privilege Cloud (each tenant serves its own live Swagger UI with no stable external URL), so unlike
the other five vendors in this skill there is no pinnable canonical spec to cite alongside the docs
pages.

**Given the above, verify every field name and path in this file against your own tenant's Swagger
UI (reachable at `https://<subdomain>.privilegecloud.cyberark.com/PasswordVault/Swagger/` per
CyberArk's own documented access method) before relying on it in production.**

## Operational procedure

### 1. Authenticate (Logon)

Obtain a session token by presenting the caller's Privilege Cloud credentials to the Logon
endpoint. The response is a session token string; every subsequent call in this procedure presents
it in an `Authorization` header exactly as returned — CyberArk's own documentation is explicit that
this is required on every call except Logon itself.

### 2. Resolve the target account

Privilege Cloud's addressable unit for a credential is an **account** (a managed privileged
identity — e.g. a service account, database user, or device admin login), not a bare key/value
secret. If the account's ID isn't already known, search for it first (by keyword, or by an explicit
filter expression such as `safeName eq <safe>`) and resolve to exactly one `accountID` before
proceeding — **if more than one account matches, stop and ask the operator to disambiguate** rather
than guessing which one is intended.

### 3. Retrieve the credential value

Submit a retrieve-password request against the resolved `accountID`. CyberArk's own documentation
states this call is intended for human/interactive retrieval (e.g. an operator copying a password
to use manually) rather than as the primary integration path for applications — where the caller is
itself an automated system needing to authenticate as this account programmatically and repeatedly,
CyberArk's documented recommendation is to use a Credential Provider integration instead of this
direct retrieve call. Use this retrieve call for the "read a value on demand" case this skill
covers, but flag the human-vs-application distinction to the operator when the caller is clearly a
recurring automated integration rather than a one-off read.

The request body may optionally include a `reason` and ticketing-system reference (`TicketingSystem`
/ `TicketId`) if the tenant is configured to require dual-control/ticketing justification for
credential retrieval — check whether the target Safe enforces this before assuming an empty body is
sufficient.

### 4. Change the credential's value

**Confirm with the operator before changing a credential that's in active use** — this immediately
invalidates the previous value for anything still relying on it, and CyberArk's own documentation
notes this action does not itself propagate the new value to the target device (this endpoint
records the new value in the vault; a separate CPM-driven change/reconcile action is what actually
pushes it to the managed system, per step 5).

Submit the new credential value against the resolved `accountID`. An optional flag controls whether
the change applies to every account CyberArk considers part of the same logical credential group
(e.g. paired accounts).

### 5. Reconcile or verify a credential (where the caller needs the vault's record to match the live device, rather than setting an arbitrary new value)

- **Verify** — asks the CPM (Central Policy Manager) to confirm the vault's stored value still
  works against the actual target device, without changing anything. Asynchronous; no request body,
  no return value beyond call acceptance.
- **Reconcile** — asks the CPM to reset the account's credential using the platform's configured
  reconcile/logon account, resolving a mismatch between what the vault has stored and what's
  actually active on the device. Also asynchronous with no synchronous return value. **Confirm with
  the operator before triggering this** — it changes the live credential on the target system, not
  just the vault's record.

### 6. Handle documented conditions

- Every call after Logon requires the session token in the `Authorization` header — a missing or
  expired token produces an authentication failure; re-run Logon rather than retrying the same
  token.
- A retrieve/change call against an `accountID` that doesn't exist, or that the authenticated
  identity lacks permission on, fails — re-verify the account resolution from step 2 and the
  caller's Safe-level permissions rather than retrying blindly.
- Reconcile and Verify are asynchronous CPM-driven actions — a successful call acceptance does not
  itself confirm the underlying device operation succeeded; if the caller needs that confirmation,
  poll the account's status/last-reconciled fields afterward rather than assuming success from the
  call's own response.

## Patterns

- **"Change" updates the vault's record of the credential; it does not by itself push that value to
  the managed device.** Don't assume a successful Change call means the target system now accepts
  the new value — that requires the CPM's own change/reconcile process, which this documented
  endpoint set only triggers indirectly (or which "Reconcile" handles explicitly for pulling the
  device back into sync).
- **Retrieval is documented as an interactive/human path, not the recommended application
  integration.** Treat a request from an automated system that needs to repeatedly fetch this
  credential as a signal to raise the Credential Provider alternative with the operator, rather than
  silently defaulting to hammering the retrieve endpoint on a schedule.

## Known limitations

- Does not cover Safe creation/permissioning, account onboarding (adding a brand-new privileged
  account to the vault), or Credential Provider deployment — this skill assumes the account and its
  Safe already exist and the caller already has scoped access.
- Does not cover session/PSM (Privileged Session Manager) connect actions — interactive session
  brokering is a different capability from reading or setting a stored credential value.
- Field names and exact request/response shapes in `endpoints.md` are not independently verified
  against a live Privilege Cloud tenant — see the sourcing note at the top of this file.

## Tools

Every operation maps to the Privilege Cloud REST API — see `endpoints.md` for literal
request/response shape.

| Operation | Description | Category |
|---|---|---|
| Logon | Exchange credentials for a session token | Authentication |
| List/search accounts | Resolve an account name/filter to a specific `accountID` | Account Lookup |
| Retrieve password value | Read an account's current credential value | Secret Read |
| Change credentials | Write a new credential value to the vault's record for an account | Secret Write |
| Verify credentials | Ask the CPM to confirm the vault's value still matches the live device | Secret Verify |
| Reconcile credentials | Ask the CPM to reset the device's credential to match/repair the vault's record | Secret Write |

## Verification checklist

- [ ] Exactly one `accountID` was resolved before retrieve/change/verify/reconcile — ambiguous
      matches were escalated to the operator, not guessed
- [ ] Whether the target Safe requires a retrieval reason/ticket reference was checked before
      submitting an empty-body retrieve
- [ ] Any credential change or reconcile was confirmed with the operator first, with the
      change-vs-reconcile distinction (vault record vs. live device) made explicit
- [ ] If the caller was a recurring automated integration rather than a one-off human read, the
      Credential Provider alternative was raised per CyberArk's own documented guidance
- [ ] The retrieved credential value was not written into any log, report, or status message
