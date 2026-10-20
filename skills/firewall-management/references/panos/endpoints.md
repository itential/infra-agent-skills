# Endpoint Wiring — PAN-OS / Panorama Firewall Policy Management

Literal API calls behind each capability named in `procedure.md`. Base URL: `https://<firewall-or-
panorama-address>`. The path segment `v11.0` below tracks the target PAN-OS/Panorama release —
confirm the correct version segment for the target device rather than assuming `v11.0` applies
universally. Auth: API key passed via the `X-PAN-KEY` request header (a query-parameter form of the
key exists on older PAN-OS releases but the header form is the current documented practice).

Citation: Palo Alto Networks, PAN-OS/Panorama API documentation (PAN-OS 11.1 doc set,
docs.paloaltonetworks.com), retrieved 2026-09-17. Panorama additions (post-rules, move, push) were checked against the 11.1 REST
and XML API pages ("Resource Methods and Query Parameters (REST API)", "Work with Policy Rules on
Panorama (REST API)", "Commit-All"), retrieved 2026-10-19. Field/path names below are reproduced from the
vendor's actual wire format (JSON keys, path segments) since those are literal interface contracts,
not prose to rephrase — only descriptive text is original wording.

## Create an address object

Tool hint: `POST /restapi/v11.0/Objects/Addresses`

Query parameters: `location` (`shared`, or `vsys` paired with `vsys=<name>` on a firewall only, or
`device-group` paired with `device-group=<name>` on Panorama only), `name` (the object's name).

Body:
```json
{
  "entry": [{
    "@location": "shared",
    "@name": "<object-name>",
    "description": "<optional description>",
    "fqdn": "<fqdn-value>",
    "tag": {"member": ["<tag-name>"]}
  }]
}
```
Use `ip-netmask`, `ip-range`, or `ip-wildcard` in place of `fqdn` for other address types (only
`fqdn` and `ip-netmask` were directly confirmed against this documentation pass — confirm the exact
field name for other types against the target version before use).

Response (success): `{"@status": "success", "@code": "20", "msg": "command succeeded"}`

## Read address object(s)

Tool hint: `GET /restapi/v11.0/Objects/Addresses`

Query parameters: `location`, and `vsys`/`device-group` as above when applicable. Omit `name` for a
list read; include it to read a single object.

## Update an address object

Tool hint: `PUT /restapi/v11.0/Objects/Addresses`

Query parameters and body: same shape as create, addressed to the existing object's `location` and
`name`.

## Delete an address object

Tool hint: `DELETE /restapi/v11.0/Objects/Addresses`

Query parameters: `location`, `name`, and `vsys`/`device-group` as applicable.

## Rename an address object

Tool hint: `POST /restapi/v11.0/Objects/Addresses:rename`

Query parameters: `location`, `name` (current name), `newname` (target name).

## Create a security policy rule

Tool hint: `POST /restapi/v11.0/Policies/SecurityRules` (vsys-scoped) — Panorama pre-rulebase uses
`POST /restapi/v11.0/Policies/SecurityPreRules` instead (the post-rulebase equivalent was not
independently confirmed by name this pass; check the target version's reference before assuming a
`SecurityPostRules` path).

Query parameters: `location` (`vsys` with `vsys=<name>`, or `device-group` with
`device-group=<name>`), `name` (the rule's name).

Body:
```json
{
  "entry": [{
    "@location": "vsys",
    "@name": "<rule-name>",
    "@vsys": "<vsys-name>",
    "action": "allow",
    "application": {"member": ["<app-name>"]},
    "category": {"member": ["any"]},
    "destination": {"member": ["any"]},
    "from": {"member": ["<zone-name>"]},
    "to": {"member": ["<zone-name>"]},
    "source": {"member": ["any"]},
    "source-user": {"member": ["any"]},
    "source-hip": {"member": ["any"]},
    "destination-hip": {"member": ["any"]},
    "service": {"member": ["application-default"]}
  }]
}
```

Response (success): `{"@status": "success", "@code": "20", "msg": "command succeeded"}`

Documented error example: `{"code": 3, "message": "Invalid Object", "details": [...]}` — treat
`code: 3` / `"Invalid Object"` as indicating the payload referenced a field or object PAN-OS didn't
recognize, and re-check field names/values rather than retrying unchanged.

## Read / update / delete a security policy rule

Tool hint: same path family as create (`Policies/SecurityRules` or `Policies/SecurityPreRules`), with
method `GET` (read), `PUT` (update, same body shape as create), or `DELETE` (delete) respectively, and
`location`/`name`/`vsys`/`device-group` query parameters addressing the target rule.

## Security post-rules, rename and move (Panorama)

Post-rule family: `/restapi/v11.0/Policies/SecurityPostRules` (name taken from a third-party OpenAPI
description; the vendor page confirms post-rules exist as a REST resource on Panorama but did not print the
path, so treat the literal path as assumed). Same methods and parameters as `SecurityPreRules`.

Rename (any rule or object family): `POST <family>:rename` with `location`, `name`, `newname`.

Move: `POST <family>:move` with `location`, `name`, `where` (`top`, `bottom`, `before`, `after`) and
`dst` (sibling rule name, required for `before`/`after`). Verified for policy rules in the vendor's
methods table; also applies to `SecurityRules`, `SecurityPreRules`, `SecurityPostRules`.

## NAT rules — family names unverified

Assumed from a third-party OpenAPI description (secondary source), not found in the vendor pages reached:
`/restapi/v11.0/Policies/NatPreRules` and `/restapi/v11.0/Policies/NatPostRules` (Panorama). The
firewall-side NAT family name was not found in any source reached. Same
parameters, `:rename` and `:move` as security rules. Confirm against the device's own API reference
(`/restapi-doc/` on the target, per the vendor) before use.

## Commit — requires the XML API (not the REST API)

The REST API documentation available for this pass states it covers only a subset of firewall/
Panorama configuration, and that commit specifically requires the XML API. Confirmed: the XML API's
`type=commit` request parameter supports both a full commit and a partial/scoped commit. The exact
request body (cmd XML shape), response job-ID field name, and the precise `type=op` job-status query
used to poll a commit job to completion were not confirmed during this pass — consult the target
PAN-OS version's own XML API reference for those exact literal parameters before relying on them.

## Push to managed devices (XML API, Panorama only)

Tool hint: `POST /api/` with form fields `type=commit`, `action=all`, and `cmd` set to a push
command. The vendor's Commit-All page shows shared-policy push to a device group as a command whose
body names the device group by entry name under a shared-policy element; a third-party OpenAPI description shows a Panorama commit call with `type=commit` and `cmd=<commit></commit>`, and
`type=commit-all` with a shared-policy command for the push (a different `type`/`action` spelling than
the vendor page — confirm which the target version accepts). Optional elements named by the vendor:
`include-template` (set to no to leave template changes out) and `validate-only` (check without
pushing). `force-template-values` and `merge-with-candidate-cfg` exist but their details were not
reached. Response carries a job id.

Commit body shapes confirmed from the vendor's Commit page (10.1 doc set): a plain commit, a force
commit, and an admin-scoped commit naming administrators as members. Job polling: `type=op` with a
show-jobs command carrying the job id; the response reports a status (active/finished), a result
state, and progress percentage. Treat success only when the job has finished with a successful
result.

Documented limitation: the push affects only firewalls directly in the named device group, not those
in its child device groups.
