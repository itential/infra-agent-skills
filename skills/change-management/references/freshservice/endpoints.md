# Endpoint Wiring — Freshservice Change Management (API v2)

Literal API calls behind each capability named in `procedure.md`. Base URL:
`https://<domain>.freshservice.com`. Auth: HTTP Basic with API key as username, `X` as password
(`-u api_key:X`), or OAuth 2.0 with the scopes noted per endpoint.

## Change object — key fields

| Field | Type | Notes |
|---|---|---|
| `id` | number | Read-only. |
| `workspace_id` | number | Defaults to primary workspace if omitted. Cannot be changed via Update — only via Move. |
| `agent_id` | number | Assigned agent. |
| `requester_id` | number | Mandatory. Initiator of the change. |
| `group_id` | number | Assigned agent group. |
| `description` / `description_text` | string | `description` is HTML; do not pass `description` and `description_html` together. `description_text` is read-only (derived). |
| `priority` * | number | See Change Properties below. |
| `impact` * | number | See Change Properties below. |
| `status` * | number | See Change Properties below. |
| `risk` * | number | See Change Properties below. |
| `change_type` * | number | See Change Properties below. |
| `approval_status` | number | Read/derived — see Approval Properties in the approvals section. Defaults to `4` on create in the documented examples (not one of the 4 named approval statuses — treat this default as platform-internal until confirmed against the target tenant; do not assume it maps to "requested"). |
| `planned_start_date` / `planned_end_date` | ISO 8601 datetime | Change window. |
| `subject` | string | |
| `department_id` | number | |
| `category` / `sub_category` / `item_category` | string | |
| `custom_fields` | hash | Key-value pairs, tenant-specific. |
| `maintenance_window` | hash | On create/update, pass only `{"id": <maintenance_window_id>}` — other maintenance-window properties (dates, description) are not settable through this API, only via the web UI. |
| `blackout_window` | hash | Read-only — details of an overlapping blackout window. |
| `change_window_id` | number | Appears in some responses; distinct from `maintenance_window`. |
| `assets` / `impacted_services` | array | Associated assets / impacted services. |

\* See "Change Properties" below for the numeric values each of these fields accepts.

## Change Properties (numeric enums)

**Status**
| Value | Meaning |
|---|---|
| 1 | Open |
| 2 | Planning |
| 3 | Approval |
| 4 | Pending Release |
| 5 | Pending Review |
| 6 | Closed |

Note: the documented table above lists 6 values. The `stats` embed (`?include=stats`) additionally
exposes `closed_at`, `planning_at`, `assigned_at`, `approval_at`, `pending_release_at`, and
`pending_review_at` timestamp fields, implying a "Released" state/transition exists operationally
between Pending Release and Closed even though it is not broken out as its own numbered status value in
the documented table — treat "Released" as a milestone reachable en route to status 6, not a separate
status number, unless the target tenant's `change_form_fields` response says otherwise (see "List all
Change Fields" below — always confirm the live enum against the tenant, since custom statuses can be
added).

**Priority**
| Value | Meaning |
|---|---|
| 1 | Low |
| 2 | Medium |
| 3 | High |
| 4 | Urgent |

**Impact**
| Value | Meaning |
|---|---|
| 1 | Low |
| 2 | Medium |
| 3 | High |

**Change Type**
| Value | Meaning |
|---|---|
| 1 | Minor |
| 2 | Standard |
| 3 | Major |
| 4 | Emergency |

**Risk**
| Value | Meaning |
|---|---|
| 1 | Low |
| 2 | Medium |
| 3 | High |
| 4 | Very High |

## Create a Change

Tool hint: `POST /api/v2/changes` — OAuth scope `freshservice.changes.create`.

```
curl -v -u api_key:X -H "Content-Type: application/json" -d '{
  "description": "<div>...</div>",
  "subject": "Getting ES3 back up to speed",
  "email": "tom@outerspace.com",
  "priority": 1,
  "status": 1,
  "group_id": 1,
  "risk": 1,
  "change_type": 1,
  "impact": 1,
  "planned_start_date": "2019-03-20T16:18:46Z",
  "planned_end_date": "2019-03-23T16:18:46Z",
  "department_id": 1,
  "agent_id": 1,
  "maintenance_window": {"id": 1},
  "workspace_id": 3
}' -X POST 'https://domain.freshservice.com/api/v2/changes'
```

Response: `201`-equivalent with `{"change": {...full object...}}`. `requester_id` is mandatory (the
sample above resolves it from `email` server-side); every field marked `*` above should be set
explicitly rather than relying on an undocumented default, since the source doc doesn't state defaults
for `priority`/`impact`/`status`/`risk`/`change_type` on create — only `approval_status` is observed
defaulting to `4` in example responses.

Custom fields: pass a `custom_fields` hash matching the tenant's configured custom fields (see
`List all Change Fields` below to discover the live set — do not guess field names).

## View a Change

Tool hint: `GET /api/v2/changes/{id}` — OAuth scope `freshservice.changes.view`.

`?include=stats` embeds `closed_at`, `planning_at`, `assigned_at`, `approval_at`,
`pending_release_at`, `pending_review_at`, and `resolution_time_by_bhrs` — each embed consumes an
additional API credit.

## View List of Changes

Tool hint: `GET /api/v2/changes` — OAuth scope `freshservice.changes.view`.

Filters (cannot combine `view` and `query` in the same request):
- `query="<field>:<value> AND|OR <field>:<value>"` — URL-encoded, quoted, max 512 chars. Operators:
  `:` (equals), `:>` (greater-or-equal), `:<` (less-or-equal), `!:` (not equal). String values in single
  quotes, numbers bare, dates as `'yyyy-mm-dd'` in UTC. Use the `null` keyword to filter for
  unassigned agent/group.
- `view=<name-or-id>` — a saved Change Management view (default or custom).
- `updated_since=<ISO8601>` — changes updated on/after this timestamp.
- `workspace_id=<id>` — `0` returns changes across all accessible workspaces (Employee Support Mode
  accounts only) with just global fields; omitted defaults to the primary workspace only.
- `order_by=<field>`, `order_type=asc|desc` (default `desc`).
- `per_page=<1-100>` (default 30), `page=<n>`.

Default list excludes deleted/spam changes unless the `deleted` filter is used.

## Update a Change

Tool hint: `PUT /api/v2/changes/{id}` — OAuth scope `freshservice.changes.edit`.

```
curl -v -u api_key:X -H "Content-Type: application/json" -X PUT -d '{ "priority": 3 }' \
  'https://domain.freshservice.com/api/v2/changes/1'
```

`workspace_id` cannot be changed via Update — only via Move (`move_workspace`, below).

Attachment upload variant: use `-F` form-data fields (not raw JSON) with `attachments[]=@<path>` —
`Content-Type: multipart/form-data` is set automatically once the body is form-data.

## Move a Change (workspace transfer)

Tool hint: `PUT /api/v2/changes/{id}/move_workspace` — OAuth scope `freshservice.changes.edit`.
Applicable only to accounts with workspaces.

```
curl -v -u api_key:X -X PUT -d '{ "workspace_id": 3, "group_id": 3, "owner_id": 4 }' \
  'https://domain.freshservice.com/api/v2/changes/1/move_workspace'
```

## Delete a Change

Tool hint: `DELETE /api/v2/changes/{id}` — OAuth scope `freshservice.changes.delete`.
Response: `204 No Content`. Documented as a soft delete — "Deleted changes are not permanently lost";
the source references a Restore Change capability but does not document its endpoint in the extracted
material — confirm its existence/path against the live API reference or the target tenant before
relying on restore being possible via API.

## List all Change Fields

Tool hint: `GET /api/v2/change_form_fields` — discovers the tenant's actual configured fields
(including custom fields and any tenant-specific additions to the enums above). Use this before
assuming the numeric enums in this file are complete for a given tenant — Freshservice allows
custom statuses/fields per account.

## Approvals for Changes

Approval object fields: `id`, `created_at`, `updated_at`, `approver_id`, `approver_name`,
`approval_type`, `approval_group` (hash: id/name), `user_id`/`user_name` (initiator), `level`
(multi-level approval position), `approval_status` (hash: `{"id": <n>, "name": "<string>"}`),
`delegatee` (hash: id/name), `latest_remark`, `email_content` (View-single only).

**Approval Type enum:**
| Value | Meaning |
|---|---|
| 1 | To be approved by Everyone |
| 2 | To be approved by Anyone |
| 3 | To be approved by Majority |
| 4 | To be approved by First Responder |

**Approval Status enum:**
| Value | Name |
|---|---|
| 0 | requested |
| 1 | approved |
| 2 | rejected |
| 3 | cancelled |

### List all Change Approvals
Tool hint: `GET /api/v2/changes/{change_id}/approvals` — OAuth scope `freshservice.changes.view`.

### View a Change Approval
Tool hint: `GET /api/v2/changes/{change_id}/approvals/{approval_id}` — OAuth scope
`freshservice.tickets.view` (documented as-is in the source; note this is a Tickets-scoped OAuth
permission being reused for a Changes read endpoint — confirm this isn't a documentation typo against
the live reference before depending on it for a least-privilege OAuth app).

### Send Reminder for a Change Approval
Tool hint: `PUT /api/v2/changes/{change_id}/approvals/{approval_id}/remind` — OAuth scope
`freshservice.changes.edit`. Empty body. Response: `200` (source labels it "200 No Content", though 200
responses conventionally carry a body — treat the documented label as informational, verify actual
behavior against the live tenant).

### Cancel a Change Approval
Tool hint: `PUT /api/v2/changes/{change_id}/approvals/{id}` — OAuth scope `freshservice.changes.edit`.
Body: `{"approval_status": {"id": 3}}` (3 = cancelled).

**This is the only approval-status transition this API supports.** The source states explicitly:
"This API supports the changing of an approval status to 'cancelled' state only. All other status
change can be executed only via approver's action in the product." There is no documented
approve/reject-via-API call — approving or rejecting a change requires the approver's own action in the
Freshservice UI (or presumably their approval-notification email flow), not this API.

### Create an Approval Group for a Change
Tool hint: `POST /api/v2/changes/{change_id}/approval-groups` — OAuth scope
`freshservice.changes.edit`.
Body: `{"name": "...", "approval_type": <1-4>, "email_content": "<optional HTML>", "approver_ids": [...]}`.
`email_content` is optional — omitting it sends the default approval notification.

### Update Approval Group In A Change Request
Tool hint: `PUT /api/v2/changes/{change_id}/approval-groups/{id}` — OAuth scope
`freshservice.changes.edit`. Same body shape as create.

### List all Approval Groups within a Change
Tool hint: `GET /api/v2/changes/{change_id}/approval-groups` — OAuth scope
`freshservice.changes.edit` (documented as edit scope even for a list/read call — confirm against the
live tenant if building a strictly read-only integration).

### Cancel Approval Group In A Change Request
Tool hint: `PUT /api/v2/changes/{change_id}/approval-groups/{id}` — same endpoint as Update; body
`{"approval_status": {"id": 3}}` (3 = cancelled) distinguishes a cancel from a content update.

### Update approval chain rule for a change
Tool hint: `PUT /api/v2/changes/{change_id}/approval-chain-rule` — OAuth scope
`freshservice.changes.edit`. Body: `{"rule": <n>}`. Response includes `approval_chain.level`,
`.rule`, `.approval_status`, and the nested `.approval_groups` at that chain level. The source sample
cURL for this endpoint uses `-X POST` while the documented method signature says `put` — flagged as an
inconsistency in the source; confirm the actual accepted verb against the live tenant before relying on
either exclusively.

## Notes on a Change

Fields: `id`, `user_id` (read-only), `body` (HTML, mandatory), `body_text` (read-only, plain-text
derived), `notify_emails` (array of strings), `created_at`, `updated_at`.

### Create a Note
Tool hint: `POST /api/v2/changes/{id}/notes` — OAuth scope `freshservice.changes.notes.create`.
Body: `{"body": "<div>...</div>"}`.

## Documented error codes (platform-wide, apply to Changes endpoints too)

| Code | Meaning |
|---|---|
| `missing_field` | A mandatory attribute is missing (e.g. `requester_id` on create). |
| `invalid_value` | Incorrect, blank, or invalid-format value. |
| `duplicate_value` | Value already exists. |
| `datatype_mismatch` | Field value doesn't match the expected type. |
| `invalid_field` | An unexpected field was included in the request payload. |
| `invalid_json` | Request body is not valid JSON. |
| `invalid_credentials` | Missing/incorrect API credentials (commonly: API key not Base64-encoded). |
| `access_denied` | Insufficient privileges for the action. |
| `require_feature` | Action requires a feature not enabled on the tenant. |
| `account_suspended` | Account suspended. |
| `ssl_required` | Request must use HTTPS. |
| `readonly_field` | Attempted to alter a read-only field. |
| `no_content_required` | JSON body supplied where none is expected. |
| `inaccessible_field` | Caller not authorized to update this specific field. |
| `incompatible_field` | Field cannot be updated given the record's current state (e.g. a state-gated field). |
| `unsupported_authentication_type` | Request used an unsupported auth method (e.g. username/password instead of API key/OAuth). |
| `access_token_expired` | OAuth access token expired — refresh and retry. |
| `access_token_invalid` | OAuth token has invalid signature/scope, or account no longer part of the issuing Freshworks org. |

Pagination: `page` (1-based), `per_page` (default 30, max 100 — values above 100 error). The response
`link` header carries the next-page URL when more pages exist. Avoid deep pagination past page 500 per
the source's own performance guidance.
