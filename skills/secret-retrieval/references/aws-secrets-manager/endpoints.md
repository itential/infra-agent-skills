# Endpoint Wiring — AWS Secrets Manager Secret Retrieval

Literal API calls behind each capability named in `procedure.md`. All calls are the AWS Secrets
Manager API, version `2017-10-17`, JSON request/response bodies, signed with SigV4 (whatever the
caller's AWS SDK/client already handles) and dispatched to a single `POST /` endpoint per region
with the action named in the `X-Amz-Target` header.

Source: docs.aws.amazon.com/secretsmanager/latest/apireference/, retrieved 2026-09-29.

## Get a Secret's Value

`X-Amz-Target: secretsmanager.GetSecretValue`

Request:
```
{
  "SecretId": "<name or ARN>",
  "VersionId": "<optional, UUID-style, 32-64 chars>",
  "VersionStage": "<optional, e.g. AWSCURRENT, AWSPREVIOUS>"
}
```

Response (200):
```
{
  "ARN": "string",
  "Name": "string",
  "VersionId": "string",
  "CreatedDate": <timestamp>,
  "SecretString": "string",
  "SecretBinary": "<base64>",
  "VersionStages": ["string", ...]
}
```
Exactly one of `SecretString`/`SecretBinary` is present, never both.

Errors: `ResourceNotFoundException` (400), `InvalidParameterException` (400),
`InvalidRequestException` (400), `DecryptionFailure` (400), `InternalServiceError` (500).

## Read Secret Metadata (no value)

`X-Amz-Target: secretsmanager.DescribeSecret`

Request: `{ "SecretId": "<name or ARN>" }`

Response (200): includes `ARN`, `Name`, `Description`, `RotationEnabled`, `RotationLambdaARN`,
`RotationRules`, `LastRotatedDate`, `LastChangedDate`, `LastAccessedDate`, `NextRotationDate`,
`Tags`, `VersionIdsToStages` (a map of version id → array of staging labels currently attached).
Never includes `SecretString`/`SecretBinary`.

Errors: `ResourceNotFoundException` (400), `InvalidParameterException` (400), `InternalServiceError`
(500).

## Create a New Version (Put Value)

`X-Amz-Target: secretsmanager.PutSecretValue`

Request:
```
{
  "SecretId": "<name or ARN>",
  "SecretString": "<text value>",
  "SecretBinary": "<base64 binary value>",
  "ClientRequestToken": "<optional idempotency token, 32-64 chars>",
  "VersionStages": ["<optional array>"]
}
```
Exactly one of `SecretString`/`SecretBinary` required, never both. If `VersionStages` omitted,
`AWSCURRENT` moves automatically to the new version (and `AWSPREVIOUS` to the version it moved from).

Response (200): `{ "ARN": "string", "Name": "string", "VersionId": "string", "VersionStages":
["string", ...] }`

Errors: `ResourceNotFoundException` (400), `InvalidParameterException` (400),
`InvalidRequestException` (400), `LimitExceededException` (400), `ResourceExistsException` (400,
idempotency-token/data mismatch), `DecryptionFailure`/`EncryptionFailure` (400),
`InternalServiceError` (500).

## Update Secret Metadata (optionally also creating a new version)

`X-Amz-Target: secretsmanager.UpdateSecret`

Request: `SecretId` required; any of `Description`, `KmsKeyId`, `SecretString`, `SecretBinary`,
`ClientRequestToken` optional. Including `SecretString`/`SecretBinary` creates a new version exactly
as `PutSecretValue` does.

Response (200): `{ "ARN": "string", "Name": "string", "VersionId": "string" }`

## Rotate a Secret

`X-Amz-Target: secretsmanager.RotateSecret`

Request:
```
{
  "SecretId": "<name or ARN>",
  "ClientRequestToken": "<optional>",
  "RotationLambdaARN": "<optional; omit for managed rotation>",
  "RotationRules": { "AutomaticallyAfterDays": <int>, "Duration": "<e.g. 2h>",
                      "ScheduleExpression": "<cron() or rate() expression>" },
  "RotateImmediately": <boolean, default true>
}
```

Response (200): `{ "ARN": "string", "Name": "string", "VersionId": "string" }` — `VersionId` matches
`ClientRequestToken` if one was supplied.

Errors: `ResourceNotFoundException` (400), `InvalidParameterException` (400),
`InvalidRequestException` (400), `InternalServiceError` (500).

## Cancel Rotation

`X-Amz-Target: secretsmanager.CancelRotateSecret`

Request: `{ "SecretId": "<name or ARN>" }`

Turns off automatic rotation; if a rotation is in progress, cancels it — may leave `AWSPENDING`
attached to a partially-created version, which the caller may need to clean up via
`UpdateSecretVersionStage`.
