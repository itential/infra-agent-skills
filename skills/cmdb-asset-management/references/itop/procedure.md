# iTop — CMDB Configuration Item Management Procedure

Create, read, update, and delete Configuration Items (CIs) in iTop, and read the dependency
relationships between them, through iTop's REST/JSON services. Every operation is an HTTP call that
carries a JSON document naming an operation and a CI class; CIs are addressed by class plus a key
(a numeric object id, an OQL query, or a field-criteria object). Assumes an authenticated
REST client against the target iTop instance, using an account that holds the REST access profile and
write rights on the target class (see Patterns), is already available.
See `endpoints.md` for the literal request syntax behind every operation named below.

Source: iTop documentation, "REST/JSON services" (itophub.io wiki, `latest` branch), retrieved
2026-10-19. Facts below are restated from that page; anything the page does not state is marked as
unknown or an assumption.

## Operational procedure

### Common Sequences

**Create a CI:**
1. Search for an existing CI that would duplicate it (Read CIs, by class, with a filter on the
   identifying attributes). The create operation has no matching step of its own — see Patterns.
2. Create a CI of the target class with its attribute values.
3. Confirm from the response that the operation succeeded and capture the assigned object key.

**Update a CI:**
1. Read the CI to confirm exactly one object matches the key you intend to use.
2. Update the CI with the changed attributes.

**Look up what a CI depends on, and what depends on it:**
1. Read related CIs starting from the CI's class and key, relation "depends on".
2. Repeat with relation "impacts". These are separate questions; one call does not answer both.

**Delete a CI:**
1. Read related CIs in the "impacts" direction to see what hangs off it.
2. Run the delete as a simulation and review the report of every object that would be deleted or
   changed.
3. After operator confirmation (see the Delete step), run the delete for real.

### Read CIs

Search a single class for CIs. The key is a numeric id, an OQL SELECT statement, or a criteria
object. Choose which attributes come back with the output-fields setting: a comma-separated list,
`*` for every attribute of the class, or `*+` to include attributes of subclasses. Limit the number
of results and page through them with the limit and page settings (limit defaults to unlimited, pages
start at 1).

Success: the response code is 0 and the message states how many objects were found; the objects are
keyed `Class::id`. When nothing matches, the objects value is null rather than an empty collection.

Only one class can be returned per call. Avoid asking for the `*_list` attributes in the output
fields: they pull in every field of the linked objects, including blobs and link sets, and can
exhaust server memory.

### Create a CI

Create an object of the given class, supplying its attribute values, optionally which attributes
to return, and an optional comment recorded with the operation. External-key attributes accept an id,
an OQL query, or a criteria object. Blob attributes take base64 data with a filename and MIME type.
Case-log attributes take either a plain string (appended as a new entry) or structured entries. Link
sets take an array of relationship objects.

Success: response code 0 and the new object with its assigned key. Authentication, rights, or
version problems come back as the error codes listed in `endpoints.md`.

### Update a CI

Update exactly one object, identified by class plus key, supplying the changed attributes, optionally
which attributes to return, and an optional comment. The update fails with a "several items found"
error when the key matches more than one object; there is no bulk update.

### Read related CIs (relationships)

Starting from a class and key (an OQL key may select several starting objects), walk the dependency
graph. Choose the relation: "impacts" or "depends on". Optionally set the direction ("up" or
"down"), the maximum depth (default 20 iterations) and whether to take redundancy into account.

Success: response code 0, the related objects, and a relations map from each origin object to its
destination objects; the message summarizes the scope and the number found per class.

### Delete a CI

**Stop and confirm with the operator before the real delete.** Deleting a CI can delete or modify
other objects linked to it, and every affected object is listed in the response report with a status
code. Always run it first as a simulation (the simulate option) and show the operator the list.

A real delete is the same call without simulation. Check each object's status in the report:
0 means deleted as requested; 2 and 5 mean the object was automatically deleted or updated to keep
the data consistent; 1, 3 and 6 are failures; 4 means that object must be explicitly requested for
deletion.

## Patterns

- **Create always makes a new object — it does not check for an existing match.** The documentation
  describes create as creating a new object of the class and mentions no identification step. Search
  first when the asset may already exist (for example from another data source), or a duplicate CI
  results. Whether other iTop mechanisms such as data synchronization deduplicate is outside this
  procedure.
- **REST access needs more than an administrator profile.** The calling account needs the REST
  Services User profile and both write and bulk-write permission on each class it modifies. An
  account with only the Administrator profile is refused.
- **A delete is a cascade, not a single-row removal.** Linked objects can be deleted or updated as a
  side effect. The simulate option exists for this reason; use it before every real delete.
- **Relationship direction matters.** "Impacts" and "depends on" are separate queries.
- **Authentication parameters travel with the request.** Prefer HTTPS and POST: credentials are
  request parameters (or a token) rather than a login session.

## Known limitations

- Covers CI create, read, update, delete and dependency reads only. Does not cover state transitions
  (the stimulus operation), attachment or inline-image handling, credential checking, class or
  datamodel administration, or data synchronization.
- No bulk update, and a read returns one class only.
- The source does not state HTTP status codes for failures, rate limits, request-size limits, or what
  an update does when the key matches no object. Treat these as unknown and report whatever the
  response code and message say.
- Which classes count as CIs, and which attributes are mandatory, depends on the target instance's
  datamodel; the source does not enumerate them. Consult the instance's own datamodel documentation.

## Tools

| Operation | Description | Category |
|---|---|---|
| Read CIs | Search one class by id, OQL, or criteria | CI Records |
| Create CI | Create one object of a class | CI Records |
| Update CI | Update exactly one object | CI Records |
| Delete CI | Delete objects, with optional simulation and a cascade report | CI Records |
| Read related CIs | Walk dependency relations from a CI | CI Relationships |

## Verification checklist

- [ ] Account holds the REST access profile and write plus bulk-write rights on the class
- [ ] A search for an existing matching CI preceded every create
- [ ] Response code was 0 and the returned key or found-count was checked, not assumed
- [ ] An update matched exactly one object
- [ ] Relationship reads covered both "depends on" and "impacts" where the ask involved both
- [ ] Every delete was simulated first, the cascade report was reviewed, and the operator confirmed
      before the real delete
- [ ] Per-object statuses in the delete report were checked, not just the overall code
