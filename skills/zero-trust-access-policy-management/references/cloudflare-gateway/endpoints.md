# Cloudflare One Gateway — Rule Endpoints

Wire-level binding for `procedure.md`. Source: Cloudflare Docs Gateway rules API reference, "DNS
policies", "Network policies", "HTTP policies", and "Common DNS policies" (retrieved 2026-10-23).
Base URL: `https://api.cloudflare.com/client/v4`. All calls send `Authorization: Bearer <API_TOKEN>`.
`{account_id}` and `{rule_id}` are placeholders. Token permission required per call: not documented.

## Calls

| Procedure operation | Method and path | Notes |
|---|---|---|
| List rules | `GET /accounts/{account_id}/gateway/rules` | Returns every rule type; group by `filters`. |
| Get rule | `GET /accounts/{account_id}/gateway/rules/{rule_id}` | |
| Create rule | `POST /accounts/{account_id}/gateway/rules` | Body fields below. `name` and `action` are required. |
| Update rule | `PUT /accounts/{account_id}/gateway/rules/{rule_id}` | Same body shape as create (assumption: full replacement). |
| Delete rule | `DELETE /accounts/{account_id}/gateway/rules/{rule_id}` | Not documented: response body. |

## Body fields

| Field | Meaning |
|---|---|
| `name` | Rule name (required) |
| `description` | Free text |
| `action` | See action values below (required) |
| `filters` | Array with exactly one value: `dns`, `l4` (network), or `http` (also `egress`, `dns_resolver`, out of scope) |
| `traffic` | Wirefilter expression for traffic matching; reformatted on save |
| `identity` | Wirefilter expression for user/group matching; empty string means any |
| `device_posture` | Wirefilter expression for posture checks |
| `precedence` | Evaluation order; lower runs first |
| `enabled` | `false` pauses the rule |
| `expiration` | `{expires_at, duration, expired}`; DNS rules only; overrides any schedule |
| `rule_settings` | Action-specific settings (below) |

## Action values by rule type

- DNS (`dns`): `allow`, `block`, `override`, `safesearch`, `ytrestricted`
- Network (`l4`): `allow`, `block`, `l4_override`
- HTTP (`http`): `allow`, `block`, `redirect`, `isolate`, `noisolate`, `off` (Do Not Inspect),
  `noscan` (Do Not Scan), `quarantine`

The action enum on the API page also lists `on`, `scan`, `resolve`, and `egress`, which this
procedure does not use. The HTTP Forward action appears in the policy docs as beta and is not in
that enum.

## `rule_settings` keys used by these rule types

`block_reason` (dns, l4, http block), `block_page_enabled` (dns block), `block_page`
(`{target_uri, include_context}`, http block), `notification_settings` (any block),
`override_host`, `override_ips` (dns override), `l4override` (`{ip, port}`, network override),
`redirect` (`{target_uri, include_context, preserve_path_and_query}`, http redirect), `quarantine`
(`{file_types}`, http), `check_session` (`{duration, enforce}`, l4/http allow), `add_headers`,
`delete_headers` (http allow; at most 20 header operations per rule), `payload_log`, `forensic_copy`
(http), `biso_admin_controls` (http isolate), `insecure_disable_dnssec_validation` (dns allow;
documented as insecure), `ip_categories`, `ip_indicator_feeds`, `ignore_cname_category_matches`
(dns). A setting applies only to the rule types and actions named; an incompatible one is a
configuration error (exact error text unknown).

## Response fields used

`id`, `version` (read-only), `read_only` (shared from a parent organization; not editable here),
`sharable`, `source_account`, `deleted_at`, `warning_status` (set when the rule is misconfigured),
plus the submitted fields in their stored form. Standard envelope: `success`, `errors[]`,
`messages[]`, `result`.

## Create body shape (placeholders only)

```json
{
  "name": "<RULE_NAME>",
  "description": "<DESCRIPTION>",
  "precedence": 100,
  "enabled": true,
  "action": "allow",
  "filters": ["dns"],
  "traffic": "any(dns.domains[*] in $<LIST_UUID>)",
  "identity": ""
}
```

Selector names (for example `dns.domains`, `dns.security_category`) and the full expression syntax
are not enumerated here; use the platform's selector reference for the rule type.

## Error text worth recognizing

Exact API error strings for these calls are not documented: unknown.
