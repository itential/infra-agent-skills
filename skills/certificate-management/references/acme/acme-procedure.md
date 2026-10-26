# ACME Protocol (e.g. Let's Encrypt) — Certificate Lifecycle Procedure

Requests, renews, inspects, and revokes TLS certificates from any Certificate Authority that
implements the Automatic Certificate Management Environment (ACME) protocol as defined in RFC 8555 —
Let's Encrypt is the most widely used public CA built on this protocol, but any ACME-compliant CA
(a private/internal CA running an ACME front end, another public ACME CA) follows the same wire
mechanics described here. Assumes an ACME client capable of generating and signing JWS requests, and
a way to satisfy the chosen challenge type (control of a web server for `http-01`, or the ability to
create a DNS TXT record for `dns-01`), are already available — this procedure does not provision
either. See `acme-endpoints.md` for the literal request/response shapes behind every operation below.
Citation: RFC 8555, "Automatic Certificate Management Environment (ACME)," IETF, retrieved
2026-09-17 (https://datatracker.ietf.org/doc/html/rfc8555).

## Operational procedure

### Discover the CA's operation endpoints

Before any other call, fetch the CA's directory resource. It returns the URLs for every other
operation this procedure uses (new-account, new-order, revoke, nonce issuance, and an optional
metadata block describing the CA's terms-of-service link and whether it requires external account
binding). Treat these URLs as CA-specific — different ACME CAs expose the same operation set at
different paths, so this directory fetch is the one step that must happen first, every time, against
a CA not previously discovered.

### Establish an account (one-time per key pair, per CA)

Create an account by submitting the account holder's contact information and explicit agreement to
the CA's terms of service, signed with the account's own key pair. The CA returns an account
resource whose status is one of valid, deactivated, or revoked, along with a URL that identifies this
account in every later signed request. Re-submitting the same account-creation request with a key
pair that already has an account returns the existing account rather than creating a duplicate — an
ACME client can safely treat this step as idempotent per key pair.

### Anti-replay: fetch a fresh nonce before every signed request

Every signed request this procedure makes must carry a nonce obtained from the CA immediately
beforehand (or reused from a nonce the CA supplied in its previous response) — a stale or reused
nonce is rejected. If a request is rejected specifically for a bad nonce, the CA's error response
carries a fresh nonce the client should use to immediately retry the same request, rather than
restarting the whole operation.

### Issue a certificate

1. **Submit a new order** naming every domain identifier the certificate should cover (the primary
   name and any additional names/wildcards). The CA returns an order resource that starts in a
   pending state, listing one authorization to complete per identifier and a URL to submit the
   certificate signing request to once every authorization is satisfied.
2. **Satisfy each identifier's authorization** by completing one of the challenge types the CA
   offers for it — typically proving control of the domain either by publishing a specific value at
   a well-known HTTP path on that domain (`http-01`) or by publishing a specific DNS TXT record under
   that domain (`dns-01`). Provision the challenge value first, then tell the CA the challenge is
   ready to be checked; the CA performs its own validation attempt asynchronously rather than
   checking synchronously in that same call.
3. **Poll until each authorization reaches a settled state.** An authorization starts pending, moves
   through the CA's own validation attempt, and settles as either valid (the challenge was verified)
   or invalid (verification failed or expired) — a client should poll rather than assume validation
   completes within the same request that signaled readiness.
4. **Confirm the order is ready**, meaning every required authorization for that order settled as
   valid. Only once the order reaches this state can the certificate signing request be submitted.
5. **Finalize the order** by submitting a certificate signing request (CSR) covering the same set of
   identifiers the order was created for. The order moves into a processing state while the CA
   issues the certificate, then settles as valid once issuance completes, or invalid if it doesn't
   (a name mismatch between the CSR and the order's identifiers is a documented reason a finalize
   attempt can fail).
6. **Download the issued certificate** once the order is valid, by fetching the certificate resource
   the valid order points to. The CA returns the leaf certificate together with the chain needed to
   establish trust up to a CA the client's peers already trust.

### Renew a certificate

The protocol has no dedicated renewal call — renewing is submitting a brand-new order for the same
set of identifiers and completing the same issue sequence above again. A CA may allow reusing an
authorization that is still within its own validity window instead of re-validating a domain from
scratch, but a client should not assume this and should be prepared to satisfy a fresh challenge per
identifier. Because renewal is just a new order, the resulting certificate is a distinct object from
the one it replaces (a new serial number) — do not assume the old certificate's identifier or serial
carries forward.

### Read certificate/order/authorization state

Fetch the specific resource (account, order, authorization, or challenge) whose current state is
needed — each carries its own status field (see the state values captured in `acme-endpoints.md`).
Reading these resources costs an authenticated request each, the same as any other ACME call — there
is no separate unauthenticated "just check status" shortcut in the base protocol.

### Revoke a certificate

**Stop and confirm with the operator before proceeding — revocation is expected to be permanent and
is a documented irreversible action for the certificate in question.** Submit the certificate to be
revoked to the CA's revocation operation, optionally naming a reason. The request can be authenticated
either with the private key belonging to the certificate itself (proving possession of the
certificate being revoked, without needing the original account) or with the account key that
requested the certificate in the first place — either is sufficient authorization per the protocol.
A successful revocation returns without a response body; there is no separate "unrevoke."

## Patterns

- **Nothing about "renew" is special at the wire level — it's a fresh order.** Any renewal-specific
  behavior (skipping a challenge because an authorization is still valid, timing renewal ahead of
  expiry) is CA policy layered on top of the same order/authorization/finalize sequence, not a
  distinct protocol feature. Don't design around an expected "renew" endpoint that doesn't exist in
  the base protocol.
- **Validation is asynchronous — always poll, never assume synchronous completion.** Telling the CA a
  challenge is ready to check is not the same event as the CA finishing that check; both
  authorizations and orders pass through in-progress states (processing/pending) before settling.
- **A finalize call only succeeds once every identifier's authorization is already valid** — attempting
  to finalize before the order is ready is expected to fail, not a sign of a broken CSR.
- **Revocation accepts two different kinds of proof of authority** (the certificate's own key, or the
  account key that requested it) — a client that only has the certificate and its key (no longer has
  the original account) can still revoke, which matters for the confirmation-gate step above.

## Known limitations

- Covers certificate issue, renewal-as-reissue, state reads, and revocation per RFC 8555's base
  protocol. Does not cover account key rollover, pre-authorization (requesting an authorization ahead
  of an order), external account binding setup, or CA-specific extensions some ACME CAs layer on top
  of the base protocol.
- The exact numeric revocation-reason codes accepted by `reason` are drawn from a separate standard
  (X.509 CRL reason codes) and are unverified value-by-value — if a specific reason code
  beyond "unspecified" or "key compromise" is needed, confirm the exact code against the target CA's
  own documentation before using it, rather than assuming a code from another context applies as-is.
- This procedure describes the CA-agnostic base protocol. A specific ACME CA (Let's Encrypt or any
  other) may add its own rate limits, staging/test environments, or restrictions on which challenge
  types it offers for a given identifier (e.g. wildcard names may require `dns-01` specifically) —
  confirm those CA-specific constraints against that CA's own operational documentation before
  relying on this procedure alone for production issuance volume.
- Does not cover installing/binding the resulting certificate into a web server, load balancer, or
  other consuming system — see this capability's own "Known limitations" for where that boundary
  sits.

## Tools

| Operation | Description | Category |
|---|---|---|
| Directory fetch | Discover this CA's operation URLs | Discovery |
| New account | Register (or retrieve) an account bound to a key pair | Account |
| New order | Request issuance for a set of domain identifiers | Issuance |
| Challenge readiness | Signal a challenge is provisioned and ready to validate | Issuance |
| Order/authorization/challenge read | Check current status of an in-progress or completed request | Read |
| Finalize order | Submit the CSR once all authorizations are valid | Issuance |
| Certificate download | Retrieve the issued certificate and chain | Read |
| Revoke certificate | Revoke a previously issued certificate | Revocation |

## Verification checklist

- [ ] The CA's directory was fetched (or a previously cached copy confirmed current) before issuing
      any other request against a CA not already in use
- [ ] Every identifier on the order has a settled (valid) authorization before finalize was attempted
- [ ] Renewal was treated as a new order for the same identifiers, not assumed to reuse the prior
      certificate's serial or identity
- [ ] Revocation was preceded by explicit operator confirmation, and used either the certificate's
      own key or the requesting account's key to authenticate
- [ ] Any CA-specific constraint (rate limits, supported challenge types per identifier type) was
      checked against that specific CA's own documentation, not assumed from the base protocol alone
