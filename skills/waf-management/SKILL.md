---
name: waf-management
description: Create, read, update, and delete web application firewall (WAF) rules, rate-limit rules, and managed-ruleset bindings on a supported platform (Cloudflare WAF). Application-layer/HTTP rule management, distinct from firewall-management's network-layer rules and NAT — even where the same vendor offers both. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it.
argument-hint: "[platform] [action: create_rule|read_rule|update_rule|delete_rule|bind_managed_ruleset] [rule/ruleset identifier, fields]"
---

# WAF Management

Manages web application firewall rules, rate-limit rules, and managed-ruleset bindings on whichever
platform the caller is targeting, following that platform's own documented procedure exactly.

## When to use this skill

- Creating, reading, updating, or deleting a WAF rule, rate-limit rule, or a managed-ruleset
  binding (e.g. enabling a vendor-curated OWASP ruleset) on a supported platform.
- Not for network-layer firewall rules or NAT — see `firewall-management` for that. A platform may
  offer both under one product line (Cloudflare, F5, Palo Alto all do); this skill covers only the
  HTTP/application-layer rule object, never the network ACL.

## Universal concepts (shared WAF vocabulary, not a wire standard)

Only one platform is listed, so each claim below holds only where that platform documents it.

- **A rule pairs a match expression with an action and is evaluated in order.** Where documented, some
  actions end evaluation for that request, so position decides whether a rule ever applies.
- **Rate-limit rules count requests by a chosen identity over a period.** Where documented, the action
  applies once the count passes the limit, and counting is approximate rather than exact.
- **A managed ruleset is a vendor-curated rule group bound to the application with optional
  overrides.** Where documented, its availability depends on the plan.
See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away.

## Known limitations

- Platform coverage is exactly the platforms in `references/INDEX.md`; a platform not listed there
  needs a new reference file before this skill can be used for it.
- Does not cover network-layer firewall rules or NAT, even where the same vendor/product offers
  both — see `firewall-management` for that.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed API path — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates on
      destructive changes (rule deletion, ruleset unbinding that removes active protection)
- [ ] Outcome reported using the platform procedure's own status vocabulary
