# Endpoint Wiring — AWS Certificate Manager (ACM)

Literal API actions behind each capability named in `aws-acm-procedure.md`. ACM is a JSON-RPC-style
AWS API (actions named via the `X-Amz-Target` header against a single POST endpoint per region, e.g.
`acm.<region>.amazonaws.com`), invoked in practice through an AWS SDK or the AWS CLI rather than a
literal HTTP method/path pair — action names below are the SDK/CLI-facing operation names. Citation:
AWS Certificate Manager API Reference, retrieved 2026-09-17
(https://docs.aws.amazon.com/acm/latest/APIReference/).

## RequestCertificate (issue)

Request fields: `DomainName` (required — FQDN, wildcard via leading `*.`; note the underlying X.509
Common Name field is limited to 64 characters even though a Subject Alternative Name entry can be up
to 253), `SubjectAlternativeNames` (array of additional FQDNs, up to 100, though the default account
quota allows 10 before a quota increase is needed), `ValidationMethod` (`DNS` | `EMAIL` | `HTTP` —
`DNS` is AWS's stated recommendation), `CertificateAuthorityArn` (supplying this requests a private
certificate from that AWS Private CA; omitting it requests a public certificate), `KeyAlgorithm`
(request-time values documented as `RSA_2048` (default), `EC_prime256v1`, `EC_secp384r1` — the
broader `CertificateDetail.KeyAlgorithm` enum, `RSA_1024/2048/3072/4096` and
`EC_prime256v1/secp384r1/secp521r1`, is documented separately and appears to be a superset relevant
to certificates from other origins, e.g. imports), `IdempotencyToken` (dedupes repeated calls within
roughly a one-hour window), `Tags`, `DomainValidationOptions` (used to steer email validation to a
specific validation domain per requested name).

Response: `CertificateArn` only.

Documented errors: `InvalidArnException`, `InvalidDomainValidationOptionsException`,
`InvalidParameterException`, `InvalidTagException`, `LimitExceededException`, `TagPolicyException`,
`TooManyTagsException`.

## DescribeCertificate (read metadata)

Request: `CertificateArn`.

Response: a `CertificateDetail` object. Fields of note: `Status`, `Type`, `CertificateKeyPairOrigin`,
`RenewalEligibility`, `RenewalSummary`, `FailureReason`, `RevocationReason`, `RevokedAt`, `InUseBy`
(array of ARNs of resources referencing this certificate), `DomainValidationOptions` (per-domain
validation state, including a `ResourceRecord` object with `Name`/`Type`/`Value` for the DNS record
to create under DNS validation), `KeyAlgorithm`, `NotBefore`, `NotAfter`, `Serial`,
`SignatureAlgorithm`, `Subject`, `SubjectAlternativeNames`.

- `Status` values: `PENDING_VALIDATION`, `ISSUED`, `INACTIVE`, `EXPIRED`, `VALIDATION_TIMED_OUT`,
  `REVOKED`, `FAILED`. Validation is attempted for up to 72 hours before a request moves to
  `VALIDATION_TIMED_OUT`.
- `Type` values: `IMPORTED`, `AMAZON_ISSUED`, `PRIVATE`.
- `CertificateKeyPairOrigin` values: `AWS_MANAGED`, `ACME`, `CUSTOMER_PROVIDED`.
- `RenewalEligibility` values: `ELIGIBLE`, `INELIGIBLE` — per AWS's own documentation this field
  specifically reflects eligibility for the explicit `RenewCertificate` action ("only exported private
  certificates can be renewed with the RenewCertificate command"), which is a narrower concept than
  the broader automatic managed-renewal eligibility described in `aws-acm-procedure.md`.
- `FailureReason` values (present only when `Status=FAILED`): `NO_AVAILABLE_CONTACTS`,
  `ADDITIONAL_VERIFICATION_REQUIRED`, `DOMAIN_NOT_ALLOWED`, `INVALID_PUBLIC_DOMAIN`,
  `DOMAIN_VALIDATION_DENIED`, `CAA_ERROR`, `PCA_LIMIT_EXCEEDED`, `PCA_INVALID_ARN`,
  `PCA_INVALID_STATE`, `PCA_REQUEST_FAILED`, `PCA_NAME_CONSTRAINTS_VALIDATION`,
  `PCA_RESOURCE_NOT_FOUND`, `PCA_INVALID_ARGS`, `PCA_INVALID_DURATION`, `PCA_ACCESS_DENIED`,
  `SLR_NOT_FOUND`, `OTHER`.
- `RevocationReason` values (present only when `Status=REVOKED`): `UNSPECIFIED`, `KEY_COMPROMISE`,
  `CA_COMPROMISE`, `AFFILIATION_CHANGED`, `SUPERCEDED`, `SUPERSEDED`, `CESSATION_OF_OPERATION`,
  `CERTIFICATE_HOLD`, `REMOVE_FROM_CRL`, `PRIVILEGE_WITHDRAWN`, `A_A_COMPROMISE` (both `SUPERCEDED`
  and `SUPERSEDED` are listed in AWS's own reference — see `aws-acm-procedure.md`'s Known limitations
  for why this is flagged as a likely source-documentation duplicate rather than silently resolved).

Documented errors: `InvalidArnException`, `ResourceNotFoundException`, `ValidationException`.

## GetCertificate (read certificate body)

Request: `CertificateArn`.

Response: `Certificate` (PEM string) and `CertificateChain` (PEM string, concatenated chain).

Documented errors: `InvalidArnException`, `RequestInProgressException` (certificate not yet issued),
`ResourceNotFoundException`, `ValidationException`.

## RenewCertificate (explicit renewal)

Request: `CertificateArn`. Response: empty body on success (`200 OK`).

Documented errors: `InvalidArnException`, `RequestInProgressException` (still pending issuance —
cannot renew something not yet issued), `ResourceNotFoundException`, `ValidationException`. Renewing
an AWS Private CA-issued certificate through ACM additionally requires the ACM service principal to
have been granted permission on that CA beforehand.

## ImportCertificate

Request fields: `Certificate` (required, PEM, base64-encoded blob per the transport encoding used),
`PrivateKey` (required, PEM, unencrypted, documented maximum 5 KB), `CertificateChain` (optional,
PEM), `CertificateArn` (optional — supply to re-import/replace an existing imported certificate;
omit to import a new one), `Tags` (cannot be supplied on a re-import).

Additional documented constraints: the certificate's validity window (`NotBefore`/`NotAfter`) must
include the current time; the certificate's `Issuer` field must be non-empty; an OCSP authority URL
in the certificate, if present, must not exceed 1000 characters; the certificate's key algorithm
family must match its signing CA's key algorithm family.

Response: `CertificateArn`.

Documented errors: `ConflictException`, `InvalidArnException`, `InvalidParameterException`,
`InvalidTagException`, `LimitExceededException`, `ResourceNotFoundException`, `TagPolicyException`,
`TooManyTagsException`, `ValidationException`.

## DeleteCertificate

Request: `CertificateArn`. Response: empty body on success (`200 OK`); deletion is documented as
eventually consistent (a brief propagation delay before the certificate stops appearing in list/read
calls).

Documented errors: `AccessDeniedException`, `ConflictException`, `InvalidArnException`,
`ResourceInUseException` (certificate currently referenced by another AWS service — must be detached
first), `ResourceNotFoundException`, `ThrottlingException`, `ValidationException`. A certificate with
`CertificateKeyPairOrigin=ACME` cannot be deleted via this action at all — AWS documents that it
removes those automatically roughly a year after expiration instead.
