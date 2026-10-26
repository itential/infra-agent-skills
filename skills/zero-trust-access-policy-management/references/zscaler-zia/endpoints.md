# Endpoints — Zscaler ZIA URL Filtering Rules

Literal wiring layer. `SKILL.md`/`procedure.md` steps reference these by name; bind them to whatever
REST client/adapter is assumed available.

Source: Zscaler's own `zscaler-sdk-go` SDK, package `zscaler/zia/services/urlfilteringpolicies`
(github.com/zscaler/zscaler-sdk-go), retrieved 2026-09-29. Field descriptions below are restated from
the SDK's own per-field doc comments, not copied verbatim.

## Base host and authentication

All ZIA calls in this procedure go through Zscaler's unified OneAPI gateway, not a legacy
tenant-specific ZIA host. Base host: `https://api.zsapi.net` for the production OneAPI cloud (a
different `<cloud>.zsapi.net` host applies for non-production clouds — confirm against the target
tenant's assigned cloud).

Authentication is OAuth2 client-credentials, brokered through Zscaler's Zidentity service (per
Zscaler's own OneAPI authentication documentation):

1. Obtain a client ID and client secret for the tenant's Zidentity vanity domain — this requires
   OneAPI access to be enabled for the organization by the Zscaler account team; it is not
   self-service, and is generated in the Admin Portal under API Key Management.
2. Exchange the client credentials for an access token at
   `POST https://<vanity_domain>.zslogin.net/oauth2/v1/token`.
3. Present the returned access token as a Bearer token (`Authorization: Bearer <token>`) on every
   subsequent ZIA call.

## List URL Filtering Rules

```
GET /zia/api/v1/urlFilteringRules
```
Returns the full ordered list of URL Filtering rules for the tenant. Use before any placement- or
conflict-sensitive create/update to see current `order` values.

## Get URL Filtering Rule

```
GET /zia/api/v1/urlFilteringRules/{id}
```
Returns a single rule by its numeric `id`.

## Create URL Filtering Rule

```
POST /zia/api/v1/urlFilteringRules
```

**Request body fields (restated from the SDK's typed struct, not exhaustive of every advanced
toggle):**

| Field | Type | Notes |
|---|---|---|
| `name` | string | Rule display name |
| `order` | integer | Position in the evaluation sequence (stop-on-first-match) — see procedure step 3 |
| `rank` | integer | A separate administrative priority/authority value, distinct from `order` |
| `state` | string | Enabled/disabled state of the rule |
| `action` | string | Match action, e.g. `ALLOW`, `BLOCK`, `CAUTION`, `ISOLATE` |
| `protocols` | array of string | Protocol match criteria |
| `urlCategories` | array of string | URL category IDs the rule matches against |
| `requestMethods` | array of string | HTTP methods the rule applies to |
| `sourceCountries` | array of string | Geographic source restriction |
| `userAgentTypes` | array of string | Client/user-agent type filter |
| `locations` | array of ID-object | Locations the rule applies to — resolve names to IDs first |
| `groups` | array of ID-object | User groups in scope |
| `departments` | array of ID-object | Departments in scope |
| `users` | array of ID-object | Individual users in scope |
| `timeWindows` | array of ID-object | Time-of-day/day-of-week windows the rule is active |
| `deviceGroups` / `devices` | array of ID-object | Managed device scope |
| `sourceIpGroups` | array of ID-object | Source IP group scope |
| `blockOverride` | boolean | Whether an authorized user can temporarily override a block |
| `timeQuota` | integer | Minutes of access allowed before the rule's action takes effect |
| `sizeQuota` | integer | KB threshold before the rule's action takes effect |
| `enforceTimeValidity` | boolean | Whether the rule is time-bound (start/end validity) |
| `cbiProfile` / `cbiProfileId` | object / string | Cloud Browser Isolation profile reference, relevant when `action` is an isolate action |
| `enableCIPACompliance` | boolean | See procedure step 5 for the documented mutual-exclusion constraint |
| `enableNewlyRegisteredDomains`, `considerEmbeddedSites`, `enforceSafeSearch`, `enableDynamicContentCat` | boolean | The four fields documented as incompatible with `enableCIPACompliance` set true |

ID-object references (`locations`, `groups`, `departments`, `users`, `timeWindows`, `deviceGroups`,
`devices`, `sourceIpGroups`) are objects carrying at minimum an `id`, not bare strings or names.

**Success:** the created rule object, including its assigned `id`.

**Failure:** the SDK source does not document specific error codes/strings for this endpoint beyond
propagating the HTTP status and response body — surface that verbatim rather than inferring a cause.

## Update URL Filtering Rule

```
PUT /zia/api/v1/urlFilteringRules/{id}
```
Same body shape as create, addressed to an existing rule's `id`. Returns the updated rule object.

## Delete URL Filtering Rule

```
DELETE /zia/api/v1/urlFilteringRules/{id}
```
Removes the rule. Returns a success status with no body on success, per the SDK's handling.

## Reference object lookups (for resolving names to IDs)

Locations, groups, departments, users, and time windows each have their own list/lookup endpoints in
ZIA (separate service packages in the same SDK) — resolve caller-supplied names against those before
building a URL Filtering rule payload; this procedure does not restate each one's own wire format
since they are outside this rule family's endpoint.

## Get Activation Status

```
GET /zia/api/v1/status
```
Returns the tenant's activation state in a `status` field. Not documented: the set of status values;
read the returned value rather than matching a fixed list.

## Activate Configuration

```
POST /zia/api/v1/status/activate
```
Publishes the tenant's saved configuration. Unverified: the request is queued and does not override concurrent changes by other
administrators, and Zscaler recommends activating once after a group of changes. Path prefix: from
the Zscaler Go SDK's activation package. Not documented: the response body; read the status
afterward.

**Failure:** an HTTP 409 with the error name `EDIT_LOCK_NOT_AVAILABLE` indicates concurrent edits
holding the lock; Zscaler advises waiting a few seconds and retrying (Unverified). Not documented: other error bodies; surface them verbatim.
