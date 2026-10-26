# Cloudflare — DNS Zone Management Procedure

Create, read, and delete a Cloudflare zone, and understand the activation flow that brings a newly
created zone from pending to active. Covers the zone object itself — creation, setup-type choice, and
deletion — not the individual DNS records inside it, which the `dns-record-management` skill's
Cloudflare procedure covers separately. Assumes an authenticated Cloudflare API client (an API Token
with Zone Write scope, or legacy email+key headers) is already available to the caller.

Source: Cloudflare API reference (Zones resource) and Cloudflare's DNS zone-setup documentation,
developers.cloudflare.com, retrieved 2026-09-17. Confidence is limited for exact error codes and
the subdomain-setup compatibility matrix; those are flagged explicitly below rather than stated as
certain.

## Operational procedure

### 1. Choose a zone setup type before creating

Cloudflare offers more than one way for a zone to relate to DNS authority for a domain — decide which
applies before creating:

- **Full (primary) setup** — Cloudflare becomes the domain's authoritative DNS provider outright. This
  is the default, most common case, available on every plan tier, and what the rest of this procedure
  assumes unless stated otherwise.
- **Partial (CNAME) setup** — the domain's existing DNS provider stays authoritative, and only
  specific subdomains are routed through Cloudflare's reverse proxy. Documented as available on
  Business and Enterprise plans only.
- **Zone transfer (secondary/primary via AXFR/IXFR)** — Cloudflare runs alongside another DNS provider
  across the entire zone (not just individual subdomains) for redundancy, and can act as either the
  primary or the secondary side of that transfer relationship. Documented as an Enterprise-only
  capability.
- **Subdomain (delegated child zone) setup** — a subdomain is managed as its own zone, independently of
  its parent zone, optionally under a different Cloudflare account, while inheriting some settings from
  the parent. Documented as Enterprise-only. The exact compatibility rules for which parent-zone-type +
  child-zone-type combinations are supported are not documented in the sources — treat that
  matrix as an unknown to confirm directly with Cloudflare's own setup docs before relying on it, rather
  than assuming any particular combination works.

If the caller's request doesn't specify a setup type, default to full (primary) setup — it's the only
one available on every plan and the one this procedure's later steps assume.

### 2. Create the zone

Supply the domain name (subject to standard DNS length limits — 253 characters overall, 63 per
label) and, if the caller's account has more than one, the target account ID. Optionally specify the
setup type from step 1 (full, partial, secondary, or internal); if omitted, Cloudflare defaults to a
full setup.

A newly created zone starts in a pending, not-yet-authoritative state — it does not take over DNS
resolution for the domain until the activation steps in step 3 are completed. On success, the response
includes the zone's Cloudflare-assigned name servers and, once Cloudflare has been able to detect them,
any name servers the domain used previously.

See `endpoints.md` § "Create a Zone" for the exact request/response shape.

### 3. Activate a full-setup zone

1. Populate the zone's DNS records before cutting over — either let Cloudflare scan the domain's
   existing authoritative servers and import what it finds, or add records directly (via
   `dns-record-management`'s Cloudflare procedure). Review the imported/added set for correctness before
   proceeding: an incomplete or wrong record at the zone apex or at a subdomain already in active use
   (most commonly `www`, or mail-related records: MX, and TXT records for SPF/DKIM/DMARC per the mail
   provider's own requirements) causes visible resolution failures for real visitors once the domain
   cuts over to Cloudflare, since Cloudflare will then be the one answering (or failing to answer)
   those queries.
   - Each proxyable record (A, AAAA, CNAME) carries its own proxied vs. DNS-only setting — proxied
     traffic is routed through Cloudflare's network, DNS-only returns the record's value with no
     proxying. Confirm with the operator which behavior each record needs, since this is a
     per-record, not per-zone, choice.
2. **Disable DNSSEC at the domain's current registrar before changing nameservers.** Changing
   nameservers while DNSSEC validation is still configured against the old provider's keys can make the
   domain unreachable, since resolvers will find a chain-of-trust mismatch. Do this first, not after.
3. At the registrar, remove the domain's existing nameserver entries and replace them with the two
   Cloudflare-assigned ones from step 2's response, exactly as given.
4. Propagation of the nameserver change is not instantaneous — allow up to 24 hours per the source,
   though it is frequently faster.
5. Confirm activation via a confirmation notification from Cloudflare and the zone's status moving to
   active (see step 4, read).

### 4. Read a zone

Fetch a zone's current state by its identifier — its name, status (`initializing`, `pending`,
`active`, or `moved`), assigned and (if known) prior name servers, and creation/activation timestamps.
Use this to confirm activation after step 3, or simply to report a zone's current state to the
operator.

### 5. Delete a zone — confirmation gate required

**Stop and confirm with the operator before deleting any zone.** This removes Cloudflare's zone
configuration for the domain outright. Cloudflare documents no precondition for zone deletion (such as Route 53's requirement that
a zone be reduced to only its default records first) — treat that absence as an open question rather than assuming deletion
either requires or doesn't require an empty zone; if the operator needs that guarantee met, verify
record contents first regardless. State to the operator: the zone name and ID, and that this action is
being treated as irreversible via this API absent evidence otherwise.

See `endpoints.md` § "Delete a Zone" for the exact request/response shape.

### 6. Handle documented errors

Cloudflare's API returns a consistent envelope on every call: `success` (boolean), `result`, `errors[]`
(each with a numeric `code`, a `message`, and optionally a `documentation_url` and a `source.pointer`
identifying the offending field), and `messages[]` for non-error informational notices. No
zone-specific error codes beyond this general shape are documented — when a call
fails, report the literal `code`/`message` pair from the response to the operator rather than guessing
at which documented error category it falls into.

## Patterns

- **A zone isn't authoritative just because it was created.** Full-setup activation is a separate,
  multi-step process gated on an external action (the registrar nameserver change) that this API alone
  cannot complete — don't report a create call's success as "the domain is now on Cloudflare."
- **Setup-type availability is plan-gated**, not just a preference — partial, zone-transfer, and
  subdomain setups require Business or Enterprise plans; don't assume a requested setup type is
  available without checking the account's plan first.

## Known limitations

- Unverified: subdomain (delegated child zone) setup's exact parent/child compatibility rules. This
  procedure documents that the capability exists and is Enterprise-only, but gives no step-by-step,
  since the source detail is not enough to state one without risking an invented step. Consult Cloudflare's own current zone-setups
  documentation directly before attempting a subdomain setup.
- Does not cover zone-transfer (AXFR/IXFR primary/secondary) configuration in depth, or partial (CNAME)
  setup's specific verification-key flow — both are referenced in step 1 as setup-type options but not
  documented step-by-step here.
- Does not cover individual DNS record management inside a zone — see `dns-record-management`.
- Whether Cloudflare requires a zone to be emptied of records before deletion is unconfirmed (see step
  5) — do not assume either way.
- Unverified: exact field names, the full Create Zone error list, and the subdomain-setup
  compatibility matrix. Re-verify them against Cloudflare's live documentation before depending on
  them in production.

## Tools

Every operation below maps to the Cloudflare REST API (Zones resource) — see `endpoints.md` for the
literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| Create Zone | Create a new zone in a pending state | Zone Management |
| Read Zone | Fetch a zone's current state, name servers, and status | Zone Management |
| Delete Zone | Remove a zone's Cloudflare configuration | Zone Management |

## Verification checklist

- [ ] A setup type was chosen deliberately (step 1), defaulting to full setup only when the caller
      didn't specify one, and checked against the account's plan tier if not full
- [ ] For full-setup activation: DNSSEC was disabled at the registrar before nameservers were changed,
      not after
- [ ] Zone records were reviewed for completeness (apex, `www`, mail records) before activation, to
      avoid visitor-facing resolution failures
- [ ] Zone status was confirmed as `active` (via read) after the nameserver change, rather than assumed
      from the create call alone
- [ ] Deletion was confirmed with the operator beforehand, and treated as irreversible absent
      documented evidence otherwise
- [ ] Any error response's literal `code`/`message` was reported to the operator, not normalized into a
      guessed category
