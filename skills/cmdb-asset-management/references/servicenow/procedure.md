# ServiceNow — CMDB Configuration Item Management Procedure

Create, read, update, and delete Configuration Items (CIs) in the ServiceNow CMDB, and read the
relationships between them, using ServiceNow's two overlapping APIs — the generic **Table API**
(works against any table, including `cmdb_ci` and its subclasses, but bypasses CI identification
logic) and the **CMDB Instance API** (CMDB-specific, routes writes through the Identification and
Reconciliation Engine — IRE — to avoid creating duplicate CIs). This procedure defaults to the CMDB
Instance API for writes and the Table API for relationship reads, per ServiceNow's own guidance — see
Patterns for why. Distinct from `change-management`'s ServiceNow procedure — that's change *requests*;
this is the configuration-item inventory those changes reference. Assumes an authenticated REST client
against the target ServiceNow instance (roles sufficient for the target CI class's ACLs — typically
`cmdb_read`/`cmdb_write` variants) is already available. See `endpoints.md` for the literal request
syntax behind every operation named below.

## Operational procedure

### Common Sequences

**Create a new CI, letting ServiceNow's identification engine check for an existing match first:**
1. Create/Update a CI via the CMDB Instance API — the IRE compares the payload against existing CIs
   using that class's identification rules; if a match is found, it updates the existing CI instead of
   creating a duplicate. Report CREATED or UPDATED based on which the response indicates, not assumed
   from the call succeeding.

**Look up a CI and its relationships (e.g. "what does this server depend on / what depends on it"):**
1. Read the CI itself against its specific class table (e.g. server CIs), not the generic CI table,
   when the caller knows the class — this returns class-specific fields directly.
2. Read CI Relationships, filtered to the CI's identifier as either the parent or the child side, to
   find its relationships and their type.

**Bulk-query CIs matching a filter (e.g. all Linux servers in a given location):**
1. Read CIs against the specific class table with a query filter, not the CMDB Instance API — the CMDB
   Instance API is documented as one-record-at-a-time for writes; for reads and bulk filtering, the
   class-table read is the more direct path.

### Create or Update a CI (CMDB Instance API — recommended for writes)

**This routes through the Identification and Reconciliation Engine (IRE).** The IRE evaluates the
submitted attributes against that class's identification rules (in priority order) to decide whether
this payload matches an existing CI. If a match is found, the existing CI is updated rather than a new
one created — this is the entire reason to prefer this capability over a raw class-table create for CI
writes. If reconciliation rules apply and another data source already supplied a value for an
attribute this payload also sets, the reconciliation rules (not simply "last write wins") determine
which source's value is trusted — don't assume your write always takes effect on a contested field.

**One record per call** — the CMDB Instance API explicitly does not support bulk insert/update/delete;
each call handles exactly one CI. For bulk operations, use a class-table write instead (see Bulk-query
sequence above), accepting that bulk writes this way bypass IRE matching.

Confirm success: the response indicates either a newly-created record or an update to an existing
identifier — check which occurred rather than assuming every successful call created a new record.

Common missing-field error: omitting the discovery-source attribute has been observed to trigger a
validation error on some CI classes — if a create call fails with a missing-attribute error, check this
field specifically before assuming the class's full required-field set is otherwise satisfied.

### Read a CI (class-table read)

Read a single CI by its identifier, or a filtered list using a query expression against the class's
table. See `endpoints.md` for the exact query-parameter set: query filter, field-list limiting,
result-count limiting/paging, and controlling whether reference fields return raw values, display
values, or both.

Prefer querying the specific class table (server, Linux server, etc.) over the base CI table when the
class is known — the base table only exposes fields common to every CI class, not the class-specific
ones.

### Read CI Relationships

Read the CI-relationship records where the target CI's identifier appears as either the parent or the
child side — read both directions, since a query for only the parent side misses relationships where
the CI is the child. Each relationship record carries a `parent` CI, a `child` CI, and a relationship
type (e.g. "Depends on::Used by").

### Update a CI Directly via Class-Table Write (bypasses IRE — use deliberately, not by default)

Use this only when the exact CI identifier is already known and IRE-based identification/reconciliation
genuinely isn't needed for this update (e.g. a field the calling system is the sole authoritative
source for) — otherwise prefer the CMDB Instance API's create/update behavior even for what is
logically an update, so reconciliation rules still apply if another source also touches that CI.

### Delete a CI

**Stop and confirm with the operator before proceeding** — deleting a CI can break relationship
records referencing it and anything else that references it by identifier (change requests,
incidents). Confirm nothing currently depends on this CI via a relationship read (above) before
deleting, not after.

## Patterns

- **The CMDB Instance API's whole reason to exist is IRE-based deduplication — a raw class-table create
  skips that check entirely.** If the same physical/logical asset might already exist in the CMDB from
  Discovery, Service Mapping, or another integration, a bare class-table create can produce a duplicate
  CI where the CMDB Instance API would have matched and updated instead. Default to the CMDB Instance
  API for CI writes unless there's a specific reason not to.
- **Reconciliation rules mean "your write succeeded" doesn't always mean "your value stuck."** When
  multiple sources feed the same CI attribute, the source with reconciliation priority wins on that
  field — a successful write can be silently overridden on the next reconciliation pass from a
  higher-priority source. Don't treat write-success as proof a specific field now holds your value if
  another source also claims that field.
- **A relationship is two rows' worth of context (parent and child), not one.** Querying only the
  parent side gives an incomplete picture — always check both directions when the ask is "what relates
  to this CI."

## Known limitations

- Covers Configuration Item CRUD (preferring CMDB Instance API for writes, class-table reads for reads/
  bulk/relationships) and relationship reads — does not cover CI class schema administration,
  Discovery/Service Mapping configuration, or writing new relationship records (creating/modifying
  relationship rows directly) — only reading existing relationships is covered.
- **The CMDB Instance API is one-record-at-a-time** — no bulk insert/update/delete. A caller needing
  bulk writes must either loop calls to this capability (accepting IRE matching per call) or use a
  class-table write directly (accepting no IRE matching).
- **Deleting a CI is not itself gated by relationship checks in this procedure** — confirming nothing
  depends on the CI before deleting is this skill's own discipline, not a platform-enforced safety net;
  ServiceNow will not automatically refuse a delete just because relationship rows reference the CI.
- Exact identification-rule and reconciliation-rule behavior is class-specific and configured per
  ServiceNow instance — this procedure describes the mechanism, not any particular instance's actual
  configured rules. Confirm the target instance's identification rules for the specific CI class in use
  if precise duplicate-matching behavior matters for the task at hand.

## Tools

| Operation | Description | Category |
|---|---|---|
| CMDB Instance API create/update | Create or update a CI, routed through IRE for identification/reconciliation | CI Records |
| Class-table read | Read one or many CIs, with class-specific fields | CI Records |
| Relationship read | Read relationships a CI participates in, as parent or child | CI Relationships |
| Class-table update/delete | Direct update or delete, bypassing IRE | CI Records |

## Verification checklist

- [ ] CI writes used the CMDB Instance API by default, with a specific documented reason if a
      class-table write was used instead
- [ ] A create call's response was checked for CREATED vs. UPDATED (an IRE match), not assumed to
      always be a new record
- [ ] Relationship reads checked both the parent and child directions against the target CI's
      identifier
- [ ] Delete was only performed after confirming (via a relationship read) that nothing currently
      depends on the CI, and after explicit operator confirmation
- [ ] Any field known to be fed by multiple sources was not assumed to hold this call's value without
      confirming against reconciliation-rule priority
