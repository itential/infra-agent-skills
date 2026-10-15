# Endpoint Wiring — AWS Route 53 DNS Record Management

Literal API calls behind each capability named in `SKILL.md`. All calls are AWS Route 53 REST API,
version `2013-04-01`, XML request/response bodies, signed with SigV4 (whatever the caller's Route 53
client/SDK already handles).

## Resolve a Domain Name to a Hosted Zone ID

Tool hint: `ListHostedZonesByName` (AWS SDK/CLI action name — this is the identifier to look for in
whatever tool registry the caller has for its Route 53 client/adapter).

Literal route: `GET /2013-04-01/hostedzonesbyname?dnsname={DNSName}&maxitems=1`

Pass the record's domain (or any parent of it) as `dnsname`. This does NOT return an exact-match-only
result — it seeks to the nearest zone alphabetically. **The caller must check the first `HostedZones[].Name`
in the response equals the requested domain (with Route 53's trailing dot, e.g. `example.com.`, and
matching the longest parent zone if the exact name isn't itself a zone) before using its `Id`.** If it
doesn't match, either page further (`NextDNSName`/`NextHostedZoneId`) or conclude no matching zone exists —
never fall back to guessing an ID.

Response: `HostedZones[].Id` (format `/hostedzone/{ID}` — strip the `/hostedzone/` prefix before using it
as `HostedZoneId` elsewhere), `HostedZones[].Name`, `IsTruncated`, `NextDNSName`, `NextHostedZoneId`.

Errors:
- `InvalidDomainName` (400) — the supplied domain name is not valid.
- `InvalidInput` (400) — malformed input.

Fallback if the above proves unreliable or the account has few zones — tool hint: `ListHostedZones`.
Literal route: `GET /2013-04-01/hostedzone` (no name filter) — match `HostedZones[].Name` client-side
across pages (`Marker`/`NextMarker`). Errors: `InvalidInput`, `NoSuchDelegationSet`,
`DelegationSetNotReusable` (all 400, not relevant unless `delegationsetid` is supplied, which this skill
does not use).

## Create, Update, or Delete a Basic DNS Record

Tool hint: `ChangeResourceRecordSets`.

Literal route: `POST /2013-04-01/hostedzone/{HostedZoneId}/rrset/`

Body (basic/standard resource record set syntax — the "Don't refer to the full Syntax section" note in
the source applies; this is the one example block that matters for plain DNS records):

```
<?xml version="1.0" encoding="UTF-8"?>
<ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2013-04-01/">
<ChangeBatch>
   <Comment>optional comment about the changes in this change batch request</Comment>
   <Changes>
      <Change>
         <Action>CREATE | DELETE | UPSERT</Action>
         <ResourceRecordSet>
            <Name>fully qualified domain name</Name>
            <Type>DNS record type</Type>
            <TTL>time to live in seconds</TTL>
            <ResourceRecords>
               <ResourceRecord>
                  <Value>applicable value for the record type</Value>
               </ResourceRecord>
               ...
            </ResourceRecords>
            <HealthCheckId>optional ID of a Route 53 health check</HealthCheckId>
         </ResourceRecordSet>
      </Change>
      ...
   </Changes>
</ChangeBatch>
</ChangeResourceRecordSetsRequest>
```

Response (200): `ChangeInfo` with `Id`, `Status` (`PENDING`), `SubmittedAt`, `Comment`.

Errors and exact strings:
- `InvalidChangeBatch` (400) — one or more validation errors in the change batch; includes duplicate
  delete of the same record set within one batch.
- `InvalidInput` (400) — malformed input.
- `NoSuchHealthCheck` (404) — `HealthCheckId` does not exist.
- `NoSuchHostedZone` (404) — `HostedZoneId` does not exist.
- `PriorRequestNotComplete` (400) — `Code: PriorRequestNotComplete`, `Message: The request was rejected
  because Route 53 was still processing a prior request.`
- `Throttling` (400) — `Code: Throttling`, `Message: Rate exceeded`.

## Check Propagation Status of a Change

Tool hint: `GetChange`.

Literal route: `GET /2013-04-01/change/{Id}`

`Id` = the `ChangeInfo.Id` returned by the create/update/delete call above (1–6500 chars).

Response (200): `ChangeInfo` with `Id`, `Status` (`PENDING` | `INSYNC`), `SubmittedAt`, `Comment`.

Errors:
- `InvalidInput` (400) — malformed `Id`.
- `NoSuchChange` (404) — no change exists with that ID.

## Field reference (basic record set only)

| Field | Location | Required | Notes |
|---|---|---|---|
| `HostedZoneId` | URI | yes | Max length 32. |
| `Action` | Change | yes | `CREATE`, `DELETE`, or `UPSERT`. |
| `Name` | ResourceRecordSet | yes | Fully qualified domain name. |
| `Type` | ResourceRecordSet | yes | e.g. A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, SRV, CAA. |
| `TTL` | ResourceRecordSet | yes | Seconds. |
| `ResourceRecords.ResourceRecord.Value` | ResourceRecordSet | yes, 1+ | Value appropriate to `Type`. |
| `HealthCheckId` | ResourceRecordSet | no | Optional Route 53 health check to associate. |
| `Comment` | ChangeBatch | no | Free-text description. |

Limits: 10,000 records per hosted zone, 400 records per record set, 1,000 `ResourceRecord` elements
per request, and 32,000 characters total across all `Value` elements per request (UPSERT counts
double against the latter two).
