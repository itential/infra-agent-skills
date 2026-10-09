# GitLab project wiki bindings

Official sources: [Project wikis API](https://docs.gitlab.com/api/wikis/), [REST API](https://docs.gitlab.com/api/rest/), API v4, retrieved 2026-10-09.

Base `https://<gitlab-host>/api/v4`; an existing client supplies supported authentication, such as `PRIVATE-TOKEN: <token>`. Project `{id}` is numeric or its URL-encoded complete path. `{slug}` is URL encoded, including embedded `/` characters.

| Operation | Literal binding | Inputs | Result |
|---|---|---|---|
| List pages | `GET /projects/{id}/wikis` | Optional `with_content=true` | Array of page objects |
| Read page | `GET /projects/{id}/wikis/{slug}` | Optional `version` SHA, `render_html` | Page `content`, `format`, `slug`, `title`, `encoding` |
| Create page | `POST /projects/{id}/wikis` | Required `title`, `content`; optional `format=markdown\|rdoc\|asciidoc\|org` | Created page and generated slug |
| Update page | `PUT /projects/{id}/wikis/{slug}` | At least one of `title` or `content`; optional `format` | Updated page and potentially new slug |
| Delete page | `DELETE /projects/{id}/wikis/{slug}` | Project and slug | 204 with empty body |

Form encoding must preserve content characters and newlines; the publisher documents URL-encoding file content for complex Markdown. The cited wiki API gives 204 explicitly for deletion but does not enumerate exact success codes for every other operation; returned page objects are the documented verification surface.

General REST errors can carry `message` or `error`. Their meanings and handling appear in the procedure; operation-specific quotas and retry guarantees remain undocumented here.
