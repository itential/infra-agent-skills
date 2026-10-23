# Cloudflare One CASB — Policy Endpoints

Wire-level binding for `procedure.md`. Source: Cloudflare Docs "Remediation Policies" and the CASB
API reference (retrieved 2026-10-22). Base URL: `https://api.cloudflare.com/client/v4`. All calls
send `Authorization: Bearer <API_TOKEN>`. `{account_id}`, `{policy_id}`, and similar are placeholders.

Terraform equivalents exist (`cloudflare_zero_trust_casb_policy` resource, plus single and list data
sources); the procedure's steps apply unchanged. A Terraform-managed policy that changes
`finding_type_id` is destroyed and recreated.

## Calls

| Procedure operation | Method and path | Notes |
|---|---|---|
| List integrations | `GET /accounts/{account_id}/one/integrations` | Note the `one/` prefix — differs from the other calls. Optional vendor filter (e.g. `GOOGLE_WORKSPACE`), `page`, `page_size`. Each result has `id`, `name`, `status`, `application.display_name`. |
| List finding types | `GET /accounts/{account_id}/data-security/posture/finding_types` | Optional `vendors` (comma-separated enum or friendly name), `page`, `per_page`, sort field. Result includes `vendor` and whether the type applies to all integrations. |
| List remediation types | `GET /accounts/{account_id}/data-security/posture/finding_types/{finding_type_id}/remediation_types` | `page`/`per_page`, or cursor; the two are mutually exclusive. Result items carry `remediation_type_id`, `remediation_type`, `display_name`. |
| List policies | `GET /accounts/{account_id}/data-security/posture/policies` | Paginated via `result_info`. |
| Get policy | `GET /accounts/{account_id}/data-security/posture/policies/{policy_id}` | Adds `last_triggered_at` (omitted if never fired), `created_at`, `updated_at`, `disabled_at`. |
| Create policy | `POST /accounts/{account_id}/data-security/posture/policies` | Token permission: Zero Trust Write. |
| Update policy | `PUT /accounts/{account_id}/data-security/posture/policies/{policy_id}` | Full replacement. Token permission: Zero Trust Write. |
| Delete policy | `DELETE /accounts/{account_id}/data-security/posture/policies/{policy_id}` | Token permission: Zero Trust Write. |

## Policy fields

| Field | Used on | Meaning |
|---|---|---|
| `display_name` | create, update | Policy name |
| `description` | create | Optional free text (not listed among the documented update fields) |
| `enabled` | create, update | `false` pauses the policy |
| `applies_to_all_integrations` | create, update | `true` covers every integration of the vendor |
| `integration_ids` | create, update | Array of integration IDs; used when the previous field is `false` (inclusion on update is an assumption) |
| `finding_type_id` | create only | Immutable |
| `actions.remediation_types[]` | create, update | Items `{remediation_type_id}`; at most one |
| `actions.webhook_configs[]` | create, update | Items `{webhook_config_id}` |

Create body shape (placeholders only):

```json
{
  "display_name": "<NAME>",
  "description": "<DESCRIPTION>",
  "enabled": true,
  "applies_to_all_integrations": true,
  "finding_type_id": "<FINDING_TYPE_ID>",
  "actions": {
    "remediation_types": [{ "remediation_type_id": "<REMEDIATION_TYPE_ID>" }],
    "webhook_configs": [{ "webhook_config_id": "<WEBHOOK_ID>" }]
  }
}
```

Responses follow the standard Cloudflare envelope: `success`, `errors[]`, `messages[]`, `result`, and
`result_info` for lists.

## Error strings worth recognizing

These come from the dashboard's remediation results rather than the policy API, and appear against
a finding instance when a remediation fails:

- `Resource has inherited permissions. Remediate permissions at the folder or organizational level.`
  (Microsoft 365)
- `Resource has inherited permissions from a parent resource. Direct remediation of the parent is
  not yet supported for Google Workspace.` (Google Workspace)
- `No automated remediation available for this finding type` — the finding type has no remediation
  types; offer webhook-only.

Exact API error codes for malformed or unauthorized policy requests are not documented: unknown.
