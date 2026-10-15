# Endpoint Wiring — AWS Route 53 DNS Zone Management

Literal API calls behind each capability named in `procedure.md`. All calls are AWS Route 53 REST API,
version `2013-04-01`, XML request/response bodies, signed with SigV4 (whatever the caller's Route 53
client/SDK already handles). Source: AWS Route 53 API Reference, docs.aws.amazon.com, retrieved
2026-09-17.

## Create a Hosted Zone

Tool hint: `CreateHostedZone`.

Literal route: `POST /2013-04-01/hostedzone`

Body fields:

| Field | Required | Notes |
|---|---|---|
| `CallerReference` | yes | Caller-generated unique string, 1–128 chars. Reusing the same value on a retried request is how Route 53 treats it as idempotent rather than a duplicate create. |
| `Name` | yes | FQDN, max 1024 chars. Trailing dot optional — treated identically with or without it. Cannot be a bare TLD. |
| `HostedZoneConfig.Comment` | no | Free-text. |
| `HostedZoneConfig.PrivateZone` | no | Boolean; omit `HostedZoneConfig` entirely if neither field is needed. |
| `DelegationSetId` | no | Max 32 chars; associates a reusable delegation set instead of assigning fresh name servers. |
| `VPC.VPCId` / `VPC.VPCRegion` | required together, private zones only | Exactly one VPC at creation time. |

Response (201, header `Location` = new zone's URL): `HostedZone` (`Id`, `Name`, `CallerReference`,
`Config`, `ResourceRecordSetCount`, `Features`, `LinkedService`), `ChangeInfo` (`Id`, `Status` starts
`PENDING`, `SubmittedAt`, `Comment`), `DelegationSet` (`Id` if reusable, `CallerReference`,
`NameServers[]`), and `VPC` (private zones only).

Errors:
- `ConflictingDomainExists` (400)
- `DelegationSetNotAvailable` (400)
- `DelegationSetNotReusable` (400)
- `HostedZoneAlreadyExists` (409) — same `CallerReference` reused.
- `InvalidDomainName` (400)
- `InvalidInput` (400)
- `InvalidVPCId` (400)
- `NoSuchDelegationSet` (400)
- `TooManyHostedZones` (400)

Note: creating a hosted zone for a private zone requires the caller's credentials to carry
`ec2:DescribeVpcs`.

## Read a Hosted Zone

Tool hint: `GetHostedZone`.

Literal route: `GET /2013-04-01/hostedzone/{Id}`

`Id` is the hosted zone identifier (as returned by create, or by a zone-lookup call — strip any
`/hostedzone/` prefix before using it here if it came from a list/lookup response).

Response (200): `HostedZone` (same shape as create), `DelegationSet.NameServers[]` (the 4 assigned
name servers — plus `Id`/`CallerReference` if the zone uses a reusable delegation set), and `VPCs[]`
(private zones only, minimum 1 entry when present).

Errors:
- `InvalidInput` (400)
- `NoSuchHostedZone` (404)

## Update a Hosted Zone's Comment

Tool hint: `UpdateHostedZoneComment`.

Literal route: `POST /2013-04-01/hostedzone/{Id}`

Body: `Comment` (optional string, max 256 chars). Omitting it clears any existing comment rather than
leaving the prior value in place.

Response (200): updated `HostedZone`.

Errors:
- `InvalidInput` (400)
- `NoSuchHostedZone` (404)
- `PriorRequestNotComplete` (400)

## Delete a Hosted Zone

Tool hint: `DeleteHostedZone`.

Literal route: `DELETE /2013-04-01/hostedzone/{Id}`

No request body. The zone must contain only its default SOA and NS records and have DNSSEC signing
disabled, or the call is rejected.

Response (200): `ChangeInfo` (`Id`, `Status` starts `PENDING`, `SubmittedAt`, `Comment`).

Errors:
- `HostedZoneNotEmpty` (400) — the zone has records beyond the default SOA/NS, or DNSSEC is still
  enabled.
- `InvalidDomainName` (400)
- `InvalidInput` (400)
- `NoSuchHostedZone` (404)
- `PriorRequestNotComplete` (400)

## Check Propagation Status of a Zone Create/Delete

Tool hint: `GetChange` — same call `dns-record-management`'s Route 53 procedure uses for record
changes.

Literal route: `GET /2013-04-01/change/{Id}`

`Id` = the `ChangeInfo.Id` returned by create or delete above.

Response (200): `ChangeInfo` (`Id`, `Status` — `PENDING` | `INSYNC`, `SubmittedAt`, `Comment`).

Errors:
- `InvalidInput` (400)
- `NoSuchChange` (404)

## Resolve/enumerate zones (for subdomain delegation and general lookup)

Tool hint: `ListHostedZonesByName` (nearest-match by name) or `ListHostedZones` (full enumeration,
client-side name matching) — same calls and caveats as `dns-record-management`'s Route 53
`endpoints.md` documents; see that file for the literal route and response shape. Reused here
unchanged since zone lookup-by-name is identical wire-level behavior whether the caller's goal is a
record change or a zone-level operation.

## Field reference (zone-level fields only)

| Field | Location | Notes |
|---|---|---|
| `CallerReference` | Create request | Idempotency token; unique per creation attempt. |
| `Name` | Create request / response | FQDN; max 1024 chars on input. |
| `HostedZoneConfig.Comment` | Create request, Update request | Free text, max 256 chars on update. |
| `HostedZoneConfig.PrivateZone` | Create request | Boolean; immutable after creation. |
| `DelegationSetId` | Create request | Reusable delegation set to associate, if any. |
| `VPC.VPCId` / `VPC.VPCRegion` | Create request, private zones | Exactly one at creation. |
| `HostedZone.Id` | Response | Format `/hostedzone/{ID}` — strip the prefix before reusing elsewhere. |
| `HostedZone.ResourceRecordSetCount` | Response | Total records currently in the zone, including the default SOA/NS pair. |
| `DelegationSet.NameServers[]` | Response | The zone's 4 assigned authoritative name servers. |
| `ChangeInfo.Status` | Response | `PENDING` → `INSYNC`. |
