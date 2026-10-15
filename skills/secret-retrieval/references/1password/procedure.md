# 1Password (Connect API) — Secret Retrieval Procedure

Reads or writes a secret value held as a field on a vault item, via a self-hosted 1Password Connect
server. Assumes a Connect server is already deployed and reachable, and the caller already holds a
Connect access token scoped to the vault(s) it needs — issuing or scoping that token is out of
scope here.

Source: 1Password's own Connect API reference (developer.1password.com/docs/connect, which
currently redirects to www.1password.dev/connect/connect-api-reference/), retrieved 2026-09-29.

## Operational procedure

### 1. Resolve the vault

1Password organizes items inside vaults, and every item operation is scoped to one vault by its
UUID. If the caller only has a vault name, list vaults and match by name first (1Password's own
filter syntax accepts an SCIM-style `name eq "..."` expression) — **never guess a vault UUID**; if
no match is found, stop and report it rather than falling back to an arbitrary vault.

### 2. Resolve the item

A secret in 1Password is a field inside an item (e.g. a Login item's password field, or a Secure
Note's contents), not a bare key/value pair addressed by path the way Vault or a cloud secrets
manager works. To read or write a value:

- If the item's UUID is already known, use it directly.
- Otherwise, list items in the resolved vault and filter by title (1Password's filter syntax again
  accepts title matching). Listing items returns item summaries without their field contents —
  a second call against the specific item UUID is required to see the actual field values.
- If more than one item matches the title filter, **stop and ask the operator which one is
  intended** rather than picking the first result — item titles are not guaranteed unique within a
  vault.

### 3. Read a secret value

Fetch the full item by vault UUID + item UUID. The item's `fields` array holds each field's
`label`, `type`, `purpose` (e.g. `USERNAME`, `PASSWORD`, `NOTES`, or unset for a custom field), and
`value`. Identify the specific field the caller needs by its `label` or `purpose` — an item
commonly has multiple fields, and only one of them is usually the secret value actually wanted
(e.g. a Login item also carries a username field alongside the password).

### 4. Create a new item holding a secret value

**Confirm the category and vault with the operator before creating an item** if either is
ambiguous — 1Password enforces a fixed set of item categories (Login, Password, API Credential,
Secure Note, etc.) and the category affects which fields are meaningful.

Submit the new item's `title`, target `vault.id`, `category`, and a `fields` array with each
field's `label`, `type`, `purpose` (where applicable), and either a literal `value` or a
`generate: true` flag plus a `recipe` describing how 1Password itself should generate the value
(length, character sets). Generating server-side avoids ever having to transmit a caller-chosen
plaintext value for that field.

### 5. Update an existing item's secret value

**Confirm with the operator before overwriting a field's value** — 1Password does not version
field history in a caller-addressable way, so a mistaken overwrite has no built-in prior-value
recovery.

Two supported approaches:
- A full replace of the item (submit the entire updated item body) — appropriate when several
  fields are changing together, but requires re-submitting fields that aren't changing too, or they
  get dropped.
- A partial update following RFC 6902 JSON Patch semantics (`add`/`remove`/`replace` operations
  against field-level paths) — appropriate for changing exactly one field's value without touching
  the rest of the item. Prefer this when only the secret value itself is changing, since it doesn't
  risk clobbering unrelated fields.

### 6. Delete an item

**This is a hard-to-reverse action — stop and confirm with the operator before submitting a
delete.** 1Password's own documentation describes item deletion as permanent. Delete by vault UUID
+ item UUID.

### 7. Handle documented errors

- **401 (invalid/missing token)** — the Connect access token is missing, malformed, or rejected;
  this is an authentication problem to resolve outside this skill, not a retry-able condition.
- **403 (vault not in scope)** — the token is valid but isn't scoped to the vault being targeted;
  report this rather than trying a different vault as a workaround, since scope is deliberately
  restricted by whoever issued the token.
- **404 (vault or item not found)** — either the UUID is wrong, or (for a vault) the resolution in
  step 1 didn't actually confirm a match — re-check rather than retrying blindly.
- **400 (invalid item category / invalid input on create)** — the submitted item body doesn't match
  what 1Password expects for the chosen category; check the category-specific field requirements
  before resubmitting.

## Patterns

- **An item is a bundle of fields, not one secret.** Always resolve to a specific field within the
  item before treating any single value as "the secret" — never assume the first field, or a field
  literally labeled "password," is automatically the one the caller wants without checking `label`/
  `purpose` against what was actually asked for.
- **Listing items is a lightweight summary call; fetching one item is the only call that returns
  field values.** Don't expect field contents from the list-items response.

## Known limitations

- Requires a self-hosted 1Password Connect server — this procedure does not cover 1Password's
  separate SaaS-hosted APIs (e.g. the Service Account-based `1password.com` REST endpoints), which
  have a different auth model and are not the same integration surface.
- No caller-addressable version history for field values — an overwrite cannot be rolled back via
  the API the way Vault KV v2 or Azure Key Vault versions can.
- Does not cover file attachments on an item (a separate files sub-resource) — only text field
  values.

## Tools

Every operation maps to the 1Password Connect REST API — see `endpoints.md` for literal
request/response shape.

| Operation | Description | Category |
|---|---|---|
| List vaults | Resolve a vault name to its UUID | Vault Lookup |
| List items in a vault | Resolve an item title to its UUID (summary only, no field values) | Item Lookup |
| Get item by UUID | Read an item's full field values | Secret Read |
| Create item | Create a new item with field values (literal or generated) | Secret Write |
| Update item (full or patch) | Overwrite an item's field value(s) | Secret Write |
| Delete item | Permanently remove an item | Secret Delete |

## Verification checklist

- [ ] Vault UUID was resolved by an exact name match, not guessed or assumed from the first result
- [ ] If multiple items matched a title filter, the operator was asked to disambiguate
- [ ] The specific field (by label/purpose) intended as "the secret" was confirmed, not assumed
- [ ] Any create used the correct item category for what's being stored
- [ ] Any update or delete of an existing item was confirmed with the operator first
- [ ] The retrieved field value was not written into any log, report, or status message
