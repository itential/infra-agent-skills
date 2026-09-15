# Freshservice CMDB — Endpoint Reference

| Operation | Method | Path |
|---|---|---|
| Create a CI | `POST` | `/api/v2/assets` |
| Read a CI | `GET` | `/api/v2/assets/{display_id}` |
| List/filter CIs | `GET` | `/api/v2/assets?filter=...` |
| Update a CI | `PUT` | `/api/v2/assets/{display_id}` |
| Delete a CI | `DELETE` | `/api/v2/assets/{display_id}` |

All requests require `Authorization: Basic <base64 API key>` per Freshservice's documented auth
scheme.
