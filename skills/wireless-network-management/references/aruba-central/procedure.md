# HPE Aruba Networking Central — WLAN Monitoring Procedure (Read-Only)

Read WLAN/SSID configuration state and throughput data from HPE Aruba Networking Central ("New
Central" — the current API generation) via its REST API. **This skill is read-only by design, not by
choice** — see Known limitations for why create/update isn't covered. Assumes an authenticated OAuth
2.0 client against the target Central account is already available.

## Operational procedure

### Common Sequences

**Check current WLAN configuration/status across a site (audit, not provisioning):**
1. Get a List of WLANs — filtered by site or access point serial number as needed.
2. For a specific WLAN of interest, Get a Specific WLAN for full detail.

**Check WLAN health/utilization:**
1. Get the Throughput Trend for a WLAN (network-wide) or for a WLAN of a specific Access Point.

### Get a List of WLANs

Lists WLANs associated with a customer account, optionally filtered by `site-id` or access point
`serial-number`, with an OData-style `filter` parameter (limited — only `and` conjunction supported)
and sortable by `wlanName`, `band`, `status`, `securityLevel`, `security`, or `vlan`. Paginated —
default page size 20, max 1000, cursor-based continuation via `next`.

Confirm success: response includes an `items` array; each entry's `id` (e.g. `wlans/wlan1`) is what a
follow-up Get a Specific WLAN call needs.

### Get a Specific WLAN

Retrieves full detail for one WLAN by name/ID. Use after a List call has identified the WLAN of
interest, or directly if the exact identifier is already known.

### Get Throughput Trend

Two variants: network-wide WLAN throughput trend, or throughput trend scoped to a specific access
point's view of that WLAN. Use the AP-scoped variant when troubleshooting a specific AP's client
experience rather than the WLAN in aggregate.

## Patterns

- **This is a read/monitoring surface, not a provisioning one.** Every operation here answers "what's
  configured / how is it performing" — none of them change configuration. Don't build a workflow on
  this skill that assumes it can also create or modify a WLAN; it can't (see Known limitations).
- **The `filter` parameter's OData support is limited to `and`.** Don't assume full OData v4
  expressiveness (`or`, nested grouping) is available — check the target account's actual filter
  behavior if a more complex query is needed, or fetch broader and filter client-side instead.

## Known limitations

- **No documented create/update/delete WLAN or SSID endpoint exists in Aruba's current public REST
  API reference** (checked both the "Classic Central" and "New Central" API generations). The only
  publicly documented way to provision a WLAN via automation is a Python SDK (`pycentral`) workflow
  script that wraps undocumented underlying calls — those calls were not reverse-engineered for this
  skill, per an explicit scoping decision to stay within what's actually documented rather than
  reverse-engineer an unofficial mechanism. If write capability becomes a real requirement, that's the
  next research step (either wait for Aruba to publish a write endpoint, or deliberately reverse-
  engineer the SDK's calls with that explicit tradeoff acknowledged).
- Covers WLAN listing, detail retrieval, and throughput trending only — does not cover site/group
  management, RF profiles, client-level detail, or guest/captive-portal configuration.
- Requires OAuth 2.0 client credentials already provisioned in the target Central account — this
  skill does not cover initial app registration/token setup.

## Tools

Every operation below maps to the Aruba Central "New Central" REST API — see `endpoints.md` for the
literal request/response shape.

| Operation | Description | Category |
|---|---|---|
| Get a List of WLANs | List WLANs for a customer account, filterable by site/AP | WLAN Monitoring |
| Get a Specific WLAN | Read detailed configuration for one WLAN | WLAN Monitoring |
| Get Throughput Trend (WLAN) | Read throughput trend for a WLAN network-wide | WLAN Monitoring |
| Get Throughput Trend (AP-scoped) | Read throughput trend for a WLAN as seen by one access point | WLAN Monitoring |

## Verification checklist

- [ ] Confirmed with the caller that a read/audit outcome (not a provisioning outcome) is actually
      what's needed before using this skill — if provisioning was the actual ask, say so explicitly
      rather than silently only doing the read half
- [ ] Pagination (`next` cursor) was followed to completion when a full inventory was needed, not just
      the first page
- [ ] A WLAN identifier from a List call was used correctly (the `id` field, e.g. `wlans/wlan1`) for
      any follow-up Get call
