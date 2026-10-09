# Vault internal-root and issuance-role configuration

Create an internal self-signed root in an existing PKI mount, then configure an explicitly supplied issuance role.

Sources: HashiCorp [PKI API](https://developer.hashicorp.com/vault/api-docs/secret/pki) and [HTTP API](https://developer.hashicorp.com/vault/api-docs), current multi-issuer API (Vault 1.11+), retrieved 2026-10-09. Bindings: [endpoints.md](endpoints.md).

## Common Sequences

- Inspect: Read issuers → Read roles.
- Create authority and role: Read issuers → Generate internal root → Read issuer → Configure role → Read roles.
- Change an existing role: Read issuer → Read roles → Configure role → Read roles.

## Read issuers

Issuer discovery returns identifiers and operator-assigned names. Reading the selected issuer returns its certificate, chain, key identifier and usage configuration. An exported-key warning is retained as a security finding. An unavailable or inaccessible issuer is not treated as permission to create a replacement.

## Generate internal root

The operator supplies the intended common name, validity, key parameters, and unique issuer name. **Stop and confirm with the operator before proceeding** because the action establishes a signing authority. Internal generation returns the certificate, serial number and issuer/key identifiers; its private key cannot subsequently be retrieved. In the multi-issuer API this does not overwrite another issuer. A creation timeout requires issuer discovery before another attempt, since repeating can create another authority.

## Read issuer

The exact generated or selected identifier is read back, establishing certificate/chain and issuer configuration. The procedure does not assume that a newly generated issuer became the default; the subsequent role uses the specific identifier.

## Read roles

Role discovery returns names. Reading a selected role returns its issuance constraints. A missing role is distinct from insufficient permissions; the native error remains visible. No organization-specific domain or lifetime policy is inferred from examples.

## Configure role

The operator-approved role definition includes its issuer reference and intended name, SAN, validity and key constraints. **Stop and confirm with the operator before proceeding** before creating or replacing the role. A full role write overwrites the definition and resets omitted options to defaults; a partial change uses the documented merge-patch binding. A successful response followed by Read roles must agree with the intended constraints. A rejected input is corrected before a new reviewed write; a timeout is resolved by read-back.

## Patterns

Domain and name permissions combine additively. A role reference by issuer name can change meaning after an issuer rename; an explicit issuer identifier records the intended association. Per-issuer issuance endpoints can override the role's issuer reference unless ACL policy prevents that access; role configuration alone is not an ACL restriction.

## Known limitations

A CA created here is not automatically trusted by devices. Root/private-key export and PKCS#12/JKS output are outside scope. Vault supports broad name/IP authorization options; this procedure does not choose them. Common authentication, malformed-input, not-found, unsupported-method, consistency, quota, and server errors are documented in the binding and leave the affected operation unverified.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read issuers/roles | Retrieves authority identity and issuance constraints | Read |
| Generate internal root | Creates a CA with a non-exported key | Authority write |
| Configure role | Creates, replaces, or patches an issuance policy | Policy write |

## Verification checklist

- Root creation returned the intended issuer and certificate.
- No private-key export was requested.
- Role read-back matches the approved issuer and constraints.
- Authority creation is not reported as trust-store deployment.
