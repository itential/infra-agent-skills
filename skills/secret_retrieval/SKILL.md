---
name: secret_retrieval
description: Read, create, update, or rotate a single secret value (API key, password, token, credential) held in a secrets-management platform — HashiCorp Vault (KV v1/v2), 1Password (Connect API), CyberArk Conjur, CyberArk Privilege Cloud, AWS Secrets Manager, or Azure Key Vault. Use when an agent or automation needs to fetch a secret's current value for use elsewhere, store a new value under an existing secret, or trigger/confirm a rotation. Assumes an authenticated client (token, API key, or OAuth session) for the target platform is already available; this skill does not provision or bootstrap that credential. Does not cover PKI certificate issuance (see certificate_management) or configuring a secrets engine/vault/mount itself (enabling KV, creating a Key Vault instance, defining a Conjur policy) — scoped strictly to reading or writing the value of a secret that already has a place to live.
argument-hint: "[platform] [action] [secret_path_or_id] [value_or_field]"
---

# Secret Retrieval

Reads, creates, updates, or rotates a secret's value on one of the supported secrets-management
platforms, following that platform's own documented API shape and access-control model
(`references/<platform>/procedure.md`).

## When to use this skill

- An automation needs the current value of a secret (API key, password, token, connection string)
  stored in Vault, 1Password, CyberArk Conjur, CyberArk Privilege Cloud, AWS Secrets Manager, or
  Azure Key Vault, in order to use it in a subsequent call.
- A secret's value needs to be created, overwritten, or rotated on one of those platforms.
- Not for issuing or renewing a PKI/TLS certificate — see `certificate_management`. Not for
  enabling a secrets engine, creating a vault/Key Vault instance, writing a Conjur policy, or any
  other one-time setup that makes a place for a secret to live — that's platform configuration,
  not secret retrieval, and is out of scope here.

## Universal concepts (apply regardless of platform)

- **A secret's value must never appear in plaintext in logs, error messages relayed upward, or
  audit trails an agent produces itself.** Every platform below either redacts the value from its
  own server-side audit log by design or explicitly warns not to pass it through channels that
  log request bodies — treat this as non-negotiable regardless of which platform is in play, and
  never echo a retrieved value back into a transcript, ticket, or chat message.
- **Every retrieval or write is an access-controlled operation, not an anonymous read.** All six
  platforms require an authenticated identity (a token, API key, or session) scoped with explicit
  permission to the specific secret/path/item, and all six generate some form of access record for
  that identity performing that action, though the exact audit mechanism differs (Vault audit
  device, CloudTrail, platform-native activity log).
- **Versioning is not universal — verify it per platform before relying on it.** Some platforms keep
  a version history a caller can address explicitly; others don't expose an equivalent
  caller-addressable version chain. Don't assume "read a specific prior version" is possible
  everywhere without checking that platform's own procedure first — see each platform's own
  `procedure.md` for exactly what it supports.
- **Overwriting or rotating a secret that's in active use is hard to reverse.** Every platform
  procedure below has its own confirmation gate on this — never skip it because the API call itself
  would succeed silently.

There is no single wire-level standard (no RFC) governing secrets-management APIs the way DNS has
RFC 1035 — each platform below defines its own request/response shape, so "universal concepts" here
are behavioral guarantees observed to hold across all six, not a shared protocol.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. If it
   isn't one of the six platforms in `references/INDEX.md`, stop: this skill doesn't cover it, and
   does not improvise a generic procedure for an unsupported platform.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it holds that platform's
   full operational procedure, error handling, patterns, known limitations, tools, and verification
   checklist. This file is intentionally just the router; the real steps live per platform because
   authentication, addressing, and versioning genuinely differ across all six (see
   `references/INDEX.md` for why).
3. **Report the outcome** using that platform procedure's own status vocabulary — don't normalize
   it away, and never include the secret's actual value in that report.

## Known limitations

- Does not cover PKI certificate issuance/renewal (see `certificate_management`) or any
  secrets-engine/vault/mount configuration step — every platform procedure here assumes the target
  secret already has a place to be stored (an existing KV mount/path, vault, safe, or resource) and
  the caller already has a scoped, authenticated credential for it.
- Does not cover bulk/batch export of many secrets at once beyond what a platform's own procedure
  documents as a single supported call (e.g. Conjur's batch-fetch endpoint, where in scope).
- Platform coverage is exactly the six vendors in `references/INDEX.md` — a platform not listed
  there needs a new `references/<platform>/procedure.md` before this skill can be used for it.

## Contributing to this skill

**`SKILL.md` itself should only ever change for two reasons: a bug in the universal concepts/router
logic above, or adding a pointer to a newly-supported platform.** Platform-specific procedure
changes — a new error code, a corrected field name, a changed API path — belong in that platform's
own `references/<platform>/procedure.md` and `endpoints.md`, never here. If you're about to add
vendor-specific detail to this file, put it in the platform's reference file instead.

## Tools

Each platform assumes its own authenticated client (a Vault token, a 1Password Connect token, a
Conjur access token, a Privilege Cloud session token, an AWS SigV4-signed client, or an Azure AD
OAuth token) — see `references/INDEX.md` for which, and that platform's `procedure.md` for the
specific operations/mechanisms.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates and
      error handling — not a generic/improvised sequence
- [ ] The secret's actual value was never written into a log, report, or status message produced by
      this skill's execution
- [ ] Outcome reported using the platform procedure's own status vocabulary
