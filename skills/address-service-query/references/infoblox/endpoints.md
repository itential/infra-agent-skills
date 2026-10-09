# Infoblox NIOS collection-read bindings

Primary publisher: [Infoblox NIOS Go client](https://github.com/infobloxopen/infoblox-nios-go-client/tree/33d2162f331b7da85ded97c2eb1927d1cdee42b1), verified 2026-10-09 at commit `33d2162f331b7da85ded97c2eb1927d1cdee42b1`. The [README](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/README.md) documents Basic authentication, TLS configuration and its client/protocol matrix. Literal bindings come from generated list methods, not a third-party WAPI mirror.

The selected base is `https://<grid-host>/wapi/v<verified-version>`. Generated APIs cited here identify 2.13.6; the README maps client 0.0.1–0.1.2 to 2.13.6 and 0.2.0–0.2.1 to 2.14. Installed version compatibility is a prerequisite, not an inferred upgrade. HTTP Basic credentials use `Authorization: Basic <encoded-credentials>` through the authenticated client; response format is `Accept: application/json`.

SDK users enable TLS verification through `NIOS_SSL_VERIFY=true` or `option.WithSslVerify(true)` and, when needed, the documented trusted CA option. The SDK's default is false. This binding does not copy that default, enable debug credential logging, or substitute plaintext HTTP from generated localhost examples.

## Supported operations

Each collection uses `GET` with `_max_results=<operator-selected-positive-bound>` and `_return_as_object=1`. The result bound is supplied by the caller; no undocumented server maximum/default is asserted. No filter serialization, reference reconstruction or pagination algorithm is inferred from neighboring operations.

| Operation | Literal route | Primary list implementation |
|---|---|---|
| Read A records | `GET /record:a` | [A](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/dns/api_record_a.go) |
| Read AAAA records | `GET /record:aaaa` | [AAAA](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/dns/api_record_aaaa.go) |
| Read CNAME records | `GET /record:cname` | [CNAME](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/dns/api_record_cname.go) |
| Read PTR records | `GET /record:ptr` | [PTR](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/dns/api_record_ptr.go) |
| Read TXT records | `GET /record:txt` | [TXT](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/dns/api_record_txt.go) |
| Read network collection | `GET /network` | [Network](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/ipam/api_network.go) |
| Read range collection | `GET /range` | [Range](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/dhcp/api_range.go) |
| Read fixed-address collection | `GET /fixedaddress` | [Fixed address](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/dhcp/api_fixedaddress.go) |

The client binds `_return_fields` or `_return_fields+` to a comma-separated field selection when explicitly supplied; omitted fields are not treated as null or false. The object-form response contains `result`; generated models can retain additional properties. These models do not define a guaranteed next-page/end-of-list contract. This procedure intentionally reports a bounded response instead of asserting full traversal.

DNS record models expose `_ref` and type-specific values such as `name`, `ipv4addr`, `ipv6addr`, `canonical`, `ptrdname`, `text`, `view`, and TTL/use flags where present. These are read values, not a claimed universal create schema. Network, range and fixed-address fields remain their own model data. [Range properties](https://github.com/infobloxopen/infoblox-nios-go-client/blob/33d2162f331b7da85ded97c2eb1927d1cdee42b1/dhcp/docs/Range.md) label `dhcp_utilization` as a percentage multiplied by 1000 but also describe available-versus-total addresses; the ambiguous population is not turned into a derived exhaustion threshold. The native utilization status and returned counts remain separate evidence.

## Failure contract

The generated list methods return a generic error for HTTP status 300 or higher, transport failure, body-read failure or failed decoding. The returned HTTP status and sanitized body identify the observed failure; the SDK source does not establish a complete per-operation error-code table or rate ceiling. Authentication/authorization failures stop for client correction, and HTTP 429 honors an available `Retry-After`. No retry or missing-data conclusion is based solely on a default zero-valued generated model.
