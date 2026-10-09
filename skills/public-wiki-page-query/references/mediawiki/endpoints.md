# MediaWiki Action API bindings

Official sources, retrieved 2026-10-09: [Query](https://www.mediawiki.org/wiki/API:Query), [Search](https://www.mediawiki.org/wiki/API:Search), [Info](https://www.mediawiki.org/wiki/API:Info), [Revisions](https://www.mediawiki.org/wiki/API:Revisions), [External links](https://www.mediawiki.org/wiki/API:Extlinks), [Categories](https://www.mediawiki.org/wiki/API:Categories), [TextExtracts limitations](https://www.mediawiki.org/wiki/Extension:TextExtracts).

Base for the selected language: `https://<language>.wikipedia.org`. Every operation below is `GET /w/api.php`, with URL-encoded parameters `action=query`, `format=json`, `formatversion=2`. Public read access is assumed; private wiki access is outside scope.

| Operation | Query parameters | Verification |
|---|---|---|
| Search pages | `list=search`, `srsearch=<query>`, optional `srwhat=title\|text`, `srlimit` | `query.search` titles and `pageid`; continuation |
| Read page identity | `prop=info`, `pageids=<id>` OR `titles=<title>`, `inprop=url`, optional `redirects=1` | `query.pages`, canonical title/URL; `missing` or invalid markers |
| Read current revision | `prop=revisions`, one page identity, `rvprop=ids\|timestamp\|content`, `rvslots=main` | Revision ID/time and main-slot content; `texthidden` means unavailable |
| List external links | `prop=extlinks`, one page identity, `ellimit` | `extlinks`; `elcontinue` when more remain |
| List categories | `prop=categories`, one page identity, `cllimit`; optional `clshow=hidden` or `!hidden` | Category titles; `clcontinue` when more remain |

The search, link, and category limits are documented between 1 and 500; the normal default is 10. Continuation sends the full returned `continue` object, not only a guessed offset.

Search error names: `nosrsearch`, `search-text-disabled`, `search-title-disabled`, `search-error`. Revision errors relevant to access or invalid combinations include `rvaccessdenied`, `accessdenied`, `rvbadparams`, `rvrevids`, `rvmultpages`, and `invalidparammix`. Historical/section/diff errors such as `rvnosuchrevid`, `rvnosuchsection`, `rvdiffto`, `badid_startid`, and `badid_endid` require leaving the unsupported historical parameters out; they are not converted to empty content. Actual API error objects and warnings remain part of the outcome.
