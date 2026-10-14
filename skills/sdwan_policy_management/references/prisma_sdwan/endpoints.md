# Endpoints — Palo Alto Networks Prisma SD-WAN, stacked path and QoS policy

Literal wiring layer for `procedure.md`. Operation names in the procedure's Tools table map to the
calls below.

Written against the Prisma SD-WAN Unified APIs specification (OpenAPI 3.0, version label "Latest"),
checked 2026-10-14. Field and example shapes are restated with placeholder values.

## Base and version pinning

SD-WAN calls go to the gateway `https://api.sase.paloaltonetworks.com` with the path prefix shown on
each route. The token call goes to a separate authentication host,
`https://auth.apps.paloaltonetworks.com` (next section). Both hosts are the ones the specification
declares. Every route below is pinned to the
newest version the specification lists for it; older versions of the same routes also exist and are
not used. Pinned versions: sets 2.0, set status 2.0, stacks 2.0, path rules 2.5, QoS rules 2.2, site
4.13, profile 2.1. The specification also lists policy-set and rule routes at 3.0 and 3.1 under an
"original" path-policy tag; those are the legacy model and are out of scope.

All bodies are JSON. Errors come back as HTTP 400 with `{"_error": [{"code": "<CODE>"}, ...]}`.

## authenticate

Reference only; the procedure assumes a client already holds a token.

```
POST /oauth2/access.token        (authentication host, not the gateway)
Authorization: Basic <client_id:client_secret>
Content-Type: application/x-www-form-urlencoded
grant_type=client_credentials&scope=tsg_id:<TSG_ID>
```

Success returns `access_token`, `token_type` (Bearer), `expires_in` (the example shows 899 seconds; the
specification says tokens last about 15 minutes) and `scope`. Invalid credentials return 401. Send
`Authorization: Bearer <access_token>` on every SD-WAN call.

## read_profile

```
GET /sdwan/v2.1/api/profile
```
The specification describes this as required immediately after minting a token, else later SD-WAN
calls return 403. That is a claim made only in the specification's own descriptive text (unverified).
Use it as the retry described in `procedure.md` Patterns, not as a standing step.

## Sites

```
GET  /sdwan/v4.13/api/sites                  list_sites
GET  /sdwan/v4.13/api/sites/{site_id}        read_site
PUT  /sdwan/v4.13/api/sites/{site_id}        update_site
```
The site record carries, among other fields, `name`, `admin_state`, `element_cluster_role`, `_etag`,
`network_policysetstack_id` (path stack), `priority_policysetstack_id` (QoS stack), and also
`security_policysetstack_id`, `nat_policysetstack_id`, and `perfmgmt_policysetstack_id`, which are out of
scope. `_etag` is required on PUT. Read the whole record, change only the stack field, and PUT the whole
record back (assumption: PUT replaces the record; the specification does not describe partial update).

For a bind, set the path or QoS stack field to the stack's identifier. Clearing a field is not
documented (unverified). Site PUT error codes relevant here: `INVALID_NETWORK_POLICY_SET_STACK`,
`INVALID_NETWORK_POLICYSETSTACK`, `INVALID_PRIORITY_POLICY_SET_STACK`,
`INVALID_PRIORITY_POLICYSETSTACK`, `DEFAULT_NETWORK_POLICYSETSTACK_NOT_AVAILABLE`,
`DEFAULT_PRIORITY_POLICYSETSTACK_NOT_AVAILABLE`, `POLICY_CONFIG_INVALID_FOR_HUB_SITE`,
`POLICYSETSTACK_CONFIG_NOT_SUPPORTED`, `INVALID_POLICY_CONFIGURATION`, `DEFAULT_POLICY_NOT_CONFIGURED`,
`INVALID_JSON_COMMON_ATTR_MISMATCH`, `INVALID_JSON_EXTRA_ATTRIBUTE`. The conditions behind them are not
described.

The specification also lists a bulk site update; its types cover only a VRF context profile and an
element system limit profile, not stack references, so it is not used.

## Policy sets and status

| Operation | Path sets | QoS sets |
|---|---|---|
| list_policy_sets | `GET /sdwan/v2.0/api/networkpolicysets` | `GET /sdwan/v2.0/api/prioritypolicysets` |
| read_policy_set | `GET .../networkpolicysets/{policy_set_id}` | `GET .../prioritypolicysets/{policy_set_id}` |
| create_policy_set | `POST .../networkpolicysets` | `POST .../prioritypolicysets` |
| update_policy_set | `PUT .../networkpolicysets/{policy_set_id}` | `PUT .../prioritypolicysets/{policy_set_id}` |
| delete_policy_set | `DELETE .../networkpolicysets/{policy_set_id}` | `DELETE .../prioritypolicysets/{policy_set_id}` |
| read_policy_set_status | `GET .../networkpolicysets/{policy_set_id}/status` | `GET .../prioritypolicysets/{policy_set_id}/status` |

(`...` is `/sdwan/v2.0/api`.) Query routes with a filter body exist for each; the filter shape is not
detailed, so listing is used.

Set body (fields from the schema; values are placeholders):

```json
{
  "name": "<name, max 128>",
  "description": "<max 256>",
  "tags": ["<up to 10>"],
  "defaultrule_policyset": false,
  "_etag": 0
}
```
Also present: `clone_from`, `send_to_element`, `region`, `disabled`, `inactive`, and their reason
fields. `_etag` is required on PUT and ignored on POST. A QoS set additionally requires
`business_priority_names` (items of `priority_name` and `priority_num`, at most 4) and
`bandwidth_allocation_schemes` (items with `business_priorities` and `bandwidth_range`, at most 4); the
inner shape of `bandwidth_range` is not detailed. A QoS set also has `default_rule_dscp_mappings`
(at most 16 items of `transfer_type`, `priority_number`, `dscp`; transfer types `RT_AUDIO`,
`RT_VIDEO`, `TRANSACTIONAL`, `BULK`). The path set schema also embeds a `policy_rules` array; creating
rules through the rule route is what this procedure uses.

The set status response carries `policy_req_state` and a set identifier. Documented values:
in progress `POLICY_REQ_PENDING`, `POLICY_CREATE_INPROGRESS`, `POLICY_REPLICATE`; failed
`POLICY_CREATE_FAILED`; completed `POLICY_CREATE_COMPLETE`, `POLICY_REQ_COMPLETE`. Which completed value
means applied to a site is not stated.

Set error codes: create/update `NAME_REQD`, `DESCRIPTION_EXCEEDS_LIMIT`, `INVALID_JSON_EXTRA_ATTRIBUTE`,
`POLICY_SET_CONFIG_INVALID_CLONE_FROM`, `INVALID_DEFAULTRULE_FLAG_OF_CLONE_FROM`,
`POLICY_SET_CONFIG_CREATION_FAILED` (update adds `READONLY_CLONE_FROM`,
`READONLY_DEFAULTRULE_POLICYSET_FLAG`). Delete: `POLICYSET_IS_IN_USE`, `POLICYSET_INVALID_STATE`. Success
on delete is 200.

## Rules

| Operation | Path rules (2.5) | QoS rules (2.2) |
|---|---|---|
| list_policy_rules | `GET /sdwan/v2.5/api/networkpolicysets/{policy_set_id}/networkpolicyrules` | `GET /sdwan/v2.2/api/prioritypolicysets/{policy_set_id}/prioritypolicyrules` |
| create_policy_rule | `POST` same path | `POST` same path |
| read_policy_rule | `GET .../networkpolicyrules/{policy_rule_id}` | `GET .../prioritypolicyrules/{policy_rule_id}` |
| update_policy_rule | `PUT` same path as read | `PUT` same path as read |
| delete_policy_rule | `DELETE` same path as read | `DELETE` same path as read |

Common rule fields: `name` (required, max 128), `description` (max 256), `tags` (max 10),
`order_number` (1 to 65535; the API default is not stated), `enabled`, `network_context_id`,
`source_prefixes_id`, `destination_prefixes_id`, `app_def_ids` (max 256, no duplicates),
`user_or_group` (`user_group_ids`, `user_ids`), `src_device_ids`, `dest_device_ids`, `_etag` (required on
PUT).

Path rule extras: `paths_allowed` holding `active_paths` (must be non-empty), `backup_paths`,
`l3_failure_paths`, each an array of `{"path_type": "<vpn|direct|servicelink|pa_vpn>", "label": "<circuit
category label>"}`; `service_context` (`type` is `ALLOWED_TRANSIT` or `REQUIRED_TRANSIT`;
`active_service_label_id` required; label types `CG_TRANSIT`, `NON_CG_TRANSIT`, `SASE`; matching
backup fields); `best_path_config` (`metric_type` `PROBE` or `LQM`, `metric` one of `LATENCY`, `JITTER`,
`PACKET_LOSS`, `INIT_FAILURE_PCT`, `DNS_TXN_FAILURE_PCT`, and `probe_config_id` for probe type).

```json
{
  "name": "<name>",
  "order_number": 1024,
  "enabled": true,
  "app_def_ids": ["<application-id>"],
  "paths_allowed": {"active_paths": [{"path_type": "vpn", "label": "<category-label>"}]}
}
```

QoS rule extras: `priority_number` (required, 1 to 4) and `dscp` as `{"value": <0-63>}`.

Path rule error codes of note: `PATHS_ALLOWED_REQUIRED`, `NETWORKPOLICY_RULE_CONFIG_INVALID_ACTIVE_PATHS`,
`POLICYRULE_CONFIG_DUPLICATE_PATHS_SPECIFIED`, `BACKUP_PATHS_NOT_ALLOWED_FOR_BEST_PATH_SELECTION`,
`METRIC_PARAMETER_MISSING`, `METRIC_TYPE_MISSING`, `METRIC_PROBE_CONFIG_ID_REQUIRED_FOR_TYPE_PROBE`,
`INVALID_METRIC_FOR_LQM_METRIC_TYPE`, `POLICYRULE_CONFIG_INVALID_SERVICE_LABEL_REQUIRED_TRANSIT`,
`POLICYRULE_CONFIG_INVALID_SERVICE_LABEL_ALLOWED_TRANSIT`, `POLICYRULE_CONFIG_ALREADY_EXISTS_FOR_THE_APPS`,
`APP_DEF_ID_LIST_SIZE_EXCEEDED`, `DUPLICATE_APP_DEF_IDS`, `INVALID_ORDER_NUMBER_MINIMUM_VAL`,
`INVALID_ORDER_NUMBER_MAXIMUM_VAL`, `INVALID_POLICYSET_STATE`, `POLICYRULE_CREATION_NOT_ALLOWED`,
`NETWORKPOLICYSET_NOT_PRESENT`. QoS: `INVALID_PRIORITY_NUMBER`, `PRIORITY_NUMBER_MINIMUM_VAL`,
`PRIORITY_NUMBER_MAXIMUM_VAL`, `PRIORITYPOLICYSET_NOT_PRESENT`, plus the shared ones. Update adds
default-rule restrictions: `INVALID_DEFAULT_RULE_FLAG`, `INVALID_DEFAULT_RULE_NAME` and
`INVALID_DEFAULT_RULE_*_UPDATE` for app, prefix, enabled flag, and network context. Delete:
`CANNOT_DELETE_DEFAULT_POLICY_RULE`, `POLICY_SET_CLONE_IN_PROGRESS`. Success on delete is 200.

## Stacks

| Operation | Path stacks | QoS stacks |
|---|---|---|
| list_policy_stacks | `GET /sdwan/v2.0/api/networkpolicysetstacks` | `GET /sdwan/v2.0/api/prioritypolicysetstacks` |
| read_policy_stack | `GET .../networkpolicysetstacks/{policy_set_id}` | `GET .../prioritypolicysetstacks/{policy_set_id}` |
| create_policy_stack | `POST .../networkpolicysetstacks` | `POST .../prioritypolicysetstacks` |
| update_policy_stack | `PUT .../networkpolicysetstacks/{policy_set_id}` | `PUT .../prioritypolicysetstacks/{policy_set_id}` |
| delete_policy_stack | `DELETE .../networkpolicysetstacks/{policy_set_id}` | `DELETE .../prioritypolicysetstacks/{policy_set_id}` |

(`...` is `/sdwan/v2.0/api`; the path parameter is named `policy_set_id` in the specification even
though it is the stack identifier.)

```json
{
  "name": "<name>",
  "description": "<optional>",
  "defaultrule_policyset_id": "<default-rule-set-id>",
  "policyset_ids": ["<set-id-1>", "<set-id-2>"],
  "_etag": 0
}
```
`policyset_ids`: 1 to 4 items, no duplicates; the order mapping to priority is an assumption (first is
highest). `defaultrule_policyset_id` is required. Path stacks also carry `legacy_policystack`,
`default_policysetstack`, `policyset_ids_update`, and a read-only expansion `policysets`. Also present:
`tags`, `region`, `disabled`, `inactive`.

Stack error codes: create/update `INVALID_DEFAULTRULE_POLICYSET_ID`,
`POLICYSETSTACK_CONFIG_DUPLICATE_POLICYSETID`, `POLICYSETSTACK_CONFIG_INVALID_POLICYSET_IDS`,
`POLICYSETSTACK_CONFIG_INVALID_POLICYSET_STATE`, `POLICYSETSTACK_CONFIG_INVALID_DEFAULTRULE_POLICYSET_STATE`,
`DEFAULT_POLICYSET_STACK_EXISTS`, `POLICYSETSTACK_CONFIG_DEFAULTRULE_POLICYSET_REQUIRED`,
`INVALID_DEFAULTRULE_POLICYSET_ID_FORMAT`, `INVALID_JSON_EXTRA_ATTRIBUTE`. Delete:
`POLICYSETSTACK_IN_USE`. Success on delete is 200.

## Error handling

Report FAILED with the HTTP status and the list of error codes returned. The specification names codes
but not their conditions beyond what their names say; do not infer a fix beyond the step's own
guidance. A 401 means the token is missing or invalid; a 403 right after minting a token is covered in
`procedure.md` Patterns. Rate limits are undocumented: back off on 429 and honor `Retry-After`.
