# Panorama XML API bindings

Sources: [managed-firewall query](https://docs.paloaltonetworks.com/ngfw/api/pan-os-xml-api-use-cases/query-a-firewall-from-panorama-api), [request structure](https://docs.paloaltonetworks.com/ngfw/api/getting-started/structure-of-a-pan-os-xml-api-request), [errors](https://docs.paloaltonetworks.com/ngfw/api/getting-started/pan-os-xml-api-error-codes), retrieved 2026-10-09.

Existing authenticated HTTPS XML API client; endpoint `POST https://<panorama>/api/`, `Content-Type: application/x-www-form-urlencoded`. Form fields are URL-encoded, including XML. Authentication uses the configured API key, with documented parameter `key=<api-key>`; secret-bearing request data is not logged.

| Operation | Form fields |
|---|---|
| All managed devices | `type=op`, `cmd=<show><devices><all></all></devices></show>` |
| Connected devices | `type=op`, `cmd=<show><devices><connected></connected></devices></show>` |
| Targeted system information | `type=op`, `target=<returned-serial>`, `cmd=<show><system><info></info></system></show>` |

Success: XML `response` attribute `status="success"`; device results contain `result/devices` entries with `serial`; targeted output contains `result/system` with fields such as `hostname`, `serial`, `model`, `sw-version`, `uptime`. No XPath or action field is invented for these operational examples.

| API code | Meaning and response |
|---|---|
| 400 | Required/allowed parameter error; correct input |
| 403,16 | Authentication/access failure; restore permitted access |
| 1,17 | Unknown or invalid command/arguments; correct binding |
| 2–5,11,21 | Internal failure; vendor support |
| 6,12 | Invalid XPath/incomplete object; correct selection |
| 7,13 | Missing object; preserve not-found result |
| 8 | Nonunique selection; disambiguate |
| 10 | Referenced object cannot be deleted; wrong binding for this read-only procedure |
| 14,15 | Operation unavailable/denied in the current state; do not force it |
| 18 | Malformed XML; correct encoding/structure |
| 19–20 | Native successful command codes |
| 22 | Session timed out; restore valid session before another read |

The error-code page's prose for code 15 says allowed while its label/examples state denial. The label and examples govern this binding; no authorization bypass is inferred.
