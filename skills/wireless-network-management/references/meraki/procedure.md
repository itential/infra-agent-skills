# Cisco Meraki — SSID Provisioning Procedure

Create (by configuring an existing numeric slot) and update an SSID on a Meraki-managed wireless
network via the Meraki Dashboard API v1. Assumes an authenticated REST client (an API key with
`X-Cisco-Meraki-API-Key` header, scoped with dashboard API access on the target organization) is
already available.

**Critical scope note up front: Meraki has no "create SSID" endpoint.** Every Meraki network ships
with SSID slots numbered 0-14, always present, initially disabled with a default name. "Creating" an
SSID means finding a currently-disabled/unused slot and configuring it via the same update call used
for any other SSID change — there is no POST-a-new-SSID operation to reach for.

## Operational procedure

### Common Sequences

**Provision a new SSID (the "create" case):**
1. List Network Wireless SSIDs — find a slot that's currently disabled or holds a placeholder/default
   name, to use as the target. Never overwrite a slot already carrying a real production SSID without
   explicit confirmation that slot is the intended target.
2. Update Network Wireless SSID against that slot's number — set `name`, `enabled: true`, `authMode`,
   and the auth-mode-specific fields (see Patterns for the `8021x-radius` requirement).
3. **Confirm via a follow-up Get Network Wireless SSID** — do not trust the update response alone for
   every field; see the known `vlanId` echo gap in Patterns.

**Update an existing SSID's configuration (e.g. change the PSK, or toggle a feature):**
1. Update Network Wireless SSID against the known slot number, with the changed fields.
2. Confirm via a follow-up Get.

**Disable/retire an SSID (there is no delete):**
1. Update Network Wireless SSID against the slot, setting `enabled: false`. This is the only "removal"
   path — the slot itself is never deleted, only disabled and left at its current or a placeholder
   configuration.

### List Network Wireless SSIDs

Returns all 15 SSID slots (0-14) for the network, each with its full current configuration. Use this
to find an available slot before provisioning, or to confirm current state before changing anything.

### Update Network Wireless SSID

The single mechanism for create, update, and disable — same call, different field values. Key fields:
`name`, `enabled`, `authMode` (open/psk/8021x-radius/8021x-meraki/and others), `encryptionMode` (wep/wpa,
PSK contexts only), `psk` (only valid when `authMode` is `psk`), `wpaEncryptionMode`, `ipAssignmentMode`
(NAT mode / Bridge mode / Layer 3 roaming / etc.), `vlanId` (relevant for tagging/concentrator modes),
`radiusServers` (array of `{host, port, secret, radsecEnabled}` — required for `8021x-radius`, see
Patterns), `splashPage`, `bandSelection`, `mandatoryDhcpEnabled`.

**Stop and confirm with the operator before updating a slot already carrying a live production SSID**
— this affects connected clients immediately; changing `psk`, `authMode`, or disabling the SSID drops
existing associations.

Confirm success: response `200` with the updated SSID object echoed back — **but see Patterns for a
known gap where `vlanId` is not always echoed even when applied.**

## Patterns

- **`8021x-radius` hard-requires a configured RADIUS server — live-verified, not just documented.**
  Attempting to set `authMode: 8021x-radius` without a `radiusServers` entry returns an explicit
  rejection ("Authentication mode requires RADIUS 802.1X servers"). Always include at least one RADIUS
  server (`host`, `port`, `secret`) when using this auth mode — there is no way to stage the SSID
  without one first.
- **The PUT response does not reliably echo every field back, even when the change actually applied —
  live-verified for `vlanId`.** A production build observed the update succeed and every other field
  (name, authMode, psk, isolation) confirmed correctly in the response, but `vlanId` sometimes missing
  from the echoed object despite being submitted and actually taking effect. **Always follow up with a
  Get Network Wireless SSID call to independently confirm VLAN tagging** rather than trusting the PUT
  response's completeness for that field specifically.
- **Slot reuse is the only way to add an SSID once all 15 are in use.** If every slot 0-14 already
  holds an active SSID, "adding a new one" means reconfiguring (and therefore replacing) an existing
  slot — there is no 16th slot. Confirm with the operator which existing SSID is being replaced before
  proceeding in this case; this is a materially different action than filling an empty slot.

## Known limitations

- No create or delete operation exists — provisioning is "configure an available slot," retirement is
  "disable a slot." There is no way to permanently remove a slot itself.
- Only 15 SSID slots (0-14) exist per network — this is a hard platform ceiling, not a configurable
  limit.
- `8021x-radius` requires a real RADIUS server to be reachable and correctly configured for actual
  client authentication to work — satisfying the API's validation (a syntactically valid
  `radiusServers` entry) is necessary but not sufficient for a functioning deployment.
- No documented auto-abort/rollback exists for an SSID update — an update takes effect immediately;
  reversal means submitting another update with the prior values, and only if they were captured
  beforehand.

## Tools

Every operation below maps to the Meraki Dashboard API v1 — see `endpoints.md` for the literal
request/response shape.

| Operation | Description | Category |
|---|---|---|
| List Network Wireless SSIDs | Read all 15 SSID slots and their current configuration | SSID Management |
| Get Network Wireless SSID | Read one SSID slot's current configuration | SSID Management |
| Update Network Wireless SSID | Configure a slot — the only create/update/disable mechanism | SSID Management |

## Verification checklist

- [ ] An available (disabled or placeholder) slot was identified via List before treating an update as
      a "create," or the operator explicitly confirmed replacing an active slot
- [ ] `8021x-radius` auth mode included at least one valid `radiusServers` entry before submission
- [ ] A follow-up Get confirmed the full configuration post-update — `vlanId` specifically was checked
      independently, not trusted from the update response alone
- [ ] A change to a slot already carrying a live SSID was confirmed with the operator before
      submission
