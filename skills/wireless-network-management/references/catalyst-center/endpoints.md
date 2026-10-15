# Endpoint Wiring — Cisco Catalyst Center SSID Create and Provision

Literal API calls behind each capability named in `procedure.md`. Base URL:
`https://<cluster-ip-or-fqdn>`. Auth: session token from
`POST /dna/system/api/v1/auth/token`, used as `X-Auth-Token` on subsequent calls.

## Create and Provision SSID

Tool hint: `POST /dna/intent/api/v1/business/ssid`.

Documented description (verbatim): "Creates SSID, updates the SSID to the corresponding site
profiles and provision it to the devices matching the given sites."

Body: `managedAPLocations` (array of strings — verbatim field description: "Managed AP Locations
(Enter entire Site(s) hierarchy)"), `ssidDetails` (object), `ssidType` (`Guest`|`Enterprise`),
`enableFabric` (boolean — verbatim: "Enable SSID for Fabric").

`ssidDetails` fields: `name` (string, required), `securityLevel` (required enum:
`WPA2_ENTERPRISE`|`WPA2_PERSONAL`|`OPEN`|`WEB_AUTH`), `passphrase` (string — verbatim: "Only
applicable for SSID with PERSONAL auth type"), `radioPolicy` (enum: `5GHz only`|`2.4GHz only`|
`6GHz only`|band-operation variants), `authKeyMgmt` (array: `dot1x`|`psk`|`owe`|`sae`),
`enableBroadcastSSID` (boolean), `enableFastLane` (boolean), `trafficType`, `fastTransition`,
`webAuthURL`, MAC filtering options, cipher suite toggles. A `flexConnect`-related field is
documented as "Applicable for non fabric profile" — confirms this call supports non-fabric
deployments in addition to fabric ones.

**Async behavior:** requires the `__persistbapioutput` header (documented as indicating async
execution). Response includes `executionId` and `executionStatusUrl` for polling task status — the
initial response is not completion.

No example JSON payload was found in the extracted source pages — construct the body from the field
descriptions above and confirm against the live API reference/Swagger UI for the target cluster
version before relying on field names verbatim.

## Update SSID

Tool hint: reference page title "Update SSID" (Catalyst Center API 2.3.7.7) — "allows users to
update an SSID at a given site." Exact path/method not confirmed beyond the operation's existence in
this extraction pass; likely follows the same `/dna/intent/api/v1/business/ssid`-family convention —
confirm against the live API reference for the target cluster version.

## Add, Update, or Remove SSID Mapping to a VLAN (fabric-specific)

Tool hint: `PUT /dna/intent/api/v1/sda/fabrics/{fabricId}/vlanToSsids`.

`fabricId` (path parameter, verbatim: "represents the Fabric ID of a particular Fabric Site").

Body: array of `{"vlanName": "string", "ssidDetails": [{"name": "string (required)",
"securityGroupTag": "string"}]}`.

Documented behavior (verbatim): "Add, update, or remove SSID mappings to a VLAN. If the payload
doesn't contain a 'vlanName' which has SSIDs mapping done earlier then all the mapped SSIDs of the
'vlanName' is cleared."

Responses: `200` — returns `taskId` and `url`; `202` — successful (async) operation; `400`, `404`,
`500` — error responses.

## Task/Execution Status Polling

Tool hint: follow the `executionStatusUrl` (Create and Provision SSID) or the `url` returned
alongside `taskId` (VLAN mapping call) to check completion state. Exact terminal-state value
vocabulary was not confirmed in this extraction pass — confirm against the live API reference for the
target cluster version.
