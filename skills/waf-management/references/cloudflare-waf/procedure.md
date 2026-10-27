# Cloudflare WAF — Custom Rules, Rate Limiting Rules, and Managed Ruleset Deployment (Zone)

Create, read, update, disable, and delete zone-level WAF custom rules and rate limiting rules, and
deploy a Cloudflare managed ruleset with overrides. Source: Cloudflare Docs "Custom rules", "Create a
custom rule via API", "Rate limiting rules", "Rate limiting parameters", "Create a rate limiting rule
via API", "Managed Rules", "Deploy a WAF managed ruleset via API", "Override a managed ruleset",
"Actions", and the Ruleset Engine Rulesets API pages (retrieved 2026-10-27). Bind each operation
through `endpoints.md`.

Scope: the zone level only. Account-level rulesets (Enterprise), exceptions that skip managed rules,
bot management, DDoS protection, API Shield, lists, payload logging, and Cloudflare's deprecated
Firewall Rules are not covered. Cloudflare's network-layer firewall (layer 3/4) uses the same Rulesets
API in different phases and belongs to `firewall-management`.

All three rule types are rules in a phase's entry point ruleset, one phase per type:

| Rule type | Phase |
|---|---|
| Custom rule | `http_request_firewall_custom` |
| Rate limiting rule | `http_ratelimit` |
| Managed ruleset deployment | `http_request_firewall_managed` |

Evaluation runs in this order: HTTP DDoS protection, custom rules, rate limiting rules, then managed
rules. A terminating action (block or a challenge) in an earlier phase stops later phases for that
request.

## Common Sequences

1. **Add a custom rule:** Resolve the entry point ruleset, Create custom rule, Verify.
2. **Add a rate limiting rule:** Resolve the entry point ruleset, Create rate limiting rule, Verify.
3. **Deploy a managed ruleset:** Resolve the entry point ruleset, Deploy managed ruleset (in log mode
   where available), Verify, then Tune overrides.
4. **Change or retire a rule:** Resolve the entry point ruleset, Update rule or Disable rule, or Delete
   rule.

## Resolve the entry point ruleset

1. Read the zone's entry point ruleset for the phase. A successful read returns the ruleset
   identifier and its rules in evaluation order; keep the identifier for later steps.
2. A not-found response means the phase has no ruleset yet. Only then create the ruleset, with the new
   rule in its rules list. When a ruleset exists, never use the create-ruleset call: add, update, and
   delete work on single rules and leave the others untouched.
3. Success is the ruleset identifier and rule list in hand. An existing rule's identifier is needed
   for update, disable, and delete.

## Create custom rule

1. Write the rule: a match expression in the Rules language, an action, and a description. Optional
   `position` places the rule; with none it goes last. Order matters, because rules run in sequence and
   a terminating action ends evaluation for that request.
2. Actions: `block`, `managed_challenge`, `js_challenge` (non-interactive), `challenge` (interactive),
   `skip`, and `log`. `log` is available only on Enterprise plans. A block can carry a custom response
   (status code, body, content type) in `action_parameters`.
3. Plan limits for the phase, counting all rules there: 5 rules on Free, 20 on Pro, 100 on Business,
   1,000 on Enterprise. Regular-expression matching needs Business or Enterprise.
4. Success is a response holding the whole ruleset with the new rule present and enabled, a new rule
   identifier, and a higher ruleset version. Report `CREATED` with the rule identifier.
5. To check a rule before it enforces, create it with `log` where the plan allows it, review the logged
   matches, then change the action. On plans without `log`, Unverified: a non-enforcing mode for custom
   rules.

## Create rate limiting rule

A rate limiting rule is a rule plus a `ratelimit` object, in the `http_ratelimit` phase. Rate limiting
rules must be last in the phase's rule list.

1. Write the match expression and the action: `block`, `managed_challenge`, `js_challenge`,
   `challenge`, or `log`. A block can carry a custom response with a status code from 400 to 499
   (default 429), a content type of JSON, HTML, XML, or plain text, and a body up to 30 KB.
2. Set the `ratelimit` object:
   - `characteristics`: what defines one counter. It must include `cf.colo.id` (data centre). Add the
     client identity: `ip.src`, or `cf.unique_visitor_id` for "IP with NAT support" (the two cannot be
     combined). Further characteristics (header, cookie, query value, host, path, ASN, country,
     fingerprints, body fields, a custom expression) depend on plan. A header name must be lowercase.
     When a header, cookie, or similar characteristic is used and may be absent, the requests that lack
     it share their own counter unless the counting expression excludes them.
   - `period` in seconds: `10`, `60`, `120`, `300`, `600`, or `3600`, narrowed by plan.
   - `requests_per_period`: the count that triggers the rule.
   - `mitigation_timeout` in seconds: how long the action keeps applying after the trigger (values `0`,
     `10`, `60`, `120`, `300`, `600`, `3600`, `86400`, narrowed by plan). `0` means throttle: only the
     requests over the limit receive the action. Outside Enterprise, a challenge action must use `0`,
     and only Enterprise can throttle with `block`.
   - Optional `counting_expression`: what increments the counter. It defaults to the match expression
     and does not extend it, so repeat the match condition in it when needed. Response fields are allowed
     only on plans that support them.
   - Optional `requests_to_origin` set true: count only requests that reach the origin, not cached ones.
3. Restrictions: the match expression cannot use response fields; custom lists in the match expression
   require counting cached assets too; a counting expression cannot combine response fields with lists.
4. Plan limits: 1 rule on Free, 2 on Pro, 5 on Business, up to 100 on Enterprise with application
   security. Complexity-based counting (`score_per_period`, `score_response_header_name`) is Enterprise
   with Advanced Rate Limiting only.
5. Success is the same as for custom rules. Report `CREATED`. Counters update with a short delay, so
   some excess requests can reach the origin before the action starts.

## Deploy managed ruleset

1. Pick the managed ruleset by plan: the Free Managed Ruleset on every plan; the Cloudflare Managed
   Ruleset and the OWASP Core Ruleset from Pro; Sensitive Data Detection on Enterprise only. Each
   ruleset can be deployed once per zone. The Free ruleset is redundant when the Cloudflare Managed
   Ruleset is deployed.
2. Add one rule to the managed phase's entry point ruleset: action `execute`, `action_parameters`
   naming the managed ruleset identifier, expression `true` to cover all traffic (or a narrower
   expression), and a description. The version resolves to the latest.
3. Managed rules inspect a request body only up to a plan limit (128 KB Enterprise, 1 MB Free; lower by
   default on other paid plans), so content beyond it may not be fully analysed.
4. Overrides ride in `action_parameters.overrides` of the execute rule, at three levels: the whole
   ruleset, a tag (`categories`), or a single rule by identifier. The rule level beats the tag level,
   which beats the ruleset level. Overridable properties are `action` and `enabled`. Ruleset and tag
   overrides also apply to rules Cloudflare adds later; use rule overrides to touch only existing
   rules.
5. For a first deployment, override the ruleset's action to `log` so matches are recorded without
   enforcement, then tighten after reviewing. `log` is Enterprise only; for other plans Unverified:
   a non-enforcing mode.
6. Success is the response showing the execute rule enabled with the ruleset identifier. Report
   `DEPLOYED`.

## Update rule

1. Read the rule first. An update replaces the rule definition, so send every field that should
   remain, not only the changed one. Each update makes a new ruleset version.
2. Position changes use the same call with a `position` of `before`, `after`, or `index`.
3. Success is the changed rule in the returned ruleset. Report `UPDATED`.

## Disable rule

Setting `enabled` to false keeps the rule and stops it matching. This is the reversible alternative to
deleting. For a managed deployment, disabling the execute rule stops that whole ruleset.
**Stop and confirm with the operator before disabling a rule that is the only protection for a
service** (unless the operator's standing instructions pre-authorize it).

## Delete rule

1. Show the operator the rule being removed: its expression, action, and phase.
2. **Stop and confirm with the operator before deleting a rule**, especially a managed ruleset
   deployment or a rate limiting rule protecting a login or API path, since protection ends immediately
   (unless the operator's standing instructions pre-authorize it).
3. Success is a response returning the remaining ruleset without that rule. Report `DELETED`.

## Patterns

- Custom, rate limiting, and managed rules live in separate phases and cannot share a ruleset.
- Rate limiting is approximate: it does not guarantee an exact request count reaches the origin.
- Applying rate limiting to verified bots can affect search engine optimization.
- Ruleset and tag overrides apply to rules Cloudflare adds later, not only to the current rules.
- Prefer a reversible action (`log`, `managed_challenge`) when a rule is first created, then tighten.

## Known limitations

- Account-level rulesets, WAF exceptions, bot management, and DDoS protection are not covered.
- Unverified: whether the dry-run query parameter applies to these phases.
- Unverified: the token permission needed for reads; the writes are documented as `Zone WAF Write`.
- Not documented: rate limits for these calls; on an HTTP 429, back off and honor any `Retry-After`
  header.
- Record a rule's full definition before deleting it; the delete response returns only the remaining
  ruleset.

## Tools

| Operation | Description | Category |
|---|---|---|
| Get entry point ruleset | Read a phase's ruleset and rule order | Rulesets API (zone) |
| Create ruleset | Create a phase's ruleset when none exists | Rulesets API (zone) |
| Add rule | Add a custom, rate limiting, or execute rule | Rulesets API (zone) |
| Update rule | Replace a rule's definition, enabled state, or position | Rulesets API (zone) |
| Delete rule | Remove one rule | Rulesets API (zone) |

## Verification checklist

- [ ] The entry point ruleset for the phase was read before any write, and the create-ruleset call was
      used only when the phase had none
- [ ] The rule sits in the right phase and position, and any plan limit was checked
- [ ] Rate limiting rules: characteristics include the data centre and the client identity, the period
      and timeout are valid for the plan, and the rule is last
- [ ] New enforcing rules started with a reversible action where the plan allows
- [ ] A managed deployment reads back enabled with the intended overrides
- [ ] Before deleting a rule or disabling a sole protection: confirmed with the operator
- [ ] Outcome reported with this procedure's status vocabulary (`CREATED`, `UPDATED`, `DEPLOYED`,
      `DELETED`, `FAILED`)
