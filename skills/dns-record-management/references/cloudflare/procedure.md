# Cloudflare — DNS Record Creation Procedure

Create a DNS record (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, PTR) in an existing Cloudflare zone.
Create-only, in an existing zone — does not cover zone creation, record edit/delete, SOA (auto-created
by Cloudflare), auto-generated SVCB/HTTPS records, DNSSEC records (DS/DNSKEY), Enterprise-only private
network routing, or less-common types (URI, NAPTR, SSHFP, TLSA, SMIMEA, CERT). Assumes an authenticated
REST client against the Cloudflare API (a Bearer token scoped with Zone-level DNS write access —
dashboard UI commonly labels this "Zone > DNS > Edit"; verify the exact permission name for the target
account) is already available.

Scope note: this covers the "Create DNS Records" procedure on Cloudflare's own how-to page; Edit and
Delete are explicitly out of scope. Per-type field schemas for MX/SRV/CAA are drawn from Cloudflare's
API reference ("DNS Records for a Zone" → Create).

## Operational procedure

1. **Confirm the zone exists and is accessible** — resolve the zone ID (or look it up by zone name if
   only a name was given). If it cannot be found or the token lacks access, stop and report FAILED with
   "zone not found or not accessible" (see `endpoints.md`).
2. **Validate record type support** — confirm the requested type is one this skill covers: A, AAAA,
   CNAME, MX, TXT, NS, SRV, CAA, or PTR. If the caller asked for SOA, SVCB/HTTPS, DS/DNSKEY, or a
   less-common type, stop and report that it's out of scope (see `record-fields.md` for why).
3. **Validate and build the type-specific payload** — per `record-fields.md`:
   - A/AAAA: content must be a valid IPv4/IPv6 address and must not be a Cloudflare-owned IP.
   - CNAME: content must be a valid hostname and must differ from the record name.
   - MX: content (mail server hostname) AND priority are both required — if priority is missing, stop
     and report REJECTED_INVALID_TYPE_FIELD.
   - TXT: content as one or more quoted strings, each ≤ 255 bytes.
   - SRV/CAA: build the structured `data` object (SRV: priority/weight/port/target; CAA: flags/tag/
     value) — do not use `content` for these two types.
   - NS/PTR: content is the nameserver/target hostname.
   If a required type-specific field is missing, stop and report REJECTED_INVALID_TYPE_FIELD rather than
   guessing a value.
4. **Apply proxy status rules** — if proxying is requested, confirm the type is A, AAAA, or CNAME; if
   not, stop and report REJECTED_INVALID_TYPE_FIELD ("proxied is not valid for this record type"). If
   proxying is requested and valid: **stop and confirm with the operator before proceeding** — this
   routes live traffic through Cloudflare and exposes/hides the origin IP, a real production change, not
   just a DNS entry. If proxied, TTL will be forced to Auto (300s) regardless of any TTL value supplied
   — do not treat this as an error, just don't expect a custom TTL to stick.
5. **Apply structural conflict checks** — before submitting, check for the two documented conflicts (see
   `record-fields.md`): an A/AAAA record cannot share a name with an existing CNAME, and an NS record
   cannot share a name with any other record type. If the calling tool can check existing records first
   and finds a conflict, stop and report REJECTED_STRUCTURAL_CONFLICT rather than submitting a call
   Cloudflare will reject.
6. **Create the record** — submit the assembled payload (type, name, plus content or the structured
   data object, TTL, proxied, and any comment/tags) against the target zone. See `endpoints.md` for the
   literal call.
7. **Confirm creation** — treat a 2xx response with `success: true` and a `result` object containing an
   `id` as success. If the calling tool needs a separate confirmation read, look the record back up by
   id, or by type+name in the same zone. Report CREATED with the record object.
8. **Handle failures verbatim** — the sources for this skill do not document specific error strings for
   duplicate-record or invalid-content conditions beyond the generic `{"success": false, "errors": [...]}`
   shape (see `endpoints.md`). If the create call fails for any reason not already handled by steps 2-5,
   report FAILED with the underlying tool's actual `errors` array rather than guessing at a cause.

## Patterns

- **Proxying silently overrides TTL.** A proxied record is always served at Auto TTL (300s) — a custom
  TTL value is accepted without error but simply doesn't take effect.
- **SRV/CAA never use `content`.** These two types are structured-only; passing a flat value for them
  is a type-field mismatch, not a valid simplified form.

## Known limitations

- Create-only, in an existing zone — does not cover zone creation, record edit/delete, SOA (auto-created
  by Cloudflare), auto-generated SVCB/HTTPS records, DNSSEC records (DS/DNSKEY), Enterprise-only private
  network routing, or less-common types (URI, NAPTR, SSHFP, TLSA, SMIMEA, CERT).
- **Enabling the Cloudflare proxy on a record is a real traffic-routing change**, not just a DNS entry —
  it changes live HTTP/HTTPS routing and origin-IP exposure for the hostname. This is why step 4 requires
  explicit operator confirmation before submitting.
- Reversible only by deleting the created record (not covered by this skill), and a wrong record type
  is a delete-and-recreate, not an in-place edit, per Cloudflare's own type/content rules.

## Tools

| Operation | Description | Category |
|---|---|---|
| Zone lookup | Resolve/confirm the target zone and access | DNS Zones |
| `DNS Records for a Zone` → List | Check for existing records (structural conflict / duplicate checks) | DNS Records |
| `DNS Records for a Zone` → Create | Create a new DNS record in the zone | DNS Records |

## Verification checklist

- [ ] Record type confirmed in-scope before building the payload
- [ ] Type-specific required fields (priority for MX, structured data for SRV/CAA) were present, not
      defaulted or guessed
- [ ] If proxying was requested: confirmed with the operator before submission
- [ ] Structural conflicts (A/AAAA vs. existing CNAME, NS vs. any other type at the same name) checked
      before submitting, where the calling tool supports a pre-check
- [ ] Creation confirmed via the API response's `result.id` or a follow-up lookup
