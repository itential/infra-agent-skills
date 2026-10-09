---
name: secrets-engine-management
description: >-
  Discover, enable, tune, or disable a secrets engine. Use for HashiCorp Vault mount configuration and authentication-method discovery. Covers HashiCorp Vault. Assumes an authenticated Vault API client with the required system-path permissions and namespace.
---

# Secrets engine management

Discover, enable, tune, or disable a secrets engine.

## When to use this skill

Use for HashiCorp Vault mount configuration and authentication-method discovery.

## Universal concepts

No common wire protocol is implied by this capability. A secrets engine has an independent configuration and lifecycle; removing it can invalidate credentials.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

Authentication-method configuration and force-revocation recovery are outside scope.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes an authenticated Vault API client with the required system-path permissions and namespace. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
