# Endpoint Wiring — Cisco Meraki SSID Provisioning

Literal API calls behind each capability named in `procedure.md`. Base URL:
`https://api.meraki.com/api/v1`. Auth: `X-Cisco-Meraki-API-Key: <key>` header.

## List Network Wireless SSIDs

Tool hint: `GET /networks/{networkId}/wireless/ssids`.

Response: array of SSID objects, `number` 0-14, e.g.:
```json
{
  "number": 0,
  "name": "My SSID",
  "enabled": true,
  "authMode": "8021x-radius",
  "psk": "deadbeef",
  "encryptionMode": "wpa",
  "wpaEncryptionMode": "WPA2 only",
  "radiusServers": [{"host": "1.2.3.4", "port": 1812}],
  "ipAssignmentMode": "NAT mode",
  "vlanId": 100,
  "bandSelection": "5 GHz band only"
}
```

## Get Network Wireless SSID

Tool hint: `GET /networks/{networkId}/wireless/ssids/{number}`.

## Update Network Wireless SSID

Tool hint: `PUT /networks/{networkId}/wireless/ssids/{number}` — `number` is 0-14.

Key body fields: `name` (string), `enabled` (boolean), `authMode` (one of 15 enum values including
`open`, `psk`, `8021x-radius`, `8021x-meraki`), `encryptionMode` (`wep`|`wpa`, PSK contexts only),
`psk` (string — "only valid if authMode is 'psk'"), `wpaEncryptionMode` (6 options, e.g. "WPA2 only"
through "WPA3 192-bit Security"), `ipAssignmentMode` (`NAT mode`|`Bridge mode`|`Layer 3 roaming`|etc.),
`vlanId` (integer), `useVlanTagging` (boolean), `radiusServers` (array of
`{host, port, secret, radsecEnabled}`), `radiusAccountingEnabled` (boolean), `radiusFailoverPolicy`
(`Allow access`|`Deny access`), `splashPage` (13 enum values), `walledGardenEnabled` +
`walledGardenRanges` (array), `bandSelection`, `mandatoryDhcpEnabled`, `ssidAdminAccessible` (boolean).

Response: `200` with the updated SSID object.

**Live-verified error (not in the docs page fetched, confirmed via a real production build):**
attempting `authMode: 8021x-radius` with no `radiusServers` entry returns a rejection with message
text to the effect of "Authentication mode requires RADIUS 802.1X servers."

**Live-verified response gap:** the `200` response does not always include `vlanId` in the echoed
object even when the submitted value was applied and is visible on a subsequent GET — confirmed
across a real test sequence where `name`/`authMode`/`psk`/`isolation` were all correctly echoed but
`vlanId` was missing from the same response.
