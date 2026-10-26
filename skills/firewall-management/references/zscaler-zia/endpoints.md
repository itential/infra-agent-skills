# Endpoint Wiring — Zscaler ZIA Cloud Firewall Filtering Rules

Source: zscaler-sdk-go, ZIA firewall filtering rules package (github.com/zscaler/zscaler-sdk-go),
retrieved 2026-10-26. Items marked *(unverified)* are not confirmed.

## Base host and authentication

Calls go to the OneAPI gateway at `https://api.zsapi.net` (production cloud; other clouds use a
different host *(unverified)*). Authentication is OAuth2 client credentials issued through
Zidentity: exchange the client id and secret at `POST https://<vanity-domain>.zslogin.net/oauth2/v1/token`
and send the token as a bearer `Authorization` header on each ZIA call *(unverified)*.

## Rule calls

| Capability | Call |
|---|---|
| List rules | `GET /zia/api/v1/firewallFilteringRules` (optional rule-name filter and paging; SDK page cap 5000) |
| Read rule | `GET /zia/api/v1/firewallFilteringRules/{id}` |
| Create rule | `POST /zia/api/v1/firewallFilteringRules` |
| Update rule | `PUT /zia/api/v1/firewallFilteringRules/{id}` |
| Delete rule | `DELETE /zia/api/v1/firewallFilteringRules/{id}` |

Rule body fields seen in the SDK struct: `name`, `order`, `rank`, `action`, `state`, `description`,
`enableFullLogging`, `defaultRule`, `predefined`, `srcIps`, `srcIpGroups`, `sourceCountries`,
`excludeSrcCountries`, `destAddresses`, `destIpGroups`, `destIpCategories`, `destCountries`,
`nwApplications`, `nwApplicationGroups`, `nwServices`, `nwServiceGroups`, `locations`,
`locationGroups`, `departments`, `groups`, `users`, `devices`, `deviceGroups`, `timeWindows`,
`labels`, `workloadGroups`. JSON key casing is inferred from the SDK's Go field names *(assumption)*.
Referenced objects are objects carrying an `id`, not bare names.

Success: the rule object with its `id` (create, read, update); a success status without body
(delete) *(unverified)*. Error bodies are not documented; report them as
returned.

## Referenced objects

Reading IP groups, services, locations, departments, groups, users, devices, time windows and
labels uses a separate call per object type. Unverified: the routes for these are not captured
here; consult the ZIA API reference for each object type before binding.

## Activation

| Capability | Call |
|---|---|
| Read activation status | `GET /zia/api/v1/status` (status string in the `status` field) |
| Activate configuration | `POST /zia/api/v1/status/activate` |

Known error: HTTP 409 with name `EDIT_LOCK_NOT_AVAILABLE` means another administrator's edit holds
the lock; wait a few seconds and retry *(unverified)*. The procedure refers to this condition as the edit-lock conflict.
