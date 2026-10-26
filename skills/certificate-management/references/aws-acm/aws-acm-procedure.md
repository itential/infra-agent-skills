# AWS Certificate Manager (ACM) — Certificate Lifecycle Procedure

Requests, reads, renews, imports, and deletes TLS certificates in AWS Certificate Manager (ACM), for
use with AWS services that integrate with it (Elastic Load Balancing, CloudFront, API Gateway, and
others). Distinct from AWS Private CA's own direct issuance API — this procedure covers ACM's own
certificate-management surface (`RequestCertificate` and related actions), not a private CA issuing
certificates outside of ACM. Assumes an authenticated AWS API client (SDK, CLI, or direct
Signature-Version-4-signed calls) with IAM permissions for the ACM actions used is already available.
See `aws-acm-endpoints.md` for the literal action names and field tables behind every operation named
below. Citation: AWS Certificate Manager API Reference and User Guide, retrieved 2026-09-17
(https://docs.aws.amazon.com/acm/latest/APIReference/, https://docs.aws.amazon.com/acm/latest/
userguide/managed-renewal.html).

## Operational procedure

### Request (issue) a certificate

Submit a certificate request naming the primary fully-qualified domain name and, optionally,
additional domain names to cover as Subject Alternative Names, plus which key algorithm the key pair
should use (RSA is the default if unspecified). A wildcard name is expressed with a leading `*.`
segment. The call returns immediately with an identifier (ARN) for the new certificate — expect a
short propagation delay of a few seconds before that certificate's details can be successfully read
back.

**Public certificates require domain-ownership validation before issuance completes; private
certificates issued against a private CA ARN do not.** For a public certificate, choose a validation
method — DNS validation (publishing a specific DNS record ACM provides) is the documented
recommendation over email validation, since it can be automated and doesn't depend on a mailbox at
the domain being monitored. Until validation completes for every requested name, the certificate sits
in a pending-validation state; it is not usable until every name validates successfully.

A request can optionally supply an idempotency token so that repeated identical requests within about
an hour are treated as one request rather than issuing duplicate certificates — changing that token
between calls signals a genuinely new, separate request.

### Complete domain validation (public certificates)

For DNS validation, read back the certificate's per-domain validation records and create the DNS
record ACM specifies for each name being validated; ACM's own validation process then detects the
record and advances that name's validation state without further action from the caller. For email
validation, ACM sends validation email to a set of standard addresses at the domain (or a specified
validation domain) and a recipient must approve it — this procedure does not automate the email
path since it depends on a human recipient. Validation is attempted for a bounded window before the
request times out; a timed-out or failed request should be deleted and re-submitted after the
underlying DNS/email issue is corrected, rather than left pending indefinitely.

### Read a certificate's status and details

Fetch the certificate's full metadata by its identifier to check its current status, its domain
validation state per name, which AWS resources currently reference it, its key algorithm, its
validity window, and (for an ACM-issued certificate) its renewal-eligibility and renewal-status
information. A certificate's status reflects where it is in the request/validation/issuance
lifecycle, or, separately, whether it has since expired or been revoked — read the status value
itself rather than inferring state from the presence/absence of other fields.

To retrieve the actual certificate material (the PEM-encoded certificate and its chain) rather than
just metadata, fetch the certificate body separately from the metadata call above. This only succeeds
once the certificate has finished issuing — requesting the body of a certificate still pending
validation is expected to fail.

### Renew a certificate

ACM distinguishes two related but different things under "renewal":

1. **Automatic managed renewal**, which ACM performs on its own for certificates it issued, without
   an explicit renewal call, as their expiration approaches — but only for certificates ACM considers
   eligible. Eligibility generally requires the certificate to be either actively referenced by
   another AWS service or to have been exported since it was issued/last renewed; a certificate
   issued directly through AWS Private CA's own API (bypassing ACM's request flow), an imported
   certificate, or an already-expired certificate is not eligible for this automatic path. A
   certificate issued through ACM's own ACME-based issuance option is explicitly excluded from
   managed renewal as well — that path's renewal is the responsibility of whatever ACME client
   requested it, not ACM's managed-renewal mechanism. Unverified: the exact
   days-before-expiration trigger point for managed renewal — treat the timing
   as CA-managed and not precisely predictable rather than assuming a specific lead time.
2. **An explicit renewal call**, which is narrower still — as documented, it applies specifically to
   exported private certificates, and fails if the certificate is still mid-request (not yet issued).
   Don't assume this explicit call is a general-purpose renewal trigger for every certificate type;
   check the certificate's own renewal-eligibility field before relying on it.

Either way, a certificate's identifier (ARN) does not change across a renewal — the same certificate
resource continues to be referenced by the same identifier after a successful renewal, unlike the
ACME protocol's own renewal pattern (see `references/acme/acme-procedure.md`), where renewing means
requesting an entirely new certificate object.

### Import a certificate (bring your own, outside ACM's own issuance)

Submit a PEM-encoded certificate, its unencrypted private key (under a documented size limit), and
optionally its certificate chain, to bring an externally-issued certificate into ACM for use with
integrated services. Supplying the identifier of a previously imported certificate replaces
(re-imports) it in place rather than creating a new one — omit that identifier to import a genuinely
new certificate. **An imported certificate is never covered by ACM's managed renewal** — its renewal
remains entirely the caller's own responsibility, on whatever schedule the external issuer requires.

### Delete a certificate

**Stop and confirm with the operator before proceeding — deletion is documented as not reversible**,
and a certificate currently referenced by another AWS service cannot be deleted until that reference
is removed first; expect the delete to fail rather than silently detach the certificate from what's
using it. A certificate issued through ACM's own ACME-based path cannot be deleted through this
operation at all — ACM handles removing those on its own, well after expiration, rather than on
request. Deleting a certificate that was issued by a private CA has no effect on that CA itself; the
CA continues to exist (and continues to be billed) independently of any certificate it issued.

## Patterns

- **"Renewal" means two different things in ACM, and they have different eligibility rules** —
  automatic managed renewal (broad, based on in-use/exported status) and the explicit renewal call
  (narrower, exported-private-certificate-specific). Check which one applies before assuming a
  certificate will renew a particular way.
- **A certificate's ARN survives renewal but does not survive re-import or re-issuance** — renewing
  in place keeps the same identifier; importing a certificate with a new identifier (rather than
  supplying the prior one to re-import) creates a genuinely separate certificate resource.
- **Certificates ACM cannot manage the same way as everything else: ACME-issued and imported.**
  Neither is eligible for managed renewal, and ACME-issued certificates additionally can't be deleted
  directly — both are documented exceptions to the otherwise-uniform issue/renew/delete pattern the
  rest of this procedure describes.
- **Deletion is blocked while in use, not silently allowed** — removing an association with the
  consuming AWS service is a precondition to deleting the certificate, not something the delete call
  handles for the caller.

## Known limitations

- Covers requesting, validating, reading, the two renewal paths, importing, and deleting certificates
  through ACM's own API. Does not cover AWS Private CA's own direct certificate-authority
  administration (creating/managing a private CA itself), or the mechanics of ACM's own ACME-based
  issuance option beyond noting where it changes renewal/delete behavior above.
- The exact automatic managed-renewal timing (how far ahead of expiration ACM initiates it) is not
  confirmed to a specific day-count in the sources — do not assume or state a specific lead
  time; if exact timing matters for a task, confirm it against AWS's current renewal documentation
  directly rather than relying on this file for that number.
- The exact numeric revocation-reason vocabulary ACM surfaces (`RevocationReason`) includes both
  `SUPERCEDED` and `SUPERSEDED` as separate documented values in AWS's own reference — this looks
  like a vendor documentation inconsistency (likely a legacy duplicate spelling) rather than two
  genuinely distinct reasons; the sources do not identify a canonical spelling.
- Does not cover binding a certificate to a consuming resource (attaching it to a load balancer
  listener, a CloudFront distribution, etc.) — that belongs to the consuming service's own
  provisioning process, not this certificate-management procedure.

## Tools

| Operation | Description | Category |
|---|---|---|
| Request certificate | Request issuance of a new public or private certificate | Issuance |
| Describe certificate | Read a certificate's metadata, status, and validation/renewal state | Read |
| Get certificate | Retrieve the issued certificate body and chain | Read |
| Renew certificate | Explicitly trigger renewal for an eligible certificate | Renewal |
| Import certificate | Bring an externally-issued certificate into ACM | Issuance (external) |
| Delete certificate | Remove a certificate from ACM | Deletion |

## Verification checklist

- [ ] Validation method (DNS preferred, email as an alternative) was confirmed before assuming a
      public certificate request would complete unattended
- [ ] Certificate status was read from its own status field, not inferred from whether other fields
      were present
- [ ] The applicable renewal path (automatic managed renewal vs. the explicit renewal call) was
      identified before assuming a certificate would or wouldn't renew a particular way
- [ ] For an ACME-issued or imported certificate, managed-renewal and (for ACME-issued) direct-delete
      exceptions were accounted for rather than assumed to behave like a standard ACM-issued cert
- [ ] Deletion was preceded by explicit operator confirmation and confirmation the certificate is not
      currently referenced by another AWS service
