# Grafana dashboard definition inspection

Resolve a dashboard UID and retrieve the requested definition detail.

## Common Sequences

- Inspect a dashboard: **Search** → **Read summary** → **Read detail**.

### Search

Dashboard search uses the requested text, immediate folder, tags and starred filter. Page numbers are one-based. The returned total is the current page length in the cited implementation, not a server-wide total; its more-results flag indicates a full page that may have successors. Full discovery continues until the next-page condition is exhausted or is explicitly partial. Search/access failures remain failures.

### Read summary

The resolved UID selects a compact summary containing title, panel information, variables and time settings. A missing/inaccessible UID ends this branch. Titles alone are not substituted for UIDs when multiple matches exist.

### Read detail

The caller selects full native dashboard JSON, a JSONPath property, or panel-query definitions. Classic and v2 dashboards have different native property paths; the published implementation preserves the stored schema. An invalid JSONPath or a path that cannot be evaluated is an extraction error, not an empty dashboard. Panel-query extraction can apply supplied variable substitutions; it returns definitions and datasource identity rather than executing the queries.

## Patterns

A saved dashboard version is an optional input for the full-definition read. The summary and targeted property/query operations inspect the currently resolved dashboard.

## Known limitations

Only dashboard/folder read functionality is covered. Image rendering needs a separately configured renderer and is outside this procedure. Permissions and installed tool categories determine availability.

## Tools

Assumes the authenticated client described in [the bindings](endpoints.md).

| Operation | Description | Category |
|---|---|---|
| Search | Find dashboard identities | Dashboard read |
| Summary/detail | Read native definitions or selected properties | Dashboard read |
| Panel queries | Extract configured query targets | Dashboard read |

## Verification checklist

- UID resolves uniquely.
- Pagination total is not mistaken for a global count.
- Native dashboard schema and property paths agree.
- Extracted query definitions are not called live data.

## Sources

- [Publisher dashboard implementation](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/tools/dashboard.go). Retrieved 2026-10-09.
- [Publisher search implementation](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/tools/search.go). Retrieved 2026-10-09.
- [Publisher setup and permission reference](https://github.com/grafana/mcp-grafana/blob/4cd6590f2b84a2e819622a3fdf7298b425cb4fc7/README.md). Retrieved 2026-10-09.
