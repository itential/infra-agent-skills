# Record Fields — Azure DNS Record Set Types

Field names and types are quoted from the Azure DNS REST API reference (api-version 2018-05-01),
`RecordSet.properties`. The Azure Portal's "Add a record set" panel renders these same fields under
UI labels the source docs only show for the A-record example (Name, Type, TTL, TTL unit, IP address);
other types' Portal field labels are inferred to correspond 1:1 to the field names below — this
mapping was not independently confirmed for every type.

Common to every record set, regardless of type:
- `properties.TTL` (integer, int64, required) — time-to-live in seconds. Portal: **TTL** + **TTL
  unit** (Seconds/Minutes/Hours/Days — combine into a single seconds value for the REST call).
  Not settable on the zone-apex SOA record set's own TTL (see SKILL.md § zone-apex rules).
- `properties.metadata` (object, optional) — free-form key/value tags on the record set.
- `properties.targetResource` (SubResource `{ "id": "<resourceId>" }`, optional) — alias-record
  target; mutually exclusive with the type's own record data. Out of scope for this skill (see
  SKILL.md scope note) — do not populate.

## A — `properties.ARecords` (array)
- `ipv4Address` (string, required) — "The IPv4 address of this A record."

## AAAA — `properties.AAAARecords` (array)
- `ipv6Address` (string, required) — "The IPv6 address of this AAAA record."

## CNAME — `properties.CNAMERecord` (single object, NOT an array — max one record per set)
- `cname` (string, required) — "The canonical name for this CNAME record."

## MX — `properties.MXRecords` (array)
- `preference` (integer, int32, required) — "The preference value for this MX record." Lower values
  are preferred by mail transfer agents (standard MX semantics; not restated on the reference page
  itself beyond the field description).
- `exchange` (string, required) — "The domain name of the mail host for this MX record."

## NS — `properties.NSRecords` (array)
- `nsdname` (string, required) — "The name server name for this NS record."
- See SKILL.md § zone-apex rules for the restriction on the auto-created NS record set at name `@`.

## PTR — `properties.PTRRecords` (array)
- `ptrdname` (string, required) — "The PTR target domain name for this PTR record."
- Created in a reverse-lookup zone (e.g. `0.0.127.in-addr.arpa`); `relativeRecordSetName` is the
  reversed IP octet (e.g. `1`), not a hostname.

## SOA — `properties.SOARecord` (single object; update-only, see SKILL.md)
- `host` (string) — "The domain name of the authoritative name server for this SOA record." Not
  editable via the Portal per the primary doc.
- `email` (string) — "The email contact for this SOA record."
- `serialNumber` (integer, int64)
- `refreshTime` (integer, int64)
- `retryTime` (integer, int64)
- `expireTime` (integer, int64)
- `minimumTTL` (integer, int64) — "By convention this is used to determine the negative caching
  duration."

## SRV — `properties.SRVRecords` (array)
- `priority` (integer, int32, required)
- `weight` (integer, int32, required)
- `port` (integer, int32, required)
- `target` (string, required) — "The target domain name for this SRV record."

## TXT — `properties.TXTRecords` (array)
- `value` (string[], required) — "The text value of this TXT record." Note this is itself an array of
  strings per TXT entry (a record can carry multiple concatenated string segments).

## CAA — `properties.caaRecords` (array; note lowercase `caaRecords` in the schema, unlike other
types' PascalCase `properties.<TYPE>Records` — verbatim from the source, not a typo introduced here)
- `flags` (integer, int32, required) — "The flags for this CAA record as an integer between 0 and
  255."
- `tag` (string, required) — "The tag for this CAA record." (e.g. `issue`, `issuewild`, `iodef` — the
  reference page's own example uses `issue`; the full tag vocabulary is not enumerated on this page)
- `value` (string, required) — "The value for this CAA record." (e.g. a CA domain name for `issue`)

## Out of scope for this skill (see SKILL.md)
DS, NAPTR, TLSA record types (present as CLI command groups marked "Experimental," not in the
2018-05-01 REST `RecordType` enum retrieved) and alias record sets (`targetResource`).
