# Cisco Catalyst Center — SSID Create and Provision Procedure

Create an SSID, map it to site profiles, and provision it to matching devices in Cisco Catalyst
Center (formerly Cisco DNA Center) via the Intent API. Covers both fabric and non-fabric (traditional)
wireless deployments through the same create call. Assumes an authenticated REST client (a session
token obtained via the platform's auth endpoint) against the target Catalyst Center cluster is already
available.

**Critical operational note up front: this is an asynchronous, multi-stage operation.** The create
call itself returns quickly with an execution/task identifier — it does not mean the SSID has actually
been created, mapped, and provisioned to devices yet. Every procedure below that triggers a
create/update must be followed by polling that identifier to confirm actual completion.

## Operational procedure

### Common Sequences

**Provision a new SSID to a set of sites (the common ask):**
1. **Stop and confirm with the operator before proceeding** if the target `managedAPLocations`
   includes any site already serving live production traffic — this pushes real configuration to
   devices actively serving clients, not a staging/preview action.
2. Create and Provision SSID — with the target sites (`managedAPLocations`), SSID details, and
   `enableFabric` set according to whether the target sites are SD-Access fabric or traditional.
3. Poll the execution status using the returned `executionId`/`executionStatusUrl` until it reports
   completion — do not report success from the initial `202`-equivalent response alone.
4. Once complete, confirm the SSID is actually live on the target devices (see Patterns).

**Update an existing SSID's site mapping or fabric VLAN association:**
1. **Stop and confirm with the operator before proceeding** — same production-impact reasoning as
   create, plus the destructive-on-omission VLAN-mapping behavior below.
2. Update SSID (non-fabric attribute changes) or the SSID-to-VLAN mapping call (fabric-specific), per
   which aspect is changing.
3. Poll the returned task identifier to confirm completion, same as create.

### Create and Provision SSID

Body has four top-level parts: `managedAPLocations` (array of full site hierarchy strings — the
sites this SSID is provisioned to), `ssidDetails` (the SSID's own configuration), `ssidType`
(`Guest` or `Enterprise`), and `enableFabric` (boolean — whether this SSID is fabric-enabled).

Within `ssidDetails`: `name` (required), `securityLevel` (required — `WPA2_ENTERPRISE`,
`WPA2_PERSONAL`, `OPEN`, or `WEB_AUTH`), `passphrase` (only applicable for PERSONAL auth type —
mirrors Meraki's same PSK-only restriction), `radioPolicy` (band selection), `authKeyMgmt` (array —
`dot1x`, `psk`, `owe`, `sae`), plus broadcast/fast-lane/traffic-type/fast-transition/web-auth-URL/MAC-
filtering/cipher-suite options.

**This call is asynchronous.** Request the async execution header (per the API's own required-header
convention) and expect a response carrying an execution identifier and a status-check URL, not an
immediately-complete result — see `endpoints.md` for the exact header/field names.

Confirm success: poll the execution status endpoint until it reports a terminal state; only then
consider the SSID actually created and provisioned. A "successfully accepted" initial response is not
completion.

### Update SSID / Add-Update-Remove SSID-to-VLAN Mapping (fabric-specific)

For fabric deployments, SSID-to-VLAN association is a separate call from the SSID's own
create/update — scoped per fabric site (`fabricId` in the path), taking an array of
`{vlanName, ssidDetails: [{name, securityGroupTag}]}` mappings.

**Submitting a payload without a `vlanName` that previously had SSID mappings clears all of that
VLAN's existing mappings** — this is documented platform behavior, not a bug: "If the payload doesn't
contain a 'vlanName' which has SSIDs mapping done earlier then all the mapped SSIDs of the 'vlanName'
is cleared." Always include every VLAN mapping that should remain in the payload, not just the ones
being changed — a partial payload here is destructive to the omitted VLANs' mappings, unlike a typical
partial-update semantic.

This call also returns a task identifier to poll, same pattern as create.

## Patterns

- **Every write here is fire-and-poll, never fire-and-forget.** The API's own async convention (an
  execution/task identifier plus a status URL) exists specifically because SSID provisioning involves
  real device configuration pushes that take time — reporting success from the initial response alone
  will produce false positives when the actual device push later fails.
- **The VLAN-mapping call's "omission clears it" semantics is the opposite of typical partial-update
  behavior.** Most REST PATCH/PUT calls in this general domain (see this skill's other platforms, and
  `dns-record-management`'s various vendors) treat an omitted field as "leave unchanged." This specific
  call treats an omitted `vlanName` as "clear its mappings" — read the full current mapping state
  before submitting an update here, the same "don't submit a partial array against a full-overwrite
  semantic" discipline that matters for Azure DNS record sets and PowerDNS's REPLACE changetype.
- **One create call, two deployment models.** `enableFabric` is what determines fabric vs. non-fabric
  behavior on the same `POST /business/ssid` call — don't assume a different endpoint is needed for
  each; the split happens inside the payload, not at the URL level.

## Known limitations

- Covers SSID create/provision and fabric SSID-to-VLAN mapping — does not cover AP Profile creation,
  RF profile management, or general device provisioning/onboarding (separate Catalyst Center Intent
  API areas not covered here).
- Async completion polling logic (exact terminal-state values, retry/backoff guidance) is not fully
  detailed in the source — confirm the specific status values the target cluster's API
  version returns before assuming a fixed set.
- No documented rollback/undo exists for a completed SSID provisioning push — reversal means issuing
  another create/update call with the desired reverted state, following the same async poll pattern.

## Tools

Every operation below maps to the Cisco Catalyst Center Intent API — see `endpoints.md` for the
literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| Create and Provision SSID | Create an SSID, map to site profiles, provision to matching devices (fabric or non-fabric) | SSID Management |
| Update SSID | Update an existing SSID's configuration at a given site | SSID Management |
| Add/Update/Remove SSID-to-VLAN Mapping | Associate SSIDs with VLANs within a fabric site (destructive on omission — see Patterns) | Fabric Wireless |
| Task/Execution Status | Poll an async operation's identifier until completion | Task Management |

## Verification checklist

- [ ] Every create/update call's returned execution/task identifier was polled to a terminal state —
      no outcome was reported from the initial async-accepted response alone
- [ ] `enableFabric` was set deliberately based on the target sites' actual deployment model, not
      defaulted
- [ ] A VLAN-mapping update included every VLAN mapping that should remain, not just the ones being
      changed — confirmed against current state first if there was any doubt
- [ ] `securityLevel`/`passphrase` pairing matches the documented PERSONAL-only restriction on
      `passphrase`, mirroring the same rule other platforms in this category enforce
