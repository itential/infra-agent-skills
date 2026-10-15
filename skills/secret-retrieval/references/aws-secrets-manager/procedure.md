# AWS Secrets Manager — Secret Retrieval Procedure

Reads, writes, or rotates a secret value stored in AWS Secrets Manager. Assumes the caller already
has an AWS credential (access key/secret key/session token, or an assumed role) with the relevant
`secretsmanager:*` IAM permissions for the target secret; provisioning that credential or the IAM
policy granting access is out of scope here.

Source: AWS's own Secrets Manager API Reference (docs.aws.amazon.com/secretsmanager/latest/
apireference/), specifically the GetSecretValue, PutSecretValue, RotateSecret, and DescribeSecret
action pages, retrieved 2026-09-29.

## Operational procedure

### 1. Resolve the secret identifier

Every call below accepts either the secret's friendly name or its full ARN as `SecretId`. AWS's own
guidance is to prefer a complete ARN over a partial one where available, and a cross-account
retrieval requires an ARN (a plain name only resolves within the caller's own account) — don't
assume a bare name will work across an account boundary.

### 2. Read the current or a specific version of a secret's value

Call the get-value action with `SecretId` and, optionally, either `VersionId` (a specific version's
UUID-style identifier) or `VersionStage` (a staging label — see step 4 for what these labels mean).
Supplying neither returns the version currently labeled `AWSCURRENT`. If both are supplied, they
must refer to the same version — AWS treats a mismatch as invalid input rather than picking one.

The response carries the decrypted value in exactly one of `SecretString` (text) or `SecretBinary`
(base64-encoded binary) — never both — depending on how the secret was originally stored. AWS's own
documentation explicitly recommends client-side caching of retrieved values rather than calling
this repeatedly at high frequency, both for latency and cost reasons.

### 3. Read secret metadata without exposing its value

If the caller only needs metadata (rotation configuration, tags, last-changed timestamp, which
version currently holds which staging label) rather than the value itself, use the describe action
instead of the get-value action — AWS's own documentation is explicit that describe never returns
the encrypted value, which makes it the safer default whenever the value itself isn't actually
needed.

### 4. Create a new version with a new value

**Confirm with the operator before writing a new version to a secret already in active use** — this
immediately shifts the `AWSCURRENT` staging label (see below) unless told not to, which changes
what every consumer using the default "current" lookup receives on their next read.

Call the put-value action with `SecretId` and either `SecretString` or `SecretBinary` (never both).
AWS's own staging-label model governs which version callers see by default:
- `AWSCURRENT` — the version returned when no `VersionId`/`VersionStage` is specified; a put
  operation automatically moves this label to the new version unless `VersionStages` is explicitly
  set otherwise.
- `AWSPREVIOUS` — automatically set to whatever version `AWSCURRENT` was just moved away from,
  giving a documented one-step-back recovery point.
- `AWSPENDING` — used during rotation (see step 6) to mark a version being validated before it
  becomes current.

This operation is idempotent when a `ClientRequestToken` is supplied and reused with identical
secret data — a retried call with the same token and same data succeeds without creating a
duplicate version; the same token with *different* data fails, since an existing version's contents
can never be modified in place, only superseded by a new version. AWS's own guidance also warns
against calling this at a sustained rate faster than roughly once every ten minutes, since Secrets
Manager prunes old versions on a schedule that assumes that pace — calling faster risks
accumulating more versions than get pruned and running into the account's version-count quota.

### 5. Update a secret's non-value metadata (only where the value doesn't need to change)

A separate update action exists for changing description, KMS key, or other metadata without
necessarily touching the value — but if `SecretString`/`SecretBinary` is included in that same
call, it creates a new version exactly like put-value does. Prefer the dedicated put-value action
from step 4 when the goal is specifically a new value, to keep the intent of the call unambiguous.

### 6. Rotate a secret

**Confirm with the operator before starting a rotation on a secret with active consumers that
haven't been updated to expect a new value**, unless rotation is already a routine, expected
process for this secret.

Call the rotate action with `SecretId`. Rotation is asynchronous and Lambda-function-driven — AWS
either uses the rotation configuration already stored on the secret, or (if rotation parameters are
supplied in this same call) sets that configuration first and then immediately starts a rotation.
`RotateImmediately` (default `true`) controls whether rotation begins now or only validates the
configured rotation function without changing the live value (`false`); when changing an
already-scheduled rotation's timing without triggering an immediate rotation, AWS's own guidance is
to use a `cron()`-style `ScheduleExpression` rather than `rate()`, since a `rate()`-based prior
schedule can still fire unexpectedly during the transition.

A call's successful acceptance does not itself confirm rotation completed — check
`RotationEnabled`/`LastRotatedDate` via describe, or attempt a get-value call for the version
expected to become current, to confirm completion rather than assuming success from the rotate
call's response alone.

### 7. Handle documented errors

- **ResourceNotFoundException** — no secret found at that `SecretId`; verify the identifier (and,
  for cross-account access, that a full ARN rather than a bare name was used).
- **InvalidRequestException** — the secret is in a state that doesn't support the requested
  operation (e.g. scheduled for deletion, or managed by another AWS service that owns write
  access) — report the specific documented cause rather than retrying.
- **InvalidParameterException** — a parameter name or value is malformed; check against
  `endpoints.md`'s field constraints.
- **DecryptionFailure** / **EncryptionFailure** — the configured KMS key can't be used to
  decrypt/encrypt the secret; this is a KMS key state or permissions problem, not something to
  retry without addressing the key itself.
- **ResourceExistsException** (put-value) — a version conflict from the idempotency rule in step 4;
  a different `ClientRequestToken` and identical-vs-different-data behavior is the resolution path,
  not a blind retry.
- **LimitExceededException** — a Secrets Manager quota (e.g. version count) was hit; this is the
  documented failure mode of writing new versions faster than AWS's pruning schedule clears old
  ones (see step 4).

## Patterns

- **AWS Secrets Manager versions by staging label, not by sequential integer, unlike Vault KV v2 or
  Azure Key Vault.** "The current version" is whichever version currently carries the `AWSCURRENT`
  label, not "the highest version number" — always reason about state changes here in terms of
  which label moved where, not a version counter.
- **`SecretString` and `SecretBinary` are mutually exclusive on both read and write** — a given
  version was created as one or the other, never both, and the response reflects whichever it was.

## Known limitations

- Does not cover secret creation (`CreateSecret`) as a first-time provisioning step, replication to
  additional regions, or resource-policy management — this skill assumes the secret already exists
  and the caller already has the relevant IAM permissions.
- Does not cover AWS Certificate Manager or any other AWS credential-adjacent service — see
  `certificate-management` for certificate issuance.
- Rotation function authoring/deployment (the Lambda function AWS invokes to actually perform a
  rotation) is out of scope — this procedure covers triggering and confirming rotation, not writing
  the rotation logic itself.

## Tools

Every operation maps to the AWS Secrets Manager API (2017-10-17) — see `endpoints.md` for literal
request/response shape.

| Operation | Description | Category |
|---|---|---|
| `GetSecretValue` | Read a secret's current or a specific version's decrypted value | Secret Read |
| `DescribeSecret` | Read a secret's metadata without exposing its value | Secret Read |
| `PutSecretValue` | Create a new version with a new value | Secret Write |
| `UpdateSecret` | Update metadata, optionally also creating a new version if a value is included | Secret Write |
| `RotateSecret` | Start (or configure and start) asynchronous rotation | Secret Rotate |
| `CancelRotateSecret` | Turn off automatic rotation / cancel an in-progress rotation | Secret Rotate |

## Verification checklist

- [ ] A full ARN was used for any cross-account access; a bare name was confirmed sufficient only
      for same-account access
- [ ] Whether the caller needed the value itself, versus just metadata, was checked before choosing
      `GetSecretValue` over the value-free `DescribeSecret`
- [ ] Any new version write or rotation trigger was confirmed with the operator first
- [ ] A `ClientRequestToken` was used on `PutSecretValue` where retry-safety mattered
- [ ] Rotation completion was confirmed via `DescribeSecret`/a follow-up read, not assumed from the
      `RotateSecret` call's own response
- [ ] The retrieved secret value was not written into any log, report, or status message
