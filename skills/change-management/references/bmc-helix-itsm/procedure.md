# BMC Helix ITSM — Change Request Lifecycle Procedure (Simplified REST API)

Search, retrieve, and update a change request in BMC Helix ITSM via the **simplified REST API**
(`com.bmc.dsm.itsm.itsm-rest-api`), which BMC recommends over the older, generic **platform REST API**
for all supported use cases (see Patterns for why). Assumes an authenticated session against the
target Innovation Suite server (a JWT-bearing session established via the login flow — see
`endpoints.md`) is already available to the calling agent.

## Operational procedure

### Common Sequences

**Find change requests needing attention and update one:**
1. Search Change Requests — using a saved filter and/or explicit field conditions (status, assignee,
   etc.) rather than fetching everything and filtering client-side.
2. Retrieve a Change Request by ID — once a specific request ID is known (from the search results, or
   supplied directly).
3. Update a Change Request — apply the field changes (e.g. reassigning coordinator/group, or
   advancing status).

**Just look up one known change request by its ID:**
1. Retrieve a Change Request by ID directly — skip search entirely.

### Search Change Requests

Search using either a named saved filter (`filter=<name>`) or explicit `criteria` conditions
(field/operation/value triples combined with `AND`/`OR` via `bindingExpression`), or both together.
Supports pagination (`limit`/`offset`), sorting (`sortBy`), and limiting returned fields (`fields`) to
avoid pulling the full record when only a few fields are needed.

**Confirm the target instance's actual status-code values before writing a condition against
`status`.** The two worked examples in BMC's own documentation use different status codes for what
appear to be similar exclusion conditions (`10`/`11`/`12`/`13` in one example, `27000` in another) —
these are very likely different fields/instances/versions, not a typo, but it means there is no single
universal status-code table to rely on here; confirm the target instance's actual configured values
(e.g. via a metadata/schema lookup, not detailed further in this pass) rather than assuming either
example's codes apply generically.

Confirm success: the response returns a list of matching change requests with the requested `fields`
populated — an empty result means no matches, not an error, if the criteria themselves are valid.

### Retrieve a Change Request by ID

Direct lookup by the change request's ID (e.g. `CRQ000000000501`). Confirm success: the response
contains the full record for that specific ID — a 404-equivalent response means the ID doesn't exist
on this instance, not a transient failure to retry.

### Update a Change Request

Partial update — only the fields included in the request body are changed; fields not mentioned are
left as-is (this is the documented PATCH semantics of this API, not a full-record replace). The
worked example reassigns coordinator/group fields; the same partial-update mechanism applies to
advancing `status` or any other writable field.

**Stop and confirm with the operator before proceeding with a status change that closes, cancels, or
otherwise finalizes a change request** — the same operator-confirmation discipline this skill applies
to every platform's terminal/durable transition, even though this specific API's own documentation
doesn't call out a particular field as
"the closing one" the way ServiceNow's gate-check does. Treat any status value that reads as terminal
on the target instance's configured workflow as requiring that confirmation.

Confirm success: re-retrieve the change request (Retrieve a Change Request by ID) and confirm the
updated field(s) actually changed — don't rely solely on a non-error response from the update call
itself.

## Patterns

- **BMC recommends the simplified REST API over the platform REST API for all supported use cases —
  default to it.** The platform REST API is the older, generic form-based API (operates on arbitrary
  Helix Innovation Suite forms, not change-request-specific resources); the simplified REST API is
  purpose-built with change-request-shaped endpoints (`/change/search`, `/change/{id}`) and is BMC's own
  stated recommendation. Only reach for the platform REST API if a specific capability genuinely isn't
  covered by the simplified API.
- **Authentication is a login-then-reuse-JWT flow, not a static API key.** A login request returns a
  JWT (and sets a cookie used for subsequent calls in some client flows); the token has a configurable
  idle/absolute expiry, after which a fresh login is required. Treat "the token expired mid-task" as an
  expected condition to handle (re-login), not an unusual failure.
- **Status-code values are not universal across instances/fields — always confirm against the target
  before writing a status condition or comparing a returned status value against an assumed meaning.**

## Known limitations

- Covers Search, Retrieve by ID, and Update (partial) on change requests only — does not cover change
  request creation, approval workflow specifics for BMC Helix ITSM's change management module,
  relationship/CI association, or the platform REST API's generic form-based operations.
- No documented gate-check/transition-discovery mechanism was found for this API (unlike ServiceNow's
  explicit "get available states" capability or Jira Service Management's "get customer transitions") —
  this procedure's own operator-confirmation discipline on terminal status changes is this skill's own
  addition, not something the API itself enforces or exposes as a pre-check.
- Status-code values used in filtering/searching are instance- and field-specific — this procedure
  does not assume a universal table of codes; confirm against the target instance before relying on any
  specific numeric value.
- Token expiry behavior (exact idle/absolute timeout values) is configurable per instance and wasn't
  extracted as a fixed default — treat "how long until I need to re-login" as instance-specific.

## Tools

| Operation | Description | Category |
|---|---|---|
| Login (token generation) | Authenticate and obtain a JWT for subsequent calls | Authentication |
| Search Change Requests | Query change requests by saved filter and/or explicit field criteria | Change Records |
| Retrieve Change Request by ID | Read a single change request's full record | Change Records |
| Update Change Request | Partial update of one or more fields on a change request | Change Records |

## Verification checklist

- [ ] The simplified REST API was used by default, with a specific reason documented if the platform
      REST API was used instead for a capability the simplified API doesn't cover
- [ ] Any status-code condition used in a search, or any comparison against a returned status value,
      was confirmed against the target instance's actual configured values — not assumed from either
      of BMC's own documentation examples
- [ ] A status change that reads as terminal (closing/cancelling) on the target workflow received
      explicit operator confirmation before the update call
- [ ] An update was re-verified via a follow-up Retrieve by ID, not assumed successful from the update
      call's response alone
- [ ] Token expiry was handled as an expected re-login condition, not treated as an unexplained failure
