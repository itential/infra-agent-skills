# Endpoint Wiring — WatchGuard Firebox Management API

Citation: WatchGuard, Firebox Management API release notes and Cloud documentation,
watchguard.com/help, retrieved 2026-10-19. Policy PATCH and deployments paths were seen on the
vendor release notes; the remaining paths and auth come from the vendor spec as curated in
itential/assets (`WatchGuard/Firebox`, API v1.29.0) — secondary source.

Base: `https://api.usa.cloud.watchguard.com/rest/firebox/management` (other regional hosts exist;
override per account). Auth *(assets)*: OAuth2 client-credentials bearer token (token URL
`https://api.usa.cloud.watchguard.com/oauth/token`, Basic-auth with API access ID and password,
expires after 3600 s) plus a `WatchGuard-API-Key` header, both required.

| Capability | Call |
|---|---|
| List policies | `GET /v1/configuration/{accountid}/firewall/policies` |
| Create policy | `POST /v1/configuration/{accountid}/firewall/policies` |
| Read policy | `GET /v1/configuration/{accountid}/firewall/policies/{objectid}` |
| Update policy | `PUT /v1/configuration/{accountid}/firewall/policies/{objectid}` |
| Enable/disable policy | `PATCH /v1/configuration/{accountid}/firewall/policies/{objectid}` |
| Delete policy | `DELETE /v1/configuration/{accountid}/firewall/policies/{objectid}` |
| List / read policy groups | `GET /v1/configuration/{accountid}/firewall/policy_groups[/{objectid}]` |
| List / read aliases | `GET /v1/configuration/{accountid}/firewall/aliases[/{objectid}]` |
| Deploy to devices | `POST /v1/commands/{accountid}/deployments` (max 50 devices per request) |
