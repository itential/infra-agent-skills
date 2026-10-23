# Cloudflare One CASB — Findings Read Endpoints

Wire-level binding for `procedure.md`. Source: Cloudflare Docs CASB API reference for findings,
finding instances, content findings, finding types, and integrations (retrieved 2026-10-23). Base
URL: `https://api.cloudflare.com/client/v4`. All calls send `Authorization: Bearer <API_TOKEN>`; the
token needs Zero Trust Read or Zero Trust Write. `{account_id}` and similar are placeholders. Every
call here is a GET and changes nothing.

## Calls

| Procedure operation | Method and path | Notes |
|---|---|---|
| List findings | `GET /accounts/{account_id}/data-security/posture/findings` | Returns ignored findings too unless `ignored=false`. |
| Get finding | `GET /accounts/{account_id}/data-security/posture/findings/{finding_id}` | Response shape not documented here; assumed to match a list item. |
| List finding instances | `GET /accounts/{account_id}/data-security/posture/findings/{finding_id}/instances` | `finding_id` is byte-formatted (assumption: base64, matching the list result's `id`). |
| Get finding instance | `GET /accounts/{account_id}/data-security/posture/findings/{finding_id}/instances/{instance_id}` | |
| List content findings | `GET /accounts/{account_id}/data-security/posture/content` | One result per asset. |
| Get finding type | `GET /accounts/{account_id}/data-security/posture/finding_types/{finding_type_id}` | |
| List finding types | `GET /accounts/{account_id}/data-security/posture/finding_types` | Filter `vendors`, paginated. |
| Get integration | `GET /accounts/{account_id}/one/integrations/{id}` | Note the `one/` prefix, unlike the posture calls. |
| List integrations | `GET /accounts/{account_id}/one/integrations` | `application` (vendor/application filter), `page`, `page_size`. |

## Query parameters

List findings: `cursor`, `direction` (`asc`/`desc`), `finding_type_ids` (comma-separated UUIDs),
`ignored` (boolean), `integration_id`, `min_affliction_date`, `max_affliction_date` (ISO 8601 or
epoch), `observation` (`Activity`/`Insight`/`Issue`), `order` (`finding.name`, `instance_count`,
`integration.name`, `latest_affliction_date`, `severity`), `page`, `per_page`, `product`
(`Cloud`/`Saas`), `search`, `severity` (`Critical`/`High`/`Medium`/`Low`), `type`
(`Content`/`Posture`), `vendor` (enum such as `GOOGLE_WORKSPACE`, `MICROSOFT`, `AWS`, `GITHUB`).

List finding instances: `archived`, `asset_ids`, `finding_instance_ids` (arrays, comma-separated),
`cursor`, `direction`, `min_affliction_date`, `max_affliction_date`, `order` (`affliction_date`,
`asset.name`, `remediation.status`), `page`, `per_page`, `remediation_statuses` (`none`, `pending`,
`processing`, `validating`, `completed`, `failed`), `search`.

List content findings: `dlp_profile_id`, `integration_id`, `vendor`, `direction`,
`min_affliction_date`, `max_affliction_date`, `order` (`asset_name`, `dlp_profile_count`,
`integration_name`, `latest_affliction_date`), `page`, `per_page`, `search`.

Whether `cursor` and `page` can be combined on these lists is not documented, so use one
pagination style per sequence.

## Response fields used

- **Finding list item:** `id` (base64), `active_count`, `archived_count`, `instance_count`,
  `ignored`, `finding` (`id`, `name`, `severity`, `vendor`, `description`, `origin`,
  `category.{observation,product,type}`, `applies_to_all_integrations`, `match_count`,
  `quarantined`, `remediation.{threat,impact,guide,frameworks}`), and `integration` (name, created,
  last-hydrated time, permissions, and a policy summary).
- **Finding instance:** `affliction_date`, `asset` (`name`, `external_id`, `category.{service,type,vendor}`,
  `fields[]` of name/value/link, `link`, `updated`), `dlp_contexts[]`, `remediations[]` (up to the
  ten most recent: `id`, `created_at`, `stale`, `status`), `webhooks[]` (latest job per
  destination).
- **DLP context:** `profile_id`, `entry_ids`, `created`, `updated`, `deleted`, `id`,
  `match_context_min_extent`, `match_context_max_extent`, `match_context_payload` (sensitive; see
  `procedure.md`).
- **Content finding:** `asset_id`, `asset_name`, `dlp_contexts[]`.
- **Integration:** `id`, `name`, `status` (the documented example shows `Healthy`), `is_paused`,
  `application.display_name`, `auth_method`, `created`, `updated`, `use_cases[]`.
- **Envelope:** `success`, `errors[]`, `messages[]`, `result`, and `result_info` (`count`,
  `total_count`, `page`, `per_page`, `next`, `previous`, `cursor`).

## Error text worth recognizing

Exact API error strings for these calls are not documented: unknown.
