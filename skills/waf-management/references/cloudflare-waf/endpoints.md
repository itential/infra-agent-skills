# Cloudflare WAF — Endpoint Wiring

Wire-level binding for `procedure.md`. Source: Cloudflare Docs "Create a custom rule via API", "Create a
rate limiting rule via API", "Rate limiting parameters", "Deploy a WAF managed ruleset via API",
"Override a managed ruleset", "Actions", and the Rulesets API rule pages (retrieved 2026-10-27). Base
URL: `https://api.cloudflare.com/client/v4`. All calls send `Authorization: Bearer <API_TOKEN>`.
`{zone_id}`, `{ruleset_id}`, `{rule_id}`, and `{phase}` are placeholders.

Phases: `http_request_firewall_custom`, `http_ratelimit`, `http_request_firewall_managed`.

## Calls

| Procedure operation | Method and path | Notes |
|---|---|---|
| Get entry point ruleset | `GET /zones/{zone_id}/rulesets/phases/{phase}/entrypoint` | 200 with the ruleset and ordered rules, 404 when the phase has no ruleset |
| Create ruleset | `POST /zones/{zone_id}/rulesets` | Only when the entry point read returned 404; body has `name`, `kind` `zone`, `phase`, `rules[]` |
| Add rule | `POST /zones/{zone_id}/rulesets/{ruleset_id}/rules` | Optional `position`; returns the whole ruleset |
| Update rule | `PATCH /zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}` | Send all fields to keep, or only `position`; new ruleset version |
| Update managed overrides (documented method) | `PUT /zones/{zone_id}/rulesets/{ruleset_id}` | Replaces the entry point ruleset including the execute rule and its `overrides`; send every rule to keep |
| Delete rule | `DELETE /zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}` | 200 with the remaining ruleset |

Token permissions: `Zone WAF Read` (documented for the entry point read) and `Zone WAF Write`
(documented for add and update). Unverified: the permission listed for the delete call.

## Rule fields

- `expression` and `action` (required), `description`, `enabled`, `ref`.
- `action`: `block`, `managed_challenge`, `js_challenge`, `challenge`, `log` (Enterprise only),
  `execute` (managed deployment).
- `action_parameters` for a custom response on `block`: `response` with `status_code`, `content`,
  `content_type`. For a rate limiting rule the status code must be 400 to 499 (default 429), the
  content type one of `application/json`, `text/html`, `text/xml`, `text/plain`, and the content up to
  30 KB.
- `position`: exactly one of `{"before": "<rule_id>"}`, `{"after": "<rule_id>"}`, `{"index": <n>}`.

## Rate limiting object

`ratelimit`: `characteristics[]`, `period`, `requests_per_period`, `mitigation_timeout`, optional
`counting_expression` (empty string means the match expression), optional `requests_to_origin`,
and for complexity-based counting `score_per_period` and `score_response_header_name`.

| Characteristic | API value |
|---|---|
| Data centre (required) | `cf.colo.id` |
| IP | `ip.src` |
| IP with NAT support | `cf.unique_visitor_id` (not with `ip.src`) |
| Header | `http.request.headers["<lowercase-name>"]` |
| Cookie | `http.request.cookies["<name>"]` |
| Query value | `http.request.uri.args["<name>"]` |
| Host, path | `http.host`, `http.request.uri.path` |
| ASN, country | `ip.src.asnum`, `ip.src.country` |

Further characteristics (JA3/JA4 fingerprints, JSON, form, JWT, body, clearance, custom) exist on
higher plans. API values: `period` 10, 60, 120, 300, 600, 3600; `mitigation_timeout` 0, 10, 60, 120, 300, 600, 3600,
86400, both narrowed by plan. The plan availability table lists a longer set of period values (up to
65535 seconds); Unverified: whether the API accepts them.

## Managed deployment

Execute rule: `action` `execute`, `expression` `true`, `action_parameters` `id` (managed ruleset
identifier) and optionally `overrides`. Overrides: ruleset-level `action` and `enabled`; `categories`
(each `category` tag plus `action` or `enabled`); `rules` (each `id` plus `action` or `enabled`).
Cloudflare Managed Ruleset identifier: `efb7b8c949ac4650a09736fc376e9aee`. Only the identifier suffixes of the
other rulesets are documented (OWASP Core `...c25d2f1f`, Exposed
Credentials Check `...14069605`, Free `...dfb893ba`, Sensitive Data Detection `...499d988e`).
Unverified: how to list the full identifiers through the API.

## Placeholder bodies

Challenge rule:

```json
{"description": "Example custom rule", "expression": "(ip.src.country eq \"XX\") and cf.waf.score lt 20", "action": "managed_challenge"}
```

Rate limiting rule:

```json
{"description": "Example rate limit", "expression": "(http.request.uri.path matches \"^/api/\")", "action": "block",
 "ratelimit": {"characteristics": ["cf.colo.id", "ip.src"], "period": 60, "requests_per_period": 100, "mitigation_timeout": 600}}
```

Managed deployment in log mode (Enterprise):

```json
{"action": "execute", "expression": "true", "description": "Execute the Cloudflare Managed Ruleset",
 "action_parameters": {"id": "efb7b8c949ac4650a09736fc376e9aee", "overrides": {"action": "log"}}}
```

## Error text worth recognizing

Not documented: an error catalogue for these calls. Surface the returned
`errors` array unchanged. A 404 on the entry point read means the phase has no ruleset yet.
