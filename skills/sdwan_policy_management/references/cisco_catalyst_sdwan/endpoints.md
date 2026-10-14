# Endpoints — Cisco Catalyst SD-WAN Manager, centralized policy (template policy)

Literal wiring layer for `procedure.md`. Operation names in the procedure's Tools table map to the
calls below.

Written against Cisco Catalyst SD-WAN Manager API release 26.2 (original configuration area,
document version 26.2.0+2026-07-29), checked 2026-10-14. Field and example shapes are restated with
placeholder values.

## Base path and versioning

API calls are made against the Manager host with the path prefix `/dataservice`; the policy calls
below are written without it. The login, refresh, and logout routes in the next section are shown as
Cisco's authentication page gives them; whether they take the prefix is not stated there, except the XSRF
token route, which is written with it. The API version, where it matters, is negotiated through a
vendor media type in the `Accept` header rather than in the path; the default is version 1.0.

## authenticate

Two documented methods:

**Session (all releases):**
1. `POST /j_security_check`, content type `application/x-www-form-urlencoded`, body
   `j_username=<user>&j_password=<password>`. The session identifier is returned as a `JSESSIONID`
   cookie; a failed login returns an HTML login page instead of an error status.
2. `GET /dataservice/client/token` with the cookie returns the XSRF token as plain text.
3. Send the cookie on every call. Send `X-XSRF-TOKEN: <token>` on every POST, PUT, and DELETE.
4. `POST /logout` ends the session.

**JWT (Manager 20.18.1 and later):**
1. `POST /jwt/login` with a JSON body of `username`, `password`, and optional `duration` in seconds
   (1 to 604800, default 1800). The response includes `token`, `refresh`, and `csrf`.
2. Send `Authorization: Bearer <token>` on every call and `X-XSRF-TOKEN: <csrf>` on writes.
3. `POST /jwt/refresh` with the refresh token returns a new access token; Cisco notes it does not
   renew the refresh token itself. A failed JWT login returns HTTP 401.

The JWT method has no logout route; Cisco advises requesting a short expiry so tokens do not outlive the
work.

Session limits stated by Cisco: 30 minutes of inactivity, 24 hours maximum lifetime, and 100
concurrent sessions (least recently used sessions are dropped beyond that).

## list_policies

```
GET /template/policy/vsmart
```
Returns an array of policies (the reference's example wraps the array in a `data` key although its
schema says array; accept both). Each item carries `policyId`, `policyName`, `policyDescription`,
`policyType`, `isPolicyActivated`, `policyVersion`, `lastUpdatedBy`, `createdBy`, and `policyDefinition`.
`policyType` is `feature` or `cli` in the examples. For `feature`, `policyDefinition` is an object holding an
assembly: a list of `{definitionId, type, entries: [{direction, siteLists: [<id>], vpnLists: [<id>]}]}`
(`vpnLists` appears where a policy block uses VPN lists). For `cli`, it is plain policy text with no assembly.
Example assembly `type` values: `vpnMembershipGroup`, `control`, `hubAndSpoke`, `appRoute`, `data`. These
are camel-case, while the definition read paths use lower-case family names (`vpnmembershipgroup`,
`hubandspoke`, `approute`); map them by lower-casing (assumption).

## read_policy

```
GET /template/policy/vsmart/definition/{policyId}
```
`policyId` is a UUID. Returns the policy object; the response schema is not detailed in the source.

## read_active_policies

```
GET /template/policy/vsmart/definition/activateIds
```
Returns the identifiers of active policies across all tenants. Response schema not detailed.

## read_controller_connectivity

```
GET /template/policy/vsmart/connectivity/status
```
Response schema not detailed in the source.

## read_definition_or_list

```
GET /template/policy/list
GET /template/policy/definition/{type}/{id}
```
`/template/policy/list` returns all policy lists. Definitions are per type, with `{type}` being one of
the definition families in the API (for example `control`, `data`, `approute`, `mesh`, `hubandspoke`,
`vpnmembershipgroup`). The same path family also holds create, edit, delete, and preview calls, which
are out of scope here.

## create_policy

```
POST /template/policy/vsmart
Content-Type: application/json
```
Body (shape from Cisco's example, values are placeholders):

```json
{
  "policyName": "<name>",
  "policyDescription": "<description>",
  "policyType": "feature",
  "policyDefinition": {
    "assembly": [
      {"definitionId": "<definition-uuid>", "type": "<definition type>"}
    ]
  },
  "isPolicyActivated": false
}
```
Success (200): `{"policyId": "<uuid>"}`. Other documented statuses: 400, 403, 500. The meaning of
`policyType` values other than `feature` is not documented.

The create example carries no `entries` (the site-list and direction attachment shown in list
responses). How a create applies a definition to site lists is not documented; copy the shape from a
list read (assumption), and see `procedure.md`.

## edit_policy

```
PUT /template/policy/vsmart/{policyId}
```
Body is the full policy object. Cisco's example shows `policyId`, `policyState` (`edit`),
`policyVersion`, `lastUpdatedBy`, `policyName`, and a `policyDefinition` expressed as policy text
(the CLI form). Whether `policyDefinition` is sent as text or as the assembly object depends on how
the policy was created; read the policy first and send the same form (assumption).

A variant exists that skips lock checks so several components can be edited together:

```
PUT /template/policy/vsmart/central/{policyId}
```
No request or lock semantics are documented for it.

## activate_policy

```
POST /template/policy/vsmart/activate/{policyId}
```
Body: `{"isEdited": false}`. Success (200): a task object, for example
`{"id": "vsmart_policy_config-<timestamp>"}`. Statuses 400, 403, and 500 are documented without
detail.

The activate route's own examples also include a \"Deactivate policy\" body of `{}`. That conflicts with the dedicated deactivate route, which this procedure follows; the activate-route example is not used.

A second route, `POST /template/policy/vsmart/activate/central/{policyId}`, is documented for
cloud-services activation. It has no described semantics and is not used by this procedure.

## deactivate_policy

```
POST /template/policy/vsmart/deactivate/{policyId}
```
No request body. Success (200): a task object, for example
`{"id": "vsmart_policy_config-<uuid>"}`.

## delete_policy

```
DELETE /template/policy/vsmart/{policyId}
```
Success: 200 with no body. 400, 403, and 500 are documented without detail.

## poll_task

Not defined in the specification used. Assumption (unverified): the Manager's device action-status call,
`GET /device/action/status/{processId}`, which Cisco's device-action API reference lists as "Find Status".
Its schema and success value were not read. Confirm it in Cisco's current documentation before relying on
it, and if it cannot be bound, report ACTIVATION_UNCONFIRMED or DEACTIVATION_UNCONFIRMED as `procedure.md`
describes.

## Error handling

The source documents only the HTTP classes 400, 403, and 500 for these calls, with no error strings.
Report FAILED with the actual status and body. A session-method login that returns an HTML page
indicates failed authentication rather than a policy error.
