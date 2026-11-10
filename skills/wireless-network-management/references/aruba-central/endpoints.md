# Endpoint Wiring — HPE Aruba Networking Central WLAN Provisioning and Monitoring

Literal API calls behind each capability named in `procedure.md`. Base URL: the target Central
account's regional API gateway (per Aruba's OAuth setup). Auth: OAuth 2.0 client credentials.
The read operations below are bound to REST calls; the write operations are not (see the last section).

## Get a List of WLANs

Tool hint: `GET /network-monitoring/v1/wlans`.

Query parameters: `site-id` (optional — "ID of the Site for which access point related information is
requested"), `serial-number` (optional — "Serial number of an access point device"), `filter`
(optional — OData v4 filter string, "Supports only 'and' conjunction"), `sort` (optional —
comma-separated; supported fields `wlanName`, `band`, `status`, `securityLevel`, `security`, `vlan`),
`limit` (optional, default 20, max 1000), `next` (optional — pagination cursor).

Example response:
```json
{
  "items": [
    {
      "wlanName": "wlan1",
      "securityLevel": "Personal",
      "security": "Enhanced Open",
      "band": "2.4 GHz, 5 GHz",
      "status": "ENABLED",
      "vlan": "1",
      "clientCount": 15,
      "id": "wlans/wlan1",
      "type": "network-monitoring/access-point-monitoring"
    }
  ],
  "count": 1,
  "total": 1,
  "next": null
}
```

## Get a Specific WLAN

Tool hint: `GET /network-monitoring/v1/wlans/{wlan-name}` (per the reference page name
`getwlanv1` — "retrieves detailed information about a specific WLAN").

## Get the Throughput Trend for a WLAN

Tool hint: reference page `getwlanthroughputtrendv1` — "retrieves throughput trend data for a
specific WLAN." Exact path not confirmed in this extraction pass beyond the operation's existence;
follow the same `/network-monitoring/v1/wlans/...` base path convention and confirm the exact
sub-resource against the live API reference before relying on a guessed path.

## Get a List of Access Point WLANs

Tool hint: reference page `getaccesspointwlanlistv1` — "retrieves a list of WLANs associated to an
access point."

## Get the Throughput Trend for a WLAN of an Access Point

Tool hint: reference page `getaccesspointwlanthroughputv1`.

## Write operations: Central console binding (no REST route published)

Create SSID profile, Set VLAN and forwarding, Set security, Set access rules, Edit SSID profile,
Disable SSID, and Delete SSID profile have no published REST route. The documented binding is the
console, operating on a configuration group that contains at least one AP:

- Navigation (ArubaOS 10 and Instant AP groups): select the group, then Manage > Devices > Access
  Points, the Config icon, and the WLANs tab, which lists the group's Wireless SSIDs.
- Create: "+ Add SSID". Edit: select the row, then the edit icon. Disable: select the row, then the
  disconnect icon and confirm. Delete: select the row, then the delete icon and confirm.
- Wizard tabs for an ArubaOS 10 SSID: General, VLANs, Security, Access, Summary. Security uses
  Advanced Settings for MAC authentication, reauthentication, denylisting, and DHCP enforcement.
- Instant AP groups use Configuration > Wireless > group > Networks, then "+"; Basic Settings, then
  VLAN. The Extended SSID setting is under System > General.

If the caller's client exposes a write operation for these steps, bind to that. The account's API
Gateway (Maintain > Organization > Platform Integration > REST API) publishes a Swagger listing of
the operations supported by the current software release; check it before assuming one exists.

API access facts from the same guide: access tokens last two hours and cannot be extended; the
refresh token lasts 14 days and refreshing invalidates the previous access token; tokens cannot be
generated through federated SSO users. Starting rate limit is 5,000 calls per day and 7 per second,
and scales with subscribed devices.

## Not documented / not found (flagged, not guessed)

No create, update, or delete endpoint for WLAN/SSID configuration was found in Aruba's public API
reference (Classic Central and New Central). A Python SDK workflow (`create_ssid_workflow.py`, using
the `pycentral` SDK) exists but does not expose its underlying REST calls. See `procedure.md`'s Known
limitations.
