# Endpoints — Netskope Private Access (NPA) Policy Rules

Literal wiring layer. `SKILL.md`/`procedure.md` steps reference these by name; bind them to whatever
REST client/adapter is assumed available.

Source: Netskope's own official documentation page "NPA Real-Time Policy REST API"
(docs.netskope.com/en/private-access-rest-apis/), retrieved 2026-09-29. Authentication header
convention cross-checked against Netskope's REST API v2 overview page
(docs.netskope.com/en/rest-api-v2-overview-312207), retrieved the same date.

## Base host and authentication

Base host is tenant-specific: `https://<tenant>.goskope.com/api/v2`. Authentication uses a
tenant-issued API token presented on every call in the `Netskope-API-Token` header. The token is
generated in the Netskope UI under Settings > Administration > Administrators & Roles > Administrators
(Service Account section), per Netskope's own REST API v2 documentation. A tenant may also require the
calling source IP to be present on its configured IP allowlist (Settings > Administration > IP
Allowlist) before the API will accept calls.

## List NPA Policy Rules

```
GET /api/v2/policy/npa/rules
```
Supports optional query parameters per Netskope's own documented conventions: `fields` (restrict
returned fields), `filter` (query-operator-based filter string), `limit` and `offset` (pagination),
`sortby` and `sortorder` (result ordering). Use before any placement-sensitive create/update to see
current rules and their order.

## Get NPA Policy Rule

```
GET /api/v2/policy/npa/rules/{id}
```

## Create NPA Policy Rule

```
POST /api/v2/policy/npa/rules
```

**Request body fields (restated from Netskope's own documentation page):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `rule_name` | string | Yes | The rule's display name |
| `enabled` | string | Yes | Activation state of the rule |
| `access_method` | array of string (enum) | Yes | `Client` or `clientless`, determining the connection mode the rule governs |
| `policy_type` | string | Yes | Fixed value identifying this as a private-app policy — do not vary |
| `rule_data` | object | Yes | The rule's actual scope/action configuration — see below |
| `description` | string | No | Free-text policy documentation |
| `group_id` / `group_name` | string | No | Associates the rule with a policy group |
| `rule_order` | object | No | Placement directive: a mode (`top`/`bottom`/`before`/`after`) plus a reference rule ID where applicable |
| `json_version` | — | No | Fixed metadata value documented by the source; do not compute or vary it manually |
| `template` | string | No | Custom block-notification template reference |

**`rule_data` sub-fields:**

| Field | Notes |
|---|---|
| `users` | List of user identifiers in scope |
| `userGroups` | List of group paths in scope |
| `organization_units` | List of organizational-unit identifiers in scope |
| `device_classification_id` | Restricts the rule to a specific device-posture classification |
| `privateApps` | List of private application references the rule governs access to |
| `privateAppTagIds` | Tag-based grouping of private apps, as an alternative/addition to naming apps directly |
| `publishers` | List of publisher references required to be associated with the matched private app(s) |
| `match_criteria_action` | The rule's primary decision, documented enum values including allow/block |
| `dlp_actions` | Data-loss-prevention profile(s) and remediation settings applied on match |
| `tss_actions` | Threat-scanning-service settings and remediation options applied on match |

**Success:** the source page frames a successful create as returning the created rule; exact HTTP
status codes are not enumerated on the page itself (it points to the tenant's own Swagger UI for full
response schema) — treat a 2xx response containing the rule object (with a populated `id`) as the
pass criterion, and prefer the live Swagger response detail for the target tenant over an assumed
status code.

**Failure:** not enumerated with specific codes/strings on the source page — surface the underlying
tool's actual response status and body rather than inferring an undocumented error condition.

## Update NPA Policy Rule (partial)

```
PATCH /api/v2/policy/npa/rules/{id}
```
Documented as a partial update — only fields present in the request body are changed; omitted fields
retain their existing value. Same field vocabulary as create.

## Delete NPA Policy Rule

```
DELETE /api/v2/policy/npa/rules/{id}
```

## Reference object lookups (for resolving names to the identifiers `rule_data` expects)

Private applications, publishers, private-app tags, and user groups each have their own list/lookup
endpoints elsewhere in Netskope's REST API v2 (outside this rule family) — resolve caller-supplied
names against those before building `rule_data`; this procedure does not restate each one's own wire
format since they sit outside the NPA policy-rule endpoint itself.

## Out-of-scope route families (not covered by this skill)

These are separate Netskope policy families with their own field shapes; listed only so a caller can
recognize them and not confuse them with the NPA rule endpoints above:

- `/api/v2/policy/realtime/rules` — real-time (CASB inline) rules
- `/api/v2/policy/internetaccess/rules` — internet-access rules
- `/api/v2/spm/policies` — SaaS Posture Management policies
