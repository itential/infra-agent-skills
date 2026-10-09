---
name: certificate-authority-configuration
description: >-
  Configure an issuing authority and its certificate issuance role. Use for HashiCorp Vault PKI internal-root creation, issuer discovery/read, and issuance-role create/read/list in an existing PKI mount. Covers HashiCorp Vault PKI. Assumes an authenticated Vault API client and an enabled PKI mount with an operator-approved CA identity, key policy, and issuance constraints.
---

# Certificate authority configuration

Configure an issuing authority and its certificate issuance role.

## When to use this skill

Use for HashiCorp Vault PKI internal-root creation, issuer discovery/read, and issuance-role create/read/list in an existing PKI mount.

## Universal concepts

No common wire protocol is implied by this capability. Authority creation and issuance-policy changes affect the trust and certificate scope of dependent systems.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Intermediate signing/import, key export, rotation, trust-store deployment, and choosing a certificate policy are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Vault API client and an enabled PKI mount with an operator-approved CA identity, key policy, and issuance constraints. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
