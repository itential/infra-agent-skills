# Endpoint Wiring — PAN-OS / Panorama Firewall Policy Management

Literal API calls behind each capability named in `procedure.md`. Base URL: `https://<firewall-or-
panorama-address>`. The path segment `v11.0` below tracks the target PAN-OS/Panorama release —
confirm the correct version segment for the target device rather than assuming `v11.0` applies
universally. Auth: API key passed via the `X-PAN-KEY` request header (a query-parameter form of the
key exists on older PAN-OS releases but the header form is the current documented practice).

Citation: Palo Alto Networks, PAN-OS/Panorama API documentation (PAN-OS 11.1 doc set,
docs.paloaltonetworks.com), retrieved 2026-09-17. Field/path names below are reproduced from the
vendor's actual wire format (JSON keys, path segments) since those are literal interface contracts,
not prose to rephrase — only descriptive text is original wording.

## Create an address object

Tool hint: `POST /restapi/v11.0/Objects/Addresses`

Query parameters: `location` (`shared`, or `vsys` paired with `vsys=<name>`, or `device-group`
paired with `device-group=<name>`), `name` (the object's name).

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

## NAT rules — path not confirmed this pass

No NAT-specific REST path was found in the documentation reachable during this research pass. Do not
assume a `Policies/NATRules` (or similarly-named) path is correct without checking the target
version's own current API reference first — see `procedure.md`'s Known limitations.

## Commit — requires the XML API (not the REST API)

The REST API documentation available for this pass states it covers only a subset of firewall/
Panorama configuration, and that commit specifically requires the XML API. Confirmed: the XML API's
`type=commit` request parameter supports both a full commit and a partial/scoped commit. The exact
request body (cmd XML shape), response job-ID field name, and the precise `type=op` job-status query
used to poll a commit job to completion were not confirmed during this pass — consult the target
PAN-OS version's own XML API reference for those exact literal parameters before relying on them.
