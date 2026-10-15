# Endpoints — Zscaler ZPA Access Policy Rules

Literal wiring layer. `SKILL.md`/`procedure.md` steps reference these by name; bind them to whatever
REST client/adapter is assumed available.

Source: Zscaler's own `zscaler-sdk-go` SDK, package `zscaler/zpa/services/policysetcontroller`
(github.com/zscaler/zscaler-sdk-go), retrieved 2026-09-29. Field descriptions below are restated from
the SDK's own struct definitions and doc comments, not copied verbatim.

## Base host and authentication

ZPA calls in this procedure go through Zscaler's unified OneAPI gateway. Base host:
`https://api.zsapi.net` for the production OneAPI cloud (a different `<cloud>.zsapi.net` host applies
for non-production clouds). Authentication is the same OAuth2 client-credentials flow via Zidentity
described in the ZIA `endpoints.md` — obtain a client ID/secret for the tenant's Zidentity vanity
domain (OneAPI access must be enabled by the Zscaler account team), exchange it at
`POST https://<vanity_domain>.zslogin.net/oauth2/v1/token`, and present the resulting access token as
`Authorization: Bearer <token>` on every call below. Every path below also requires the target
tenant's `customerId` as a path parameter.

## Get Policy Set by Type

```
GET /zpa/mgmtconfig/v1/admin/customers/{customerId}/policySet/policyType/{policyType}
```
Resolves the policy set object (including its `id`) for a given `policyType` — use the access-policy
type value to get the `policySetId` needed for every rule operation below.

## List Rules by Policy Type

```
GET /zpa/mgmtconfig/v1/admin/customers/{customerId}/policySet/rules/policyType/{policyType}
```
Returns the current rules for the access policy set, including their order — use before any
placement-sensitive create/update/reorder.

## Get Rule

```
GET /zpa/mgmtconfig/v1/admin/customers/{customerId}/policySet/{policySetId}/rule/{ruleId}
```

## Create Rule

```
POST /zpa/mgmtconfig/v1/admin/customers/{customerId}/policySet/{policySetId}/rule
```

**Request body fields (restated from the SDK's typed `PolicyRule` struct):**

| Field | JSON key | Type | Notes |
|---|---|---|---|
| Name | `name` | string | Rule display name |
| Action | `action` | string | Match action for the access-policy type (e.g. allow/deny-style value documented per policy type) |
| Action ID | `actionId` | string | Reference ID tied to the chosen action, where applicable |
| Operator | `operator` | string | Top-level boolean operator combining the rule's condition groups |
| Priority | `priority` | string | Typed as a string in the wire format, not an integer |
| Rule order | `ruleOrder` | string | Typed as a string in the wire format; position in the evaluation sequence |
| Disabled | `disabled` | string | Typed as a string in the wire format, not a boolean |
| Default rule | `defaultRule` | boolean | Marks the rule as the policy set's default/catch-all rule |
| Conditions | `conditions` | array of Conditions | The structured scope expression — see below |
| Policy set ID | `policySetId` | string | The resolved access policy set ID (also supplied as a path parameter on some calls) |
| Policy type | `policyType` | string | Identifies which ZPA policy type this rule belongs to |
| Microtenant ID | `microtenantId` | string | Optional microtenant scoping, where the tenant uses microtenants |

**`conditions` structure:** each entry is an operator/operand grouping — an operator (combining
operands with AND/OR-style logic) over a set of operands, where each operand names an object type
(e.g. application segment, segment group, SAML/SCIM attribute, posture profile) and the resolved
ID(s) of the specific object(s) in scope. The SDK source notes that on update, empty operand values
are normalized to an empty list type and operand display names are cleared before submission — build
conditions with only the fields the object type actually requires rather than passing through
caller-supplied extra fields.

**Success:** the created rule object, including its assigned `id`.

**Failure:** the SDK source does not document specific error codes/strings for this endpoint beyond
propagating the HTTP status and response body — surface that verbatim. A failure on a rapid sequence
of writes to the same policy set is plausible given the source's own note that ZPA restricts
concurrent policy-set write operations; the SDK serializes its own calls with a mutex for this reason.

## Update Rule

```
PUT /zpa/mgmtconfig/v1/admin/customers/{customerId}/policySet/{policySetId}/rule/{ruleId}
```
Same body shape as create, addressed to an existing rule's `id`. Returns the updated rule object.

## Delete Rule

```
DELETE /zpa/mgmtconfig/v1/admin/customers/{customerId}/policySet/{policySetId}/rule/{ruleId}
```
Removes the rule. Returns a success status on success.

## Reorder Rule (single)

```
PUT /zpa/mgmtconfig/v1/admin/customers/{customerId}/policySet/{policySetId}/rule/{ruleId}/reorder/{newOrder}
```
Moves one rule to the specified position without changing any of its other fields.

## Reorder Rules (bulk)

```
PUT /zpa/mgmtconfig/v1/admin/customers/{customerId}/policySet/{policySetId}/reorder
```
Repositions multiple rules in one call. The SDK source notes this operation automatically keeps any
rule flagged as the default rule pinned at the end of the resulting order regardless of the requested
positions for other rules.

## Reference object lookups (for resolving condition operands to IDs)

Application segments (`/application`, `/application/{applicationId}`) and segment groups
(`/segmentGroup`, `/segmentGroup/{segmentGroupId}`) are the two object types most commonly referenced
in access-policy conditions and have their own list/lookup endpoints in the same SDK — resolve
caller-supplied names against those before building a rule's `conditions`. User-attribute, SAML/SCIM,
and posture-profile operand types have their own separate lookup endpoints outside this rule family's
scope and are not restated here.
