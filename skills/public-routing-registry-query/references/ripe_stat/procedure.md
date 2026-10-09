# RIPEstat routing and registry evidence

Read published ASN/prefix observations, registry records, abuse contacts and RPKI origin-validation evidence.

## Common Sequences

- ASN context: **Read ASN overview** → **Read announced prefixes** → **Read registry context**.
- Prefix-origin validation: **Validate origin** → **Read registry context** for the supplied resource.

### Read ASN overview

The overview returns the queried ASN, holder and announcement flag with its query timing. The flag reflects originating prefixes visible to at least ten RIS full-feed peers; a transit-only ASN can consequently be false. Missing holder information remains unavailable registration evidence.

### Read announced prefixes

The announcement read accepts an ASN and optional time bounds and peer-visibility threshold. Success is the prefix list with visibility timelines and returned query/data-availability times. Defaults cover the previous two weeks with at least ten seeing peers. Empty output does not prove that no localized or low-visibility announcement exists.

### Read registry context

WHOIS evidence returns registration and routing-registry records with their authorities and query time. An abuse-contact lookup returns dedicated contacts and the authoritative RIR. Success is those native records, including empty or missing contact fields; RIPE warns that abuse-contact data may be missing or inaccurate. This read does not send a report to any contact.

### Validate origin

The origin-validation read uses the exact prefix, including its length, and ASN. The native status is retained: valid means a matching authorization; invalid ASN means a covering authorization differs in origin; invalid length means the proposed prefix exceeds its allowed maximum; unknown means no matching authorization was found. None of these states alone establishes a hijack, intent or root cause.

For every operation, only the API's successful envelope is treated as successful data. Error envelopes retain the publisher's message; maintenance remains unavailable. A deprecated/development endpoint status and cached-response flag qualify the evidence. Transport or throttling errors leave the read unresolved; any response retry guidance is retained without inventing a fixed rate.

## Patterns

Registration authority, observed announcement and origin authorization are independent facts. The API's envelope status must not be confused with the RPKI status inside its data. The API documentation inconsistently calls its error text singular or plural; the returned message payload is preserved as received.

## Known limitations

No RDAP object traversal, route-policy change or maliciousness verdict is included. The documented per-IP concurrency limit is eight requests; regular high-volume usage has separate publisher registration guidance.

Sources: [RIPEstat API basics](https://stat.ripe.net/docs/data-api/ripestat-data-api/), [ASN overview](https://stat.ripe.net/docs/data-api/api-endpoints/as-overview), [prefixes](https://stat.ripe.net/docs/data-api/api-endpoints/announced-prefixes), [WHOIS](https://stat.ripe.net/docs/data-api/api-endpoints/whois), [abuse contact](https://stat.ripe.net/docs/data-api/api-endpoints/abuse-contact-finder), [RPKI](https://stat.ripe.net/docs/data-api/api-endpoints/rpki-validation), retrieved 2026-10-09. Bindings: [endpoints](endpoints.md).

## Tools

| Operation | Purpose | Category |
|---|---|---|
| Read ASN overview | Read holder and observed origination | Read |
| Read announced prefixes | Read prefixes and visibility timelines | Read |
| Read registry context | Read WHOIS/IRR and abuse contacts | Read |
| Validate origin | Read prefix/ASN RPKI validity | Read |

## Verification checklist

- Resource, prefix length, time bounds and visibility threshold are retained.
- API envelope and RPKI statuses are distinguished.
- Cache/deprecation/maintenance information is visible.
- Registration or validity is not converted into incident attribution.
