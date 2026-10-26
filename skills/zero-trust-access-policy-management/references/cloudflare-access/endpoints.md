# Cloudflare One Access — Reusable Policy Endpoints

Wire-level binding for `procedure.md`. Source: Cloudflare Docs Access reusable policies API
reference and "Manage Access policies" (retrieved 2026-10-26). Base URL:
`https://api.cloudflare.com/client/v4`. All calls send `Authorization: Bearer <API_TOKEN>`.
`{account_id}`, `{policy_id}`, and `{app_id}` are placeholders.

## Calls

| Procedure operation | Method and path | Token permission |
|---|---|---|
| List policies | `GET /accounts/{account_id}/access/policies` | `Access: Apps and Policies Read` or `Write` |
| Get policy | `GET /accounts/{account_id}/access/policies/{policy_id}` | Read or Write |
| Create policy | `POST /accounts/{account_id}/access/policies` | `Access: Apps and Policies Write` |
| Update policy | `PUT /accounts/{account_id}/access/policies/{policy_id}` | Write |
| Delete policy | `DELETE /accounts/{account_id}/access/policies/{policy_id}` | Write |
| Convert legacy policy | `PUT /accounts/{account_id}/access/apps/{app_id}/policies/{policy_id}/make_reusable` | Write; send an empty body |

List query parameters: `page`, `per_page` (maximum 1000). `{account_id}` is at most 32 characters
and `{policy_id}` at most 36.

## Body fields (create and update)

Required: `name`, `decision`, `include`.

- `decision`: `allow` (Allow), `deny` (Block), `non_identity` (Service Auth), `bypass` (Bypass).
- `include`, `require`, `exclude`: arrays of rule objects (below). Include is OR, Require is AND,
  Exclude is NOT.
- `session_duration`: string such as `300ms` or `2h45m` (units ns, us, ms, s, m, h).
- `isolation_required`: boolean; needs client web isolation on for the account.
- `purpose_justification_required` (boolean) and `purpose_justification_prompt` (string).
- `approval_required` (boolean) and `approval_groups`: array of `{approvals_needed, email_addresses,
  email_list_uuid}`.
- `mfa_config`: `{mfa_disabled, allowed_authenticators, session_duration}`. The schema lists
  `totp`, `biometrics`, `security_key`; the MFA guide also names `piv_key` and `ssh_fido2_key` for
  infrastructure applications. `session_duration` here is minutes or hours (`5m`, `24h`, maximum
  `720h`); `0m` means every login (stated for the application-level setting).
- `connection_rules.rdp`: `allowed_clipboard_local_to_remote_formats` and
  `allowed_clipboard_remote_to_local_formats`, each a list of `text` and/or `file`.
- Unverified: the field that carries allowed UNIX usernames for infrastructure (SSH) applications is
  not in the API schema.
- Unverified: whether update replaces or merges; the procedure assumes replace.

## Rule objects

| Selector | Object |
|---|---|
| Emails | `{"email": {"email": "<address>"}}` |
| Emails ending in | `{"email_domain": {"domain": "<domain>"}}` |
| Email list | `{"email_list": {"id": "<list_id>"}}` |
| IP ranges | `{"ip": {"ip": "<CIDR>"}}` |
| IP list | `{"ip_list": {"id": "<list_id>"}}` |
| Country | `{"geo": {"country_code": "<code>"}}` |
| Everyone | `{"everyone": {}}` |
| Rule group | `{"group": {"id": "<group_id>"}}` |
| Valid certificate | `{"certificate": {}}` |
| Common name | `{"common_name": {"common_name": "<name>"}}` |
| Service token | `{"service_token": {"token_id": "<id>"}}` |
| Any service token | `{"any_valid_service_token": {}}` |
| Linked app token | `{"linked_app_token": {"app_uid": "<id>"}}` |
| Login method | `{"login_method": {"id": "<idp_id>"}}` |
| Authentication method | `{"auth_method": {"auth_method": "<RFC 8176 value>"}}` |
| Device posture | `{"device_posture": {"integration_uid": "<id>"}}` |
| User risk score | `{"user_risk_score": {"user_risk_score": ["low","medium","high","unscored"]}}` |
| External evaluation | `{"external_evaluation": {"evaluate_url": "<url>", "keys_url": "<url>"}}` |
| Cloudflare account member | `{"cloudflare_account_member": {"account_id": "<id>"}}` |
| Okta group | `{"okta": {"identity_provider_id": "<id>", "name": "<group>"}}` |
| Azure group | `{"azureAD": {"id": "<group_id>", "identity_provider_id": "<id>"}}` |
| Azure auth context | `{"auth_context": {"id": "<id>", "ac_id": "<acid>", "identity_provider_id": "<id>"}}` |
| GitHub organization | `{"github-organization": {"identity_provider_id": "<id>", "name": "<org>", "team": "<team>"}}` |
| Google Workspace group | `{"gsuite": {"email": "<group email>", "identity_provider_id": "<id>"}}` |
| SAML group | `{"saml": {"attribute_name": "<n>", "attribute_value": "<v>", "identity_provider_id": "<id>"}}` |
| OIDC claim | `{"oidc": {"claim_name": "<n>", "claim_value": "<v>", "identity_provider_id": "<id>"}}` |

The Warp and Gateway selectors in the dashboard have no object in the API schema; their wire
form is unverified.

## Response fields

`id`, `account_id`, `app_count` (applications using the policy), `reusable` (true), `created_at`,
`updated_at`, `precedence` (optional; documented as the order of execution, unique per policy; not accepted in create or update bodies, and its relation to per-application order is unverified), plus the submitted fields. Delete returns `result.id`. Envelope: `success`, `errors[]`,
`messages[]`, `result`; list responses add pagination info.

## Placeholder bodies

Allow an email domain:

```json
{"name": "Allow team", "decision": "allow", "include": [{"email_domain": {"domain": "example.com"}}], "session_duration": "24h"}
```

Service Auth with a service token, restricted to a source range:

```json
{"name": "Service auth", "decision": "non_identity", "include": [{"service_token": {"token_id": "<SERVICE_TOKEN_ID>"}}], "require": [{"ip": {"ip": "192.0.2.0/24"}}]}
```

## Error text worth recognizing

Exact API error strings for these calls are not documented: unknown.
