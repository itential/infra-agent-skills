---
name: certificate-management
description: Issue, renew, read, and revoke TLS/SSL certificates, and where a platform documents it set up the certificate authority and issuance roles, on a supported certificate-management platform or protocol — currently the ACME protocol (e.g. Let's Encrypt), HashiCorp Vault's PKI secrets engine, AWS Certificate Manager, DigiCert ONE Trust Lifecycle Manager, and Sectigo Certificate Manager. Use when an agent needs to manage certificate lifecycle itself, distinct from installing/binding an already-issued certificate to a specific application, device, or load-balancer VIP (that binding step belongs to the consuming platform's own skill, e.g. load-balancing). Assumes an authenticated client/credential for the target platform's API is already available; this skill does not provision or authenticate it. See references/INDEX.md for the full vendor/protocol list.
argument-hint: "[platform] [action: issue|renew|read|revoke] [certificate identifier/CSR, fields]"
---

# Certificate Management

Manages TLS/SSL certificate lifecycle — issuance, renewal, inspection, revocation — on whichever
certificate-management platform or protocol the caller is targeting, following that platform's own
documented procedure exactly.

## When to use this skill

- Issuing, renewing, reading (expiry, SANs, chain), or revoking a certificate on a supported
  platform/protocol.
- Where a platform's reference documents it (Vault PKI today): creating a certificate authority
  and defining or changing issuance roles.
- Not for installing or binding an already-issued certificate to a specific consuming system — e.g.
  binding a certificate to a load-balancer VIP is `load-balancing`'s concern, not this skill's; this
  skill's job ends at producing/managing the certificate itself.

## Universal concepts (shared certificate-management vocabulary, not a wire standard)

No wire-level standard grounds every platform in this category the way, say, RFC 1035/2136 grounds
DNS — the ACME protocol (RFC 8555) is itself a standard, but Vault PKI, AWS ACM, DigiCert, and Sectigo are each a
vendor-specific API with no shared protocol underneath them. The claims below hold for the platforms checked;
DigiCert and Sectigo details are partly unverified (see their procedure files). Re-check every one
of them against a new platform's actual behavior before assuming it still holds (see `AGENTS.md` rule
4) — several plausible-sounding claims did NOT survive checking every platform and are deliberately left
out below (see each platform's own `procedure.md` "Patterns"/"Known limitations" for specifics):

- **Revocation is generally permanent; a hold or suspension, where a platform offers one, may be
  reversible.** No platform documents reversing a revocation made for any other reason, and the
  remedy is issuing a replacement certificate. Confirm which reasons are reversible in the
  platform's own `procedure.md`. This is why every platform's procedure gates revocation on
  explicit operator confirmation.
- **"Renewal" is not one consistent mechanism across platforms — confirm which pattern a given
  platform actually uses before assuming behavior.** The ACME protocol and Vault's PKI engine have no
  dedicated renewal call at all (renewing is just issuing again); AWS ACM has both an automatic
  managed-renewal mechanism and a separate explicit `RenewCertificate` action with its own narrower
  eligibility rules. Do not assume a "renew" step exists as a distinct wire operation, or that a
  certificate's identifier is preserved across renewal, until that platform's own `procedure.md`
  confirms it either way.
- **Where a platform generates the private key on the caller's behalf, capturing it at issuance time
  is a one-time opportunity, not something guaranteed retrievable later** — confirmed explicitly for
  Vault PKI's issue call; check this against any platform that offers server-side key
  generation rather than assuming AWS ACM's fully-managed-key model (where the caller never handles
  the private key at all) is how every platform works. Where a platform offers optional key
  escrow, one-time capture may not apply.

See `references/INDEX.md` for which platforms/protocols have a procedure, and each platform file for
how it implements this shape concretely.

## Procedure

1. **Identify the target platform/protocol** — from the caller's request or the `platform` argument.
   Check `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist.
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize it
   away, and don't conflate a renewed certificate with a newly issued one, on a platform that
   distinguishes them (e.g. serial number/identifier continuity).

## Known limitations

- Currently covers the ACME protocol (e.g. Let's Encrypt), HashiCorp Vault's PKI secrets engine, AWS
  Certificate Manager, DigiCert ONE Trust Lifecycle Manager, and Sectigo Certificate Manager — see `references/INDEX.md`. A platform not listed there needs a new
  reference file before this skill can be used for it.
- Does not cover installing/binding an issued certificate to a consuming application, device, or load
  balancer — that belongs to the consuming system's own skill.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific procedure changes — a new error
code, a corrected field, a changed call mechanism detail — belong in that platform's own
`references/<platform>/procedure.md`, never here.

## Tools

Each platform assumes its own authenticated client/credential — see `references/INDEX.md` for which,
and that platform's `procedure.md` for the specific operations.

## Verification checklist

- [ ] Target platform/protocol confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates on
      destructive changes (revocation, which is generally irreversible)
- [ ] Outcome reported using the platform procedure's own status vocabulary, distinguishing a renewed
      certificate from a newly issued one where the platform makes that distinction
