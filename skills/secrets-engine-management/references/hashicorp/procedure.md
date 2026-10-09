# Vault secrets-engine lifecycle

Inspect or change a secrets-engine mount in a specified Vault namespace.

Sources: current HashiCorp [mounts API](https://developer.hashicorp.com/vault/api-docs/system/mounts), [authentication-method API](https://developer.hashicorp.com/vault/api-docs/system/auth), and [HTTP API](https://developer.hashicorp.com/vault/api-docs), retrieved 2026-10-09. Literal bindings and errors are in [endpoints.md](endpoints.md).

## Common Sequences

- Inspect: Read mounts → Read configuration; optional Read auth methods.
- Configure: Read mounts → Enable or tune → Read configuration.
- Remove: Read mounts → Disable → Read mounts.

## Read mounts

The mount listing identifies each engine's path, type, options and configuration. A zero lease setting in this response means inheritance from system settings, not a zero-second effective lifetime. The supplied namespace must be the intended one; a missing or inaccessible namespace is not an empty inventory.

## Read configuration

The individual mount lookup returns its configuration; the tuning lookup reports effective lease durations in seconds. The returned path/type/options establish the selected engine. For any read, invalid input is corrected, forbidden access requires credential/policy review, and a not-found response does not distinguish an absent resource from a hidden one. Unsupported methods require the documented binding; a sealed/uninitialized or unavailable server blocks the operation.

## Enable or tune

Before enabling a mount or altering live engine settings, **stop and confirm with the operator before proceeding**. Enabling specifies the path and engine type; KV version 2 requires its explicit version option. Tuning supplies only the requested supported settings. A success response may be empty or include warnings; Read configuration verifies the result. A mutation error or timeout leaves the outcome unverified until the mount is read again. Plugin-version tuning does not load that version until a separate reload; this procedure does not claim it did.

## Disable

Disabling revokes secrets associated with the mount. **Stop and confirm with the operator before proceeding**, including credential revocation and loss of access to engine data. Success is the documented successful response and absence from the subsequent mount inventory. Revocation failures can prevent disabling; the vendor's normal recovery is to resolve the underlying cause, including a timeout if reported. Forced revocation may leave external credentials active and is outside this procedure.

## Read auth methods

The authentication-method inventory returns configured auth mounts and their metadata. It does not authenticate a user or modify an auth method.

## Patterns

Mount listing values and tuning values differ in their treatment of inherited TTLs. A mutation returning no body is not a parsing failure.

## Known limitations

Enterprise-only settings require the corresponding edition. Authentication, secret contents, and engine-specific configuration beyond mount options are not changed here. The complete common HTTP error vocabulary is recorded in the binding; errors are preserved rather than normalized to an empty list.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read mounts/configuration | Identifies engines and effective tuning | Read |
| Enable/tune | Creates a mount or changes its settings | Write |
| Disable | Removes an engine and revokes its secrets | Destructive |
| Read auth methods | Lists configured authentication mounts | Read |

## Verification checklist

- Namespace, mount path and engine type match the requested scope.
- Read-back agrees with requested settings and warnings remain visible.
- A disable failure is not reported as completed removal.
