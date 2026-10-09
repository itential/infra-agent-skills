# APIC empty-tenant bindings

Source: [Cisco APIC REST guide](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/all/apic-rest-api-configuration-guide/cisco-apic-rest-api-configuration-guide/m_using_the_rest_api.html), retrieved 2026-10-09.

Authenticated HTTPS session with `APIC-cookie=<token>` and any deployed challenge-token requirements handled by the client. The deployed MIM reference is `https://<apic>/doc/html/`.

| Operation | Binding | Payload / result |
|---|---|---|
| Read tenant | `GET https://<apic>/api/mo/uni/tn-<tenant-name>.xml?query-target=self` | `imdata` containing `fvTenant` with intended `dn` and `name`, or absence/error |
| Create tenant | `POST https://<apic>/api/mo/uni.xml?rsp-subtree=modified` | XML `<fvTenant name="<tenant-name>"/>`; successful modified-object response identifies that tenant |

`<tenant-name>` is a placeholder, not literal XML text; the client must XML-escape the actual name and encode the corresponding URI. The payload supplies no child policy. APIC uses the URL encoding suffix to select XML/JSON rather than inferring it from a header.

The publisher defines `fvTenant` DN as `uni/tn-[name]` and explicitly documents the minimal XML tenant creation payload. APIC rejects model/privilege violations with error information. No undocumented universal error-code table is added.
