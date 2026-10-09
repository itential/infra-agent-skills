# Wikipedia page evidence

MediaWiki Action API operations retrieve one public Wikipedia page and its associated evidence.

## Common Sequences

- Find and read: **Search pages → Read page identity → Read current revision**.
- Inspect references: **Read page identity → List external links → List categories**.

### Search pages

The search operation applies the requested title/text query on the selected language site. Success returns matching titles and page identifiers. Search syntax depends on the site's search backend. A missing-query error requires a query; disabled title/text search requires a supported mode; a search-engine error is reported as failure. An empty successful result remains an empty match set.

### Read page identity

The page-information operation resolves the selected title or page identifier and returns its current title and canonical URL. Normalization, redirects, missing-page markers, and invalid titles remain explicit. A missing page stops content retrieval for that identity.

### Read current revision

The revision operation selects the page's current main-slot content and its revision identifier/timestamp. Success returns the content actually stored, which can be wikitext rather than rendered prose. Hidden revision content is reported as unavailable. Access-denied errors require stopping retrieval; invalid parameter combinations require correction. The binding intentionally avoids historical range, section, and diff parameters that introduce unrelated error cases.

### List external links

The external-link operation returns URLs associated with the selected page. Continuation is followed until the requested result set is complete. These are external URLs, excluding interwiki links; they are not guaranteed to be a bibliography or validated sources.

### List categories

The category operation returns category titles associated with the page. Hidden-category filtering is explicit, and continuation is preserved. Success is the returned category collection, including an empty collection.

## Patterns

Every continuation member returned by the server is retained for the next request with the original query. Page identity and revision timestamp make the evidence attributable. A transport failure or API error is not an empty successful result.

## Known limitations

Current main-slot content only. This procedure does not manufacture summaries or treat Wikipedia as authority for vendor configuration. The publisher warns against new Wikimedia-production features based on TextExtracts; a summary service is therefore not inferred from that extension. Exact operation-specific quotas are unknown; rate-limited requests follow any returned retry guidance.

## Tools

| Operation | Description | Category |
|---|---|---|
| Search pages | Find candidate page identities | Read |
| Read page identity | Resolve canonical page information | Read |
| Read current revision | Retrieve current source content | Read |
| List external links | Retrieve page-associated URLs | Read |
| List categories | Retrieve category membership | Read |

Bindings, error names, and citations are in [endpoints.md](endpoints.md).

## Verification checklist

- Language site, canonical page identity, and revision are retained.
- Missing, hidden, and failed retrievals are distinct from empty collections.
- Continuation is exhausted or the result is labeled partial.
- External links and article claims are not presented as verified vendor guidance.
