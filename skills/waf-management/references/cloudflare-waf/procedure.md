# Cloudflare WAF — Custom Rules, Rate Limiting Rules, and Managed Ruleset Deployment (Zone)

Create, read, update, reorder, and delete zone-level WAF custom rules and rate limiting rules, and
deploy a Cloudflare managed ruleset with overrides. Source: Cloudflare Docs "Custom rules", "Create a
custom rule via API", "Rate limiting rules", "Rate limiting parameters", "Create a rate limiting rule
via API", "Managed Rules", "Deploy a WAF managed ruleset via API", "Override a managed ruleset",
"Actions", and the Ruleset Engine Rulesets API pages (retrieved 2026-10-27). Bind each operation
through `endpoints.md`, which also holds the field names.

Scope: the zone level and the request-phase WAF only. Account-level rulesets (Enterprise), exceptions
that skip managed rules, the `skip` action, Sensitive Data Detection (it runs in a separate response
phase), bot management, DDoS protection, API Shield, lists, payload logging, and Cloudflare's
deprecated Firewall Rules are not covered. Cloudflare's network-layer firewall uses the same Rulesets
API in other phases and belongs to `firewall-management`.

Each rule type lives in its own phase's entry point ruleset:

| Rule type | Phase |
|---|---|
| Custom rule | `http_request_firewall_custom` |
| Rate limiting rule | `http_ratelimit` |
| Managed ruleset deployment | `http_request_firewall_managed` |

Phases run in this order: HTTP DDoS protection, custom rules, rate limiting rules, managed rules. A
terminating action (block or a challenge) in an earlier phase stops later phases for that request.

## Common Sequences

1. **Add a rule:** Resolve the entry point ruleset, Create custom rule or Create rate limiting rule,
   Read rules to verify.
2. **Deploy a managed ruleset:** Resolve the entry point ruleset, Deploy managed ruleset, Read rules to
   verify, then Update rule to adjust overrides.
3. **Change a rule:** Resolve the entry point ruleset, Update rule (definition or position).
4. **Retire a rule:** Resolve the entry point ruleset, Delete rule.

## Resolve the entry point ruleset

1. Read the zone's entry point ruleset for the phase. Success returns the ruleset identifier and its
   rules in evaluation order. Keep the identifier, and the rule identifiers needed later.
2. A not-found response means the phase has no ruleset yet; only then create the ruleset, with the new
   rule in its rules list. When a ruleset already exists, add, update, and delete single rules instead,
   which leaves the other rules alone.

## Read rules

Reading the entry point ruleset again is the read operation: it lists each rule's identifier,
expression, action, enabled state, and order, plus the ruleset version. Use it before any change and
to verify after one.

## Create custom rule

1. Write the rule: a match expression in the Rules language, an action, and a description. Without a
   position the rule goes last. Rules run in order, and a terminating action ends evaluation for that
   request, so position decides whether a later rule ever applies.
2. Actions: `block`, `managed_challenge`, `js_challenge` (non-interactive), `challenge`
   (interactive), and `log` (Enterprise only). A block can return a custom response (status code,
   body, content type).
3. Plan limits for rules in the phase: 5 on Free, 20 on Pro, 100 on Business, 1,000 on Enterprise.
   Regular-expression matching needs Business or Enterprise.
4. **Stop and confirm with the operator before creating a rule whose action enforces (anything other
   than `log`)**, since it takes effect on live traffic at once (unless the operator's standing
   instructions pre-authorize it). Where the plan allows `log`, create the rule with `log` first,
   review the matches it records, then change the action; Cloudflare recommends this before a more
   severe action. On plans without `log`, Unverified: a non-enforcing mode for custom rules.
5. Success is a response holding the whole ruleset with the new rule, a new rule identifier, and a
   higher ruleset version. Report `CREATED` with the rule identifier.

## Create rate limiting rule

A rate limiting rule is a rule with an added rate configuration, in the rate limiting phase, and it
must come last in that phase's rule list.

1. Write the match expression and the action: `block`, `managed_challenge`, `js_challenge`,
   `challenge`, or `log`. A block can return a custom response with a status code from 400 to 499
   (default 429), a body up to 30 KB, and a JSON, HTML, XML, or plain-text content type.
2. Choose the rate configuration:
   - Counting identity: the data centre is always part of it. Add the client identity, either the
     source IP or "IP with NAT support" (a cookie-based visitor identity), never both. More identities
     (header, cookie, query value, host, path, ASN, country, fingerprints, body fields, a custom
     expression) depend on plan. Header names are lowercase. When an identity value can be missing,
     requests without it share their own counter unless the counting condition excludes them.
   - Period: 10, 60, 120, 300, 600, or 3600 seconds, narrowed by plan.
   - Request threshold for the period.
   - Mitigation duration: how long the action keeps applying once triggered, from 0 to 86,400 seconds.
     Zero means throttling: only requests above the limit receive the action. Outside Enterprise a
     challenge action must use zero, and only Enterprise can throttle with `block`.
   - Counting condition (optional): what increments the counter. It defaults to the match expression
     and is not combined with it automatically, so repeat the match condition in it when needed.
   - Origin-only counting (optional): ignore cached responses when counting.
3. Restrictions: the match expression cannot use response fields; custom lists in it require counting
   cached responses too; a counting condition cannot combine response fields and custom lists.
4. Plan limits: 1 rule on Free, 2 on Pro, 5 on Business, up to 100 on Enterprise with application
   security. Complexity-based counting is Enterprise with Advanced Rate Limiting only.
5. **Stop and confirm with the operator before creating a rule whose action enforces** (unless the
   operator's standing instructions pre-authorize it), as for custom rules.
6. Success is as for a custom rule. Report `CREATED`. Counters lag by a few seconds, so some excess
   requests can still reach the origin, and limiting verified bots can affect search indexing.

## Deploy managed ruleset

1. Pick the ruleset by plan: the Free Managed Ruleset on every plan; the Cloudflare Managed Ruleset and
   the OWASP Core Ruleset from Pro. A zone can deploy each ruleset once. The Free ruleset adds nothing
   when the Cloudflare Managed Ruleset is deployed.
2. Add one rule to the managed phase's entry point ruleset that executes the ruleset by identifier,
   with an expression covering all traffic or a narrower one. The version resolves to the latest.
3. Overrides can be set at three levels: the whole ruleset, a tag, or one rule by identifier. A rule
   override wins over a tag override, which wins over a ruleset override. The overridable properties
   are the action and the enabled state. Ruleset and tag overrides also change rules Cloudflare adds
   to the ruleset later, so use rule identifiers when the change must stay fixed.
4. For a first deployment, override the ruleset's action to `log` so matches are recorded without
   enforcement, then tighten after review. `log` is Enterprise only; on other plans Unverified: a
   non-enforcing mode. **Stop and confirm with the operator before deploying with enforcing actions**
   (unless the operator's standing instructions pre-authorize it).
5. Request bodies are inspected only up to a plan-dependent size (128 KB Enterprise, 1 MB Free, lower
   by default on other paid plans); the remainder may go unanalysed.
6. Success is the entry point read showing the execute rule enabled with the ruleset identifier and
   the intended overrides. Report `DEPLOYED`.

## Update rule

1. Read the rule first. An update replaces the rule definition, so send every field that should
   remain, not only the changed one. Each update creates a new ruleset version.
2. Changing the order uses the same call with a position (before, after, or an index).
3. To change overrides on an existing managed deployment, the documented method is the update-ruleset
   operation on the entry point ruleset; Assumption: updating the single execute rule works as well.
4. **Stop and confirm with the operator before an update that weakens enforcement** (lowering an
   action to `log`, widening an exclusion, or disabling a ruleset) (unless the operator's standing
   instructions pre-authorize it).
5. Success is the changed rule in the returned ruleset. Report `UPDATED`.

## Delete rule

1. Show the operator the rule being removed: its expression, action, and phase, and record its full
   definition; the delete response returns only the remaining ruleset.
2. **Stop and confirm with the operator before deleting a rule**, especially a managed ruleset
   deployment or a rate limiting rule protecting a login or API path, since protection ends
   immediately (unless the operator's standing instructions pre-authorize it).
3. Success is a response returning the remaining ruleset without that rule. Report `DELETED`.

## Patterns

- Custom, rate limiting, and managed rules live in separate phases and cannot share a ruleset.
- Rate limiting is approximate; it does not hold the origin to an exact request count.

## Known limitations

- Account-level rulesets, exceptions, `skip`, Sensitive Data Detection, bot management, and DDoS
  protection are not covered.
- Not documented: rate limits for these calls; on an HTTP 429, back off and honor any `Retry-After`
  header.
- Unverified: a documented way to disable a rule without deleting it, other than a managed override's
  enabled state.

## Tools

| Operation | Description | Category |
|---|---|---|
| Get entry point ruleset | Read a phase's ruleset and rule order | Rulesets API (zone) |
| Create ruleset | Create a phase's ruleset when none exists | Rulesets API (zone) |
| Add rule | Add a custom, rate limiting, or execute rule | Rulesets API (zone) |
| Update rule | Replace a rule's definition or position | Rulesets API (zone) |
| Update ruleset | Replace a phase's ruleset, used for managed overrides | Rulesets API (zone) |
| Delete rule | Remove one rule | Rulesets API (zone) |

## Verification checklist

- [ ] The entry point ruleset for the phase was read before any write, and the create-ruleset call was
      used only when the phase had none
- [ ] The rule sits in the right phase and position, and the plan limit was checked
- [ ] Rate limiting rules: the identity includes the data centre and one client identity, the period and
      duration are valid for the plan, and the rule is last
- [ ] Enforcing rules, managed deployments, and weakening updates were confirmed with the operator
- [ ] The entry point read after the change shows the intended rule and overrides
- [ ] Before deleting a rule: confirmed with the operator and its definition recorded
- [ ] Outcome reported with this procedure's status vocabulary (`CREATED`, `UPDATED`, `DEPLOYED`,
      `DELETED`, `FAILED`)
