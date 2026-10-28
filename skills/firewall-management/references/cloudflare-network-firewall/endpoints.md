# Cloudflare Network Firewall — Endpoint Wiring

Wire-level binding for `procedure.md`. Source: Cloudflare Docs "Cloudflare Network Firewall"
(add policies, enable managed rulesets, enable IDS, use Logpush with IDS, use IP lists, form
expressions) and the Ruleset Engine Rulesets API pages (retrieved 2026-10-26 and 2026-10-28). Base URL: `https://api.cloudflare.com/client/v4`. All
calls send `Authorization: Bearer <API_TOKEN>`. `{account_id}`, `{ruleset_id}`, `{rule_id}`, and
`{phase_name}` are placeholders.

Network Firewall rules are ordinary Rulesets API objects in account-level phases:

| Phase name | Holds |
|---|---|
| `magic_transit` | Custom rules (root kind entry-point ruleset) |
| `magic_transit_managed` | The single deployment rule that executes a managed ruleset with overrides |
| `magic_transit_ids_managed` | The single execute rule that turns IDS on or off |

## Calls

| Procedure operation | Method and path | Notes |
|---|---|---|
| List rulesets | `GET /accounts/{account_id}/rulesets` | All phases; rules are not included in the list |
| Get phase entry-point ruleset | `GET /accounts/{account_id}/rulesets/phases/{phase_name}/entrypoint` | Assumption: path shape comes from the generic Rulesets API page; the Network Firewall documentation does not show it |
| Get ruleset | `GET /accounts/{account_id}/rulesets/{ruleset_id}` | Returns rules in order; 404 when not found |
| Create ruleset | `POST /accounts/{account_id}/rulesets` | From-scratch build; on a phase that already has a ruleset it can replace the deployed one |
| Add rule | `POST /accounts/{account_id}/rulesets/{ruleset_id}/rules` | Optional `position` object; returns the whole ruleset |
| Update rule | `PATCH /accounts/{account_id}/rulesets/{ruleset_id}/rules/{rule_id}` | Full rule fields, or only `position`, or both; returns the whole ruleset |
| Delete rule | `DELETE /accounts/{account_id}/rulesets/{ruleset_id}/rules/{rule_id}` | 200 with the remaining ruleset |

Token permission: `Magic Firewall Write` for the write calls (documented on the rule calls). Not
documented: the read permission name; `Magic Firewall Read` is presumed.

Validation: append `?dry_run=true` to a supported mutation to run the same checks with no change;
a successful dry run returns `result: null`. Unverified for the `magic_transit` phase.

## Rule fields

- `expression` (string, required), `action` (string, required), `description` (string, up to 4,096
  bytes), `enabled` (boolean; a new rule is enabled unless set false), `ref` (optional unique
  external identifier within the ruleset).
- `action`: `block`, or `skip` with `action_parameters: {"ruleset": "current"}` as the allow form.
  Managed deployment uses `execute` (below).
- `position`: exactly one of `{"before": "<rule_id>"}` (empty string for first),
  `{"after": "<rule_id>"}` (empty string for last), `{"index": <n>}` (starts at 1; shifts later
  rules; out of range returns 400).
- Response rule fields: `id`, `version` (per rule, unchanged by reordering), `last_updated`. Ruleset
  fields: `id`, `name` (immutable), `kind`, `phase`, `version` (increments on every change),
  `rules`. Envelope: `success`, `errors[]`, `messages[]`, `result`.

## Managed deployment

The deployment rule is `action: "execute"`, `expression: "true"`, with `action_parameters` of
`id` (managed ruleset ID), `version` (`latest`), and `overrides`. `overrides` takes `enabled`
(whole ruleset), `rules` (each `id`, `enabled`, `action`), and `categories` (each `category`,
`enabled`, `action`). The only documented action override is `log`.

## IDS deployment

The IDS phase holds one `managed`-kind ruleset supplied by Cloudflare, found by listing the account's
rulesets. The account's own root ruleset in that phase holds one rule: `action: "execute"`,
`expression: "true"`, `enabled`, and `action_parameters` with `id` set to the managed ruleset ID.
Disable or re-enable it with the rule update call, sending `enabled` together with the same
`expression`, `action`, and `action_parameters`. The IDS page writes the phase name with hyphens once
and with underscores in its request body; use the underscore form, which matches the phase list.

IDS detections are a Logpush dataset named `magic_ids_detections`. It is account-scoped, so the
Logpush job calls use `/accounts/{account_id}/` where the generic examples use `/zones/{zone_id}/`.
Output options (such as the timestamp format, unix nanoseconds by default) follow all requested fields in the job
definition. The job's own calls are described in the Logpush documentation and are not bound here.

## Placeholder bodies

Allow one port, then block all TCP (create-from-scratch form; use the rule calls when a ruleset
exists):

```json
{"name": "Example ruleset", "kind": "root", "phase": "magic_transit", "description": "Example", "rules": [
  {"action": "skip", "action_parameters": {"ruleset": "current"}, "expression": "tcp.dstport in { 8080 }", "description": "Allow port 8080"},
  {"action": "block", "expression": "tcp.dstport in { 1..65535 }", "description": "Block all TCP ports"}]}
```

Add a block rule that uses an account IP list, as the last rule:

```json
{"action": "block", "expression": "ip.src in $<LIST_NAME>", "description": "Block listed sources", "enabled": true, "position": {"after": ""}}
```

Create the IDS execute ruleset:

```json
{"name": "IDS execute ruleset", "kind": "root", "phase": "magic_transit_ids_managed", "description": "Enable IDS", "rules": [
  {"action": "execute", "expression": "true", "enabled": true, "description": "Enable IDS", "action_parameters": {"id": "<IDS_MANAGED_RULESET_ID>"}}]}
```

Disable IDS (rule update body):

```json
{"enabled": false, "expression": "true", "action": "execute", "action_parameters": {"id": "<IDS_MANAGED_RULESET_ID>"}}
```

Move a rule to the front:

```json
{"position": {"before": ""}}
```

## Related calls (lists)

IP lists are created and filled through the account lists calls (`POST /accounts/{account_id}/rules/lists`
with `kind: "ip"`, then `POST /accounts/{account_id}/rules/lists/{list_id}/items` with `{"ip": "<address or CIDR>"}`
items). The lists documentation shows an email-and-key header rather than a bearer token.
Unverified: whether a bearer token works. List management is not part of this procedure.

## Error text worth recognizing

- `ruleset exceeds complexity constraints` (HTTP 400): the expression or ruleset is too complex;
  split the expression across several rules.
- HTTP 400 on a position `index` outside the list.
- HTTP 404 from a ruleset read: the ruleset does not exist (or, for a managed ruleset, the account
  is not entitled to it).
