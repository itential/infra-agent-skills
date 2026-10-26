---
name: waf-management
description: Create, read, update, and delete web application firewall (WAF) rules, rate-limit rules, and managed-ruleset bindings on a supported platform. Application-layer/HTTP rule management, distinct from firewall-management's network-layer rules and NAT — even where the same vendor offers both. Assumes an authenticated client for the target platform's API is already available; this skill does not provision or authenticate it. No vendor coverage yet — see references/INDEX.md.
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

No vendor is listed yet, so no claims are stated as shared. Do not assume any shared behavior for a
platform until its own procedure exists.

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

- No vendor coverage yet — see `references/INDEX.md`. A platform not listed there needs a new
  reference file before this skill can be used for it.
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
