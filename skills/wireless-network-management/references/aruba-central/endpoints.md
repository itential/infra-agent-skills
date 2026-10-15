# Endpoint Wiring — HPE Aruba Networking Central WLAN Monitoring (Read-Only)

Literal API calls behind each capability named in `procedure.md`. Base URL: the target Central
account's regional API gateway (per Aruba's OAuth setup). Auth: OAuth 2.0 client credentials.

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

## Not documented / not found (flagged, not guessed)

No create, update, or delete endpoint for WLAN/SSID configuration was found in Aruba's public API
reference (checked both Classic Central and New Central). The only documented provisioning path is a
Python SDK workflow script (`create_ssid_workflow.py`, using the `pycentral` SDK) that does not expose
its underlying REST calls on the documentation page. See `procedure.md`'s Known limitations.
