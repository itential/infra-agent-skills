# Cisco ACI APIC — Read Fabric, Endpoint, Fault and Object State

Reads live fabric state from the APIC controller: system nodes, attached endpoints, faults, or one named managed object. Read-only: no configuration is created, changed or deleted.

Source (Cisco, APIC REST API Configuration Guide, "Using the REST API", retrieved 2026-10-26). Wire bindings are in [endpoints.md](endpoints.md).

## Common Sequences

- **Fabric inventory:** Open a session → Read a class collection → Page through the result.
- **Fault evidence:** Open a session → Read faults (optionally by cause) → Page through the result.
- **One object:** Open a session → Read a managed object by its distinguished name.

## Open a session

The controller authenticates by username and password and returns a token that is presented afterwards as a session cookie. A session lasts 600 seconds by default; refresh it before it lapses or log in again. An authentication or authorization failure is a failed read, not an empty fabric. The token is a secret credential: keep it and the password out of reported output.

## Read a class collection

Read every instance of a managed-object class. Classes covering this procedure: system nodes (controllers, spines, leaves), attached endpoints, and fault instances. Class names, attributes and access privileges depend on the release; the deployed controller serves its own model reference. Not documented: a universal field list beyond what that reference shows, so do not assume attributes the deployed release does not list.
Success is the returned object list and its reported total count. Faults and endpoints are separate classes from system nodes. A cleared or absent fault does not show that applications are reachable.
To restrict faults to configuration failures, apply an equality filter on the fault cause field.

## Page through the result

Collections are retrieved in pages: zero-based page number plus a page size. Every request, paged or not, computes a fresh result set. Pages are not held on the controller, so a later page can reflect a fabric that changed since the earlier one: objects can repeat, move or be missed across pages. Report paged coverage as a sequence of point-in-time reads, not one consistent snapshot.
Large pages are truncated at a per-page object cap that applies from a stated release (see endpoints.md). Ordering across pages is by an order-by option naming a class property; no documented page-size maximum is stated beyond that.
Two scale errors are documented: the query-timeout error (retry a few times, as the guide advises) and the result-too-large error (narrow the query with filters or a smaller class scope before retrying), both listed with their exact text in endpoints.md. Other errors remain failed reads with their native detail.

## Read a managed object

An object is addressed by its full distinguished name. Reading with the self scope returns that one object's properties; the documented subtree-include option can add its health or fault records where the model supports it. Success is the intended object's distinguished name and properties. Absence of health or fault records is absence, not a score of zero.
Password properties come back blank on reads. Posting a read response back to the controller would write those passwords as blank, so a read response is never replayed as a write.

## Patterns

- The login call is a POST but only opens a session; nothing in the fabric configuration is created or changed by any call in this procedure.

## Known limitations

- Read-only. Creating tenants, policies or any managed object, and subscriptions or event streams, are outside this procedure.
- Log-record queries have their own ordering and paging rules and are not covered.
- No health threshold, fault-severity judgement, contract analysis or reachability verdict is made.
- No comparison operation: to compare, repeat the same class query with the same filters at two times and diff outside the platform, noting the paging caveat above.

## Tools

| Operation | Description | Category |
|---|---|---|
| Open session | Authenticate and obtain the session cookie | REST API |
| Read class collection | Retrieve instances of a class, optionally filtered and paged | REST API |
| Read managed object | Retrieve one object by distinguished name | REST API |
| Refresh session | Reset the session timer and obtain a new token | REST API |

## Verification checklist

- [ ] The target controller, release, class or object, and filters are explicit.
- [ ] Page coverage and the point-in-time nature of paged reads are stated.
- [ ] Scale errors were handled by retry (timeout) or by narrowing (too big), not an unchanged retry.
- [ ] Errors and empty results are reported as such, not as a healthy fabric.
- [ ] No read response was posted back.
