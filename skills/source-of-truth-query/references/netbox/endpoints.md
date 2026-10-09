# NetBox record-read bindings

Source: [NetBox REST API](https://netboxlabs.com/docs/netbox/integrations/rest-api/), retrieved 2026-10-09. Base URL is the configured instance `https://<instance>`. `Authorization: Bearer nbt_<key>.<token>` for v2 tokens; legacy v1 uses `Authorization: Token <token>`. v1 is deprecated from NetBox 4.6 and scheduled for removal at 5.0.

| Operation | Binding | Result |
|---|---|---|
| Discover API root | `GET /api/` | Application links |
| Discover application | `GET <returned-application-url>` | Model collection links |
| Read collection | `GET <returned-model-list-url>` with model-documented filters | HTTP 200; `count`, `next`, `previous`, `results` |
| Read detail | `GET <returned-object-url>` | HTTP 200; object with its numeric primary key |
| Continue offset page | `GET <next-url>` | Next page preserving selected filters |

The model URL placeholders are populated from API discovery, not inferred route strings. Collection filters, available fields and detail identifiers are resolved from the installed API schema. Offset paging uses `limit` and `offset`; server configuration constrains the page size. Paths retain their trailing slash; missing-slash redirects are not treated as a record response.

The documented missing-credentials response is HTTP `403` with `detail` equal to `Authentication credentials were not provided.` Other model-specific errors use the endpoint's own response contract. Secrets remain in the configured client and are not printed in query reports.
