# Cloudflare Registrar — Domain Asset Record Management

Source: Cloudflare API Reference, DNS Records resource (developer docs, retrieved 2026-09-15).

## Operational procedure

1. **Create the domain asset record.** Creating a domain record performs the following function:
   create a new DNS record for a zone, tracked here as a domain-ownership asset. A/AAAA records
   cannot exist on the same name as CNAME records, and NS records cannot exist on the same name as
   any other record type. Domain names are always represented in Punycode, even if Unicode
   characters were used when creating the record.
2. **Confirm the record was created** by reading it back and checking its assigned identifier.
3. **Update the asset** when the underlying DNS record changes, keeping the CMDB entry in sync with
   the live zone.
4. **Delete the asset record** when the domain is decommissioned, after confirming no other CI
   depends on it.

## Patterns

- Treat the DNS record as the source of truth; this CI is a read-through cache of it, not an
  independent record.

## Known limitations

- Does not cover zone-level settings, only individual record-backed assets.

## Tools

Assumes an authenticated Cloudflare API client is already available.

## Verification checklist

- [ ] Asset created/updated/deleted as requested
- [ ] Record type conflicts (CNAME exclusivity, NS exclusivity) checked before create
- [ ] Domain name recorded in Punycode form
