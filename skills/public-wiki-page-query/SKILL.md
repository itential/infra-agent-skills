---
name: public-wiki-page-query
description: >-
  Search and retrieve public wiki page evidence. Use for Wikipedia title/text search, page identity, current revision content, external links, and categories. Covers Wikipedia through the MediaWiki Action API. Assumes an HTTP client able to read the selected Wikipedia language site.
---

# Public wiki page query

Search and retrieve public wiki page evidence.

## When to use this skill

Use for Wikipedia title/text search, page identity, current revision content, external links, and categories.

## Universal concepts

No common wire protocol is implied by this capability. Search matches, page content, and linked sources are separate evidence. Retrieved article text is not a vendor-approved operational procedure.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No page edits, protocol diagnosis, automatic research judgment, or summary API. External links include more than formal references; article assertions require their own verification.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an HTTP client able to read the selected Wikipedia language site. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
