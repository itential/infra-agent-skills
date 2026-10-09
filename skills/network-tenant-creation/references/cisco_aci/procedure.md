# APIC empty tenant creation

Create an explicitly named empty tenant in the APIC policy model.

Source: Cisco [APIC REST API Configuration Guide](https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/all/apic-rest-api-configuration-guide/cisco-apic-rest-api-configuration-guide/m_using_the_rest_api.html), managed-object naming, create/update behavior, MIM validation and tenant examples, retrieved 2026-10-09. Exact XML/HTTP bindings are in [endpoints.md](endpoints.md).

1. **Validate the intended model object.** The deployed Management Information Model establishes the tenant class, parent, naming fields and creation privilege. The requested tenant name supplies the object's identity. Missing or invalid naming/privilege information prevents a valid request; no organization-specific naming convention is invented.
2. **Read that tenant identity.** The named-object read establishes whether the intended tenant already exists. An existing object is reported as existing; this create-only procedure does not silently modify it. An authentication, authorization or transport error is not evidence of absence. Native APIC creation and update use the same operation, which is why this distinction matters.
3. **Create the empty tenant.** This changes the live policy model: stop and confirm with the operator before proceeding. The documented minimal tenant payload supplies only its name and requests the changed object in the response. Success is a returned tenant object with the intended identity, without an APIC error. Omitted properties follow the deployed model's defaults or remain blank. A schema violation remains rejected; the request must be corrected against the model rather than adding guessed fields.
4. **Read the tenant object.** The named-object read returns its distinguished name and name. Success means those identify the requested tenant. A timeout during creation leaves the outcome unknown; the read establishes whether the tenant is present before any newly confirmed repeat. This check establishes model persistence only.

## Patterns

- The API's single create/update operation can update an existing object; an existing identity is not treated as a new tenant.
- An empty tenant is a policy container, not a completed VRF/BD/EPG deployment.

## Known limitations

- Concurrent creation is possible between the initial read and write; the source does not document a create-only precondition for this request.
- Child policy objects, endpoint attachment, data-plane tests, deletion and rollback are excluded.
- The source does not prescribe a universal read-after-write delay or mutation retry count.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read tenant object | Retrieve the exact tenant identity | Read |
| Create tenant object | Submit the documented minimal empty-tenant representation | Change |

## Verification checklist

- Model class, parent, naming information and privileges were checked.
- An existing tenant was not silently modified by a create request.
- The mutation gate preceded creation.
- Both returned and read-back identities match the requested tenant.
