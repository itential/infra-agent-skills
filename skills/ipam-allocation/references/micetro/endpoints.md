# Endpoint Mapping — Micetro IPAM Allocation

Literal Micetro REST operations behind `procedure.md`. Base URL pattern and authentication options come
from Micetro's documentation (docs.menandmice.com, 25.1, retrieved 2026-10-19). Paths, parameters and
bodies come from the generated OpenAPI definition v2.0 in the Itential `assets` repository — a secondary
source, so every row is *(unverified)* against a live server; the instance serves its own definition at
`/mmws/api/swagger.json`.

Base URL placeholder: `https://micetro.example.com/mmws/api/v2`

| Capability | Operation | Notes |
|---|---|---|
| List available address blocks | `GET /ranges/{rangeRef}/availableAddressBlocks` | Query: `mask`, `size`, `ignoreSubnetFlag`, `startAddress`, `temporaryClaimTime`; `limit` per the reference listing. |
| Create range | `POST /ranges` | Body: `range` (required), optional `discovery`, `saveComment`. |
| Get next free address | `GET /ranges/{rangeRef}/nextFreeAddress` | Query: `startAddress`, `ping`, `random`, `excludeDHCP`, `temporaryClaimTime`. |

## Auth / headers

Documented options: session-based or basic credentials, bearer token (a Micetro session ID created via
the sessions endpoint), Windows NTLM, Kerberos. `Authorization: Bearer <session id>` for the bearer form.
HTTPS strongly recommended per the definition.

## Error signals

Error strings are not documented in the sources used — unknown.
