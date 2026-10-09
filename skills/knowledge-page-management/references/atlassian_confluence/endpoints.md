# Confluence Cloud page bindings

Official sources: [Pages REST v2](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/), [Spaces REST v2](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/), [Rate limiting](https://developer.atlassian.com/cloud/confluence/rate-limiting/), publisher OpenAPI v2, retrieved 2026-10-09.

Site base `https://<site>.atlassian.net`; an existing authenticated client selects the supported site or OAuth gateway binding. JSON media type `application/json`. IDs are returned by the platform, not inferred from page titles.

| Operation | Literal binding | Inputs | Result |
|---|---|---|---|
| Read space | `GET /wiki/api/v2/spaces/{id}` | Space ID | 200 space; 400/401/404 |
| List pages | `GET /wiki/api/v2/pages` | Optional `space-id`, `title`, `status`, `body-format`, `limit`, `cursor` | 200 page collection; 400/401 |
| Read page | `GET /wiki/api/v2/pages/{id}` | `body-format=storage` or supported format; optional `status` | 200 page with `id`, `status`, `spaceId`, `title`, `body`, `version.number`; 400/401/404 |
| Create page | `POST /wiki/api/v2/pages` | `spaceId`, `status=current`, `title`, `body:{representation,value}`; optional `parentId` | 200 page; 400/401/404/413 |
| Update page | `PUT /wiki/api/v2/pages/{id}` | Required `id`, `status=current`, `title`, `body`, `version:{number:<current+1>}` | 200 page; 400/401/404/409 |
| Trash page | `DELETE /wiki/api/v2/pages/{id}` | Published page; `purge=false`, `draft=false` | 204; 400/401/404 |

Body representations include `storage`, `atlas_doc_format`, and `wiki`; values are strings in the selected representation. This scope uses ordinary pages with no `subtype=live`. List continuation is available through the `Link` response header and response links. Rate limiting can supply `Retry-After`.

Publisher safeguards: `purge=true` permanently removes an already trashed page; `draft=true` deletes a draft permanently. Those modes are excluded. Updating status to `draft` has a separate version rule and can replace an existing draft, so this binding fixes status to `current`.
