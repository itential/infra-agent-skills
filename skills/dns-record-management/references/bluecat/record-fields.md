# Record Field Reference — BlueCat Horizon / DDI Orchestrator dnsRecord Object

Full field list for the `dnsRecord` object accepted by DNS record creation, drawn from the Micetro
`mm_dnsrecord` Ansible module reference (documented against the same underlying object the REST API
uses) plus the Horizon UI guide's TTL notation.

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Record name; partial or fully qualified. |
| `type` (`rrtype` in the Ansible module) | Yes | One of the supported record types. Defaults to `A` if omitted where the tool allows a default. Immutable after creation — see below. |
| `data` | Yes | Record value. Space-separated list of sub-fields for `MX`, `SRV`, `NAPTR`, `CAA`, `CERT`, `HINFO`, `TLSA` (exact token order per sub-field is not stated in the sources retrieved — confirm against the target instance before scripting these types). Single value for simple types (`A`/`AAAA` address, `CNAME` target, `TXT` string, `NS` target, `PTR` target). |
| `dnszone` | Yes | The zone the record is created in. |
| `ttl` | No | Seconds, or shorthand `1s` / `1m` / `1h` / `1d` / `1w`. |
| `comment` | No | Static zones only — dynamic-zone records cannot carry a comment. |
| `enabled` | No | Boolean; record is enabled by default. |
| `aging` | No | AD-integrated dynamic zones only. Hours since 1601-01-01 00:00 UTC. A non-zero value marks the record dynamic (inferred from a secondary source, not a directly fetched primary page — not independently confirmed). |

## Supported record types (35 total, per the Horizon "DNS resource records" page)

`A`/`AAAA`, `AFSDB`, `CAA`, `CDS`, `CDNSKEY`, `CERT`, `CNAME`, `CSYNC`, `DNAME`, `DS`, `HINFO`, `HTTPS`,
`LOC`, `MX`, `NAPTR`, `NS`, `PTR`, `RP`, `SOA`, `SPF`, `SRV`, `SSHFP`, `SVCB`, `TLSA`, `TXT`, `URI`, `WKS`

**Read-only — cannot be created directly:** `ALIAS`, `DLV`, `DNSKEY`, `NSEC`, `NSEC3`, `NSEC3PARAM`,
`RRSIG`. If asked to create one of these, stop and report that the type is read-only per BlueCat's
documentation rather than attempting the call.

## A/AAAA free-IP autocomplete (UI-only behavior)

The Horizon UI offers an autocomplete that, given digits of a network address, finds a free IP and
populates `data` with it, showing the address's state: `Free`, `Reserved`, `Claimed`, or `Assigned`.
This is a UI convenience, not a REST field — when creating A/AAAA records via API, `data` must be
supplied directly as a resolved IP address; there is no documented API-level "find me a free IP" call
in the sources retrieved. If the caller needs an unassigned address, that is a separate IPAM lookup
outside this skill's scope.

## Type immutability

Once a record is created, `type` cannot be changed. The documented remedy is delete-and-recreate, not
an update call — see the verbatim warning in `references/endpoints.md`.
