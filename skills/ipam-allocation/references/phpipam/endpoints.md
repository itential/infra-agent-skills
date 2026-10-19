# Endpoint Mapping — phpIPAM Subnet and IP Address Allocation

Literal phpIPAM REST operations behind each capability in `procedure.md`. Source: phpIPAM API
documentation, https://phpipam.net/api/api_documentation/, retrieved 2026-10-19.

Base path: `https://<phpipam-host>/api/<app-id>/` — every path below is relative to it. The app ID is
the name of the API app configured in the phpIPAM admin interface. The documentation says URL rewriting
must be enabled on the server for the API to work.

| Capability | Operation | Body / notes |
|---|---|---|
| Find subnet by CIDR | `GET subnets/cidr/{subnet}/` | `{subnet}` is the CIDR (e.g. `192.0.2.0/24`). The documentation also lists a `subnets/search/{subnet}/` form. 404 when nothing matches. |
| Create subnet | `POST subnets/` | JSON body: `subnet` (network address), `mask`, `sectionId` required. Optional: `description`, `vlanId`, `vrfId`, `masterSubnetId`, others. Returns code 201 with the new ID. |
| Get subnet usage | `GET subnets/{id}/usage/` | No body. |
| Read first free child subnet | `GET subnets/{id}/first_subnet/{mask}/` | `{id}` = parent subnet ID, `{mask}` = child mask length. Reserves nothing. |
| Create first free child subnet | `POST subnets/{id}/first_subnet/{mask}/` | Optional body: `description`. Creates the subnet. |
| Read first free address | `GET addresses/first_free/{subnetId}/` | No body. Reserves nothing. (A `subnets/{id}/first_free/` form also appears in a published API description; this procedure uses the addresses form shown in the documentation.) |
| Create address at first free IP | `POST addresses/first_free/{subnetId}/` | Optional body: address fields such as `hostname`, `description`. Creates the address. |
| Create address (chosen IP) | `POST addresses/` | JSON body: `ip`, `subnetId` required. Optional: `hostname`, `description`, `mac`, `owner`, `tag`, `deviceId`. |
| Look up address | `GET addresses/{ip}/{subnetId}/`, `GET addresses/search/{ip}/`, `GET addresses/search_hostname/{hostname}/` | By IP within a subnet, by IP across subnets, or by hostname. |

## Auth / headers

Send the API token in the `token` header (the documentation also accepts a `phpipam-token` header).
Two modes: a static app token (SSL required) used directly on every request, or a dynamic token
obtained by logging in with HTTP Basic credentials, valid for 6 hours by default and renewed on each
successful request. `Content-Type: application/json` on writes.

## Response envelope

`code` (numeric HTTP-style status), `success` (boolean), `message` (error detail), `data` (payload),
`time` (optional timing). Create calls return code 201 with a Location header; other successes return
200.

## Unverified

- Response and message text when a subnet has no free address or a parent has no free child slot of the
  requested mask: not stated in the documentation. (Assumption: reported as a non-success envelope.)
- Duplicate-subnet and duplicate-address create behavior: not stated.
- Rate limits: not stated.
- Exact usage-response field names: not stated.
