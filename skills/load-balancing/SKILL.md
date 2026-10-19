---
name: load-balancing
description: Create, read, update, and delete load-balancer virtual server (VIP) and pool/pool-member objects on a supported load-balancing platform — currently F5 BIG-IP LTM (iControl REST), Citrix ADC/NetScaler (NITRO REST), HAProxy (config file + Runtime API), and Cloudflare Load Balancing (REST; hostname-based, with pools and monitors). A VIP configuration often references a certificate by identifier for TLS termination — provisioning that certificate is certificate-management's job, not this skill's; this skill only consumes the reference. Assumes an authenticated client for the target platform's API/CLI is already available; this skill does not provision or authenticate it.
argument-hint: "[platform] [action: create_vip|read_vip|update_vip|delete_vip|add_pool_member|remove_pool_member] [VIP/pool identifier, fields]"
---

# Load Balancing

Manages load-balancer virtual server (VIP) and pool/pool-member objects on whichever load-balancing
platform the caller is targeting, following that platform's own documented procedure exactly.

## When to use this skill

- Creating, reading, updating, or deleting a virtual server (VIP), or adding/removing/updating a pool
  member's state, on a supported platform.
- Not for issuing or renewing the TLS certificate a VIP terminates — see `certificate-management` for
  that. A VIP may *reference* a certificate by identifier, but provisioning that certificate is out of
  scope here.

## Universal concepts (shared load-balancing vocabulary, not a wire standard)

There is no wire-level standard grounding this capability (unlike, say, DNS) — the claims below are
verified against the four platforms currently listed in `references/INDEX.md` (F5 BIG-IP LTM, Citrix
ADC, HAProxy, Cloudflare Load Balancing), with the exceptions noted. Treat them as the current common
ground, not a guarantee that every future vendor added here will match:

- **A VIP is its own object, separate from the pool/backend of members it directs traffic to.** On the
  three appliance-style platforms it is identified by an address+port pair (F5 `ltm virtual`'s
  `destination`; Citrix `lbvserver`'s `ipv46`+`port`; HAProxy's `frontend`/`bind`) and the member side
  is a distinct object (F5 `ltm pool`; Citrix `service`; HAProxy `backend`/`server`). **Cloudflare is
  the exception to the address+port part:** its load balancer is identified by a DNS hostname with no
  listener address, and its pools are separate objects it references.
- **The VIP references its pool/backend by name/identifier — it does not embed member definitions
  directly.** F5's `pool` field, HAProxy's `default_backend`, Citrix's explicit
  `lbvserver_service_binding`, and Cloudflare's list of referenced pools are all references or
  bindings, never a single combined create.
- **A pool/backend member is defined by a target address (and usually a port).** How a platform
  identifies a member for update or removal differs (F5 member resource name, Citrix `service.ip`,
  HAProxy `server` line, Cloudflare an origin entry identified by its name within the pool) — see each
  platform's own `procedure.md`.
- **Every platform distinguishes disabling/draining a member from removing it**, with more than one
  documented flavor of "disabled" on most (F5's `session` vs. `state`; Citrix's graceful vs.
  non-graceful disable; HAProxy's maintenance/drain/health-down; Cloudflare's per-origin enabled flag
  versus removing the origin). Do not normalize these into one generic "disabled" status — report the
  specific mechanism actually used.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away, and don't conflate a pool member being disabled/drained with it being removed, on a platform
   that distinguishes them.

## Known limitations

- Currently covers F5 BIG-IP LTM, Citrix ADC/NetScaler, HAProxy, and Cloudflare Load Balancing — see `references/INDEX.md`
  for exact scope per vendor and known gaps. A platform not listed there needs a new reference
  file before this skill can be used for it.
- Does not cover certificate issuance/renewal, even where a VIP configuration references a
  certificate by identifier — see `certificate-management` for that.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed call mechanism detail — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates on
      destructive changes (VIP deletion, pool member removal from a live pool)
- [ ] Outcome reported using the platform procedure's own status vocabulary, distinguishing a
      disabled/drained pool member from a removed one where the platform makes that distinction
