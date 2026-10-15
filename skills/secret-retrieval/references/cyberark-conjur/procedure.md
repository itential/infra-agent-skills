# CyberArk Conjur — Secret Retrieval Procedure

Retrieves or sets the value of a Conjur `variable` resource — Conjur's term for a secret-holding
resource that a policy has already defined. Assumes the caller already has valid credentials
(a login name plus either a password or API key) for a Conjur identity that has been granted the
relevant permission on the target variable; provisioning that identity or writing the policy that
creates the variable itself is out of scope here.

Source: CyberArk's own canonical Conjur OpenAPI specification, published and maintained at
github.com/cyberark/conjur-openapi-spec, and CyberArk's hosted documentation describing the same
authentication and secrets endpoints (docs.cyberark.com, under the Conjur/Secrets Manager developer
API sections — search-indexed confirmation of endpoint names and behavior used where the docs site
itself could not be fetched directly, retrieved 2026-09-29).

## Operational procedure

### 1. Authenticate — two-step token exchange

Conjur uses a two-step flow rather than a single login call:

1. **Obtain an API key** (skip this step if the caller already has a long-lived API key for the
   identity, e.g. for a machine/Host identity that was issued one when created) — present the
   identity's login name and password over HTTP Basic authentication against the API-key endpoint.
   The response body is the plain-text API key. Because Conjur hashes stored passwords expensively
   by design, treat this call as relatively costly and not something to repeat per-request.
2. **Exchange the API key for a short-lived access token** — submit the API key as the raw request
   body against the authenticate endpoint for the identity's login name. The response is a
   short-lived access token; subsequent calls present it as `Authorization: Token token=<token>`
   (base64-encoded per Conjur's own convention). Re-authenticate to get a fresh token once it
   expires — this skill does not manage a token cache across calls.

Both the `account` (Conjur's organization/account name) and the `login` must be URL-encoded in the
path — a login containing `@` or a host login prefixed `host/` needs percent-encoding before use
(e.g. `host/webserver` becomes `host%2Fwebserver`).

### 2. Retrieve a secret value

Fetch the variable's current value by account, resource kind (almost always `variable`), and
URL-encoded identifier. Conjur returns the raw secret value in the response body (plain text, not
wrapped in a JSON envelope) — there is no separate metadata field mixed into this response the way
Vault or Azure Key Vault return alongside the value.

- To retrieve a specific prior value rather than the latest, supply the `version` query parameter —
  Conjur retains a bounded number of the most recent versions (the source states the last twenty)
  server-side, though unlike Vault KV v2 or Azure Key Vault there is no separate metadata call to
  enumerate what versions currently exist before picking one.
- To fetch several variables' values in one call (more efficient than one call per variable), use
  the batch-fetch endpoint with a comma-separated, URL-encoded list of fully-qualified resource
  identifiers.

### 3. Set a secret's value

**The variable resource must already exist (defined via Conjur policy) before a value can be set
against it** — this call adds/overwrites the value inside an existing variable, it does not create
the resource itself. If the identifier doesn't resolve to an existing variable, report that as a
policy-provisioning gap rather than attempting to work around it.

**Confirm with the operator before overwriting a variable that already holds a value in active
use** — Conjur's own guidance is that a variable can technically hold a secret at any resource, but
the documented best practice is to only store/retrieve through variable resources specifically;
follow that convention rather than deviating to another resource kind.

### 4. Handle documented errors

- **400 (Bad Request)** — malformed account/kind/identifier in the path.
- **401 (Unauthorized)** — missing, expired, or invalid access token; re-run step 1's token exchange
  rather than retrying the same token.
- **403 (Inadequate Privileges)** — the authenticated identity lacks the Conjur permission (e.g.
  `execute` for read, `update` for write) on this specific variable — a policy change by an
  operator with sufficient privilege is required, not a retry.
- **404 (Resource Not Found)** — the variable doesn't exist at that identifier; verify the
  account/kind/identifier rather than assuming a transient issue.
- **422 (Unprocessable Entity)** — the request was well-formed but semantically invalid (e.g. an
  out-of-range version number on a read).

## Patterns

- **Two distinct credentials are in play and must not be confused: the long-lived API key and the
  short-lived access token.** The API key is what's exchanged to get a token; only the token (not
  the API key) is presented on ordinary secret read/write calls.
- **The response to a single-variable read is a bare value, not a JSON object** — don't expect a
  `data`/`value` wrapper the way Vault, AWS Secrets Manager, or Azure Key Vault return one. The
  batch-fetch endpoint, by contrast, *does* return a JSON object mapping each requested identifier
  to its value — the two response shapes are genuinely different.

## Known limitations

- Does not cover Conjur policy authoring (defining a new `variable` resource, granting permissions
  on it) — that's a prerequisite this skill assumes is already done.
- Does not cover Conjur's non-default authenticators (Azure, GCP, AWS IAM, JWT, Kubernetes, LDAP,
  OIDC) beyond noting that step 1's password/API-key flow is the default — an environment using one
  of those instead has a different, platform-specific authentication call in place of step 1's
  login/authenticate pair, and that call's exact shape needs to be confirmed against Conjur's own
  authenticator-specific documentation before substituting it in.
- The documented server-side retained-version count (twenty) for a variable is a retention limit,
  not a caller-facing version-listing capability — there is no documented call to enumerate what
  versions currently exist the way Vault KV v2's metadata endpoint does.

## Tools

Every operation maps to the Conjur REST API — see `endpoints.md` for literal request/response
shape.

| Operation | Description | Category |
|---|---|---|
| Get API key | Exchange login + password (HTTP Basic) for a long-lived API key | Authentication |
| Authenticate | Exchange login + API key for a short-lived access token | Authentication |
| Get a secret | Read a variable's current or specific-version value | Secret Read |
| Get multiple secrets (batch) | Read several variables' values in one call | Secret Read |
| Set a secret | Write/overwrite a variable's value | Secret Write |

## Verification checklist

- [ ] The two-step auth flow (API key, then access token) was followed — the API key itself was
      never presented on an ordinary secret read/write call
- [ ] Account, kind, and identifier path segments were correctly URL-encoded
- [ ] The target variable was confirmed to already exist (via policy) before attempting a write
- [ ] Any overwrite of an existing value was confirmed with the operator first
- [ ] The retrieved secret value was not written into any log, report, or status message
