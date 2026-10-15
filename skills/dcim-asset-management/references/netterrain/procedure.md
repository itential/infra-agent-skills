# NetTerrain (Graphical Networks) — Device Asset & Rack Provisioning Procedure

Create, read, update, or delete a device asset record on NetTerrain, including mounting/dismounting
it to a rack-unit position, and create/read/update/delete the rack container it can be mounted into.
Covers the `devices` and `racks` object types in NetTerrain's WAPI v1 REST interface. Does not cover
power-circuit-level assignment (NetTerrain's own docs describe rack `power`/`power_used` as
rack-level capacity totals rather than a discrete per-circuit assignment object — no source retrieved
for this skill documents a separate circuit-assignment call), cabling/link records, cards/slots/ports
sub-objects, or the generic `nodes`/`node_types` collections that devices and racks specialize.
Assumes an authenticated REST client against a specific NetTerrain instance's WAPI (a bearer access
token for any write call; see Step 1) is already available.

Sources (see `endpoints.md` for the literal wiring drawn from each):
- Graphical Networks, "Getting Started with REST API: Part 1 (Basic Procedures)",
  https://graphicalnetworks.com/blog-getting-started-with-rest-api-part-1/, retrieved 2026-09-29.
- Graphical Networks, "Getting Started with REST API: Part 2 (Data Retrieval, Writing, Deletions)",
  https://graphicalnetworks.com/blog-getting-started-with-rest-api-part-2/, retrieved 2026-09-29.
- Graphical Networks, "Getting Started with REST API: Part 3 (Collections, Filters, Expansions)",
  https://graphicalnetworks.com/blog-getting-started-with-rest-api-part-3/, retrieved 2026-09-29.
- NetTerrain's own generated WAPI v1 OpenAPI/Swagger definition. Per the vendor's blog series above,
  this definition is served directly by each NetTerrain instance and reachable from its Help ribbon
  ("REST Guide"); the version consulted for this skill was a definition export retrieved from a
  previously provisioned NetTerrain instance, used to confirm exact field names, required-vs-optional
  create/update fields, and status codes for the `devices` and `racks` operations. Treat the live
  Swagger page on the target instance as the authoritative field list — a given deployment's schema
  can carry local customizations.

## Operational procedure

1. **Establish the write credential.** Reading (`GET`) can be done with HTTP Basic auth over TLS, but
   the vendor's own guidance calls Basic auth unsuitable for anything beyond that — it resends raw
   credentials on every call and has no CSRF protection. For any create/update/delete call, first
   exchange credentials for a bearer access token via the instance's dedicated token endpoint (see
   `endpoints.md`), then send that token on every subsequent write call's Authorization header. If the
   instance's Swagger definition shows a request-verification/anti-forgery header parameter on the
   write operations, populate it too — that instance has anti-forgery checking turned on
   (`ValidateAntiForgeryToken` in the server's own configuration) and will reject writes missing it.
2. **Identify the target instance's base path.** Every call is rooted at that instance's own
   versioned API base path (see `endpoints.md`) — there is no shared/global NetTerrain endpoint. Confirm this base path (and
   whether the deployment sits behind a non-default port or reverse-proxy prefix) before building any
   request.
3. **Resolve prerequisite type references.** A device cannot be created without a reference (`href`)
   to an existing entry in the device-type library, and a rack cannot be created without a reference to
   an existing rack-type entry — types themselves are a separate, pre-managed collection
   (`device_types`, `rack_types`), not something this procedure creates inline. Look the desired type
   up by listing or filtering that collection first; if no matching type exists, stop and report
   REJECTED_MISSING_TYPE rather than guessing an href.
4. **Create a rack (if the target rack doesn't already exist).** Submit a create call with the rack's
   name, its resolved rack-type href, a `base_node` reference pointing at the parent diagram/location
   node it lives in, and its power and weight capacity limits. Do not include an `href` in a create
   body — NetTerrain treats a create request that already carries one as a conflict. A successful
   create returns the new rack object including its assigned id/href; capacity-consumption fields
   (`power_used`, `weight_used`, `available_rack_units`) are server-computed rollups, not inputs, and
   should never be sent on create or update.
5. **Create a device asset.** Submit a create call with the device's name, its resolved device-type
   href, and a placement — either:
   - **Rack-mounted:** a reference to the specific container slot inside the target rack
     (`parent_rack_container` href) plus the numeric rack-unit offset (`container_position`) at which
     it starts; or
   - **Unmounted/free-floating:** a `base_node.parent_diagram` href pointing at the node/diagram that
     should contain it instead of a rack.
   One of the two placements is required — a device with neither is not a valid create body per the
   vendor's own documented shape. Optional attributes on the same call: `peak_power` (numeric power
   draw), `weight` (numeric), and `status` (a free-text operational-state string, e.g. an "online" or
   "installed" value the caller's environment already uses — NetTerrain does not appear to constrain
   this to a fixed enumeration in the sources retrieved). As with racks, never include an `href` on a
   create body. A successful create returns 201 with the new device object; treat presence of an
   assigned `href`/id in the response as the create-confirmed signal.
6. **Read a device or rack.** Fetch a single record by its numeric id, or list the collection with
   optional pagination (`page`, `per_page`, `offset`) and attribute filters (e.g. filter the collection
   down to a matching `name`). By default, related objects in the response (parent rack, type, mounted
   sub-resources) appear only as `href` stubs — pass the `expand` parameter (a specific child-resource
   name, or an all-children option) to inline their full data instead of stub links, and
   `show_child_collections` to include basic collection metadata for unexpanded child collections
   rather than a bare stub. Treat a 200 response as success and a 404 as "record does not exist."
7. **Update a device or rack's fields.** Submit an update call scoped to the target record's id,
   carrying that record's own `href` (required on update, unlike create) plus every field being
   changed. Renaming, changing capacity/operational attributes, and re-mounting a device to a
   different rack container (by supplying a new `parent_rack_container` href and `container_position`)
   all go through this same call shape. Treat 200 as success, 400 as a rejected/empty body, and 404 as
   "record does not exist."
8. **Assign or reassign a device's rack-unit position.** This is the same update call as Step 7,
   scoped to `parent_rack_container` and `container_position` — NetTerrain does not expose a separate
   mount/unmount endpoint. **Stop and confirm with the operator before submitting a remount or
   dismount against a device that is already reporting an "online"/in-service status** — moving a live
   asset's recorded position is a change to production placement data, not a cosmetic edit, and should
   not be applied silently.
9. **Dismount a device from its rack** by submitting an update whose only meaningful field is
   `container_position` set to the documented negative sentinel value (`-1`) — this clears the rack
   mount without deleting the device record itself. Apply the same operator-confirmation gate as Step
   8 before submitting this against an in-service device.
10. **Delete a device or rack.** **Stop and confirm with the operator before submitting a delete call**
    — this is destructive and, per the vendor's own guidance, verified only by a subsequent read
    returning 404; there is no documented soft-delete or undo. Submit the delete against the record's
    id with no body. Treat 200 as success; if the calling tool needs positive confirmation beyond the
    status code, follow up with a read on the same id and expect 404.
11. **Handle failures verbatim.** Beyond the specific cases already called out (missing type
    reference, missing placement, href included on a create body, missing record), the sources
    retrieved for this skill do not document a stable error-body schema or vendor-specific error
    strings for create/update/delete failures — report FAILED with the underlying response's actual
    status code and body rather than inventing a cause.

## Patterns

- **Devices and racks are typed views over one generic node model.** Both object types share the
  underlying `base_node`/`parent_diagram` placement mechanism used for non-rack-mounted objects; a
  rack-mounted device instead anchors through `parent_rack_container` + `container_position`, not
  through `base_node`. Don't mix the two placement mechanisms on the same create/update call.
- **`href` presence is what distinguishes create from update payloads.** Its absence is required on
  create (present → 409 conflict) and its presence is required on update (identifies which existing
  record is being changed).
- **Capacity totals vs. capacity consumption are different fields.** `power`/`max_weight` (settable)
  describe what the rack can hold; `power_used`/`weight_used`/`available_rack_units` (read-only,
  server-computed) describe current consumption — never submit the latter set on a write.

## Known limitations

- No power-circuit-level assignment object is documented in the sources retrieved for this skill —
  only rack-level power capacity/consumption totals. If a caller needs discrete circuit-to-device
  mapping, check the target instance's own Swagger definition for a circuit-assignment field before
  assuming this procedure covers it; as documented today it does not.
- Does not cover cabling/link records, cards/slots/ports sub-objects, the generic `nodes`/`node_types`
  collections, or the `hierarchy`/`search` endpoints exposed alongside `devices`/`racks` in the WAPI.
- Whether anti-forgery/request-verification headers are enforced on write calls is instance-specific
  configuration (`ValidateAntiForgeryToken`), not a fixed platform behavior — confirm against the
  target instance's own Swagger definition rather than assuming either way.
- Status-value vocabulary for the `status` field is not constrained to a documented fixed set in the
  sources retrieved — treat it as a free-text field matching whatever operational-state values the
  target environment already uses.

## Tools

| Operation | Description | Category |
|---|---|---|
| Token exchange | Exchange credentials for a bearer access token used on write calls | Authentication |
| Device type / rack type lookup | Resolve an existing type record's href before create | Nodes / Types |
| Devices → Create | Create a new device, mounted or unmounted | Nodes / Devices |
| Devices → Get / List | Read one device or a filtered/paginated device collection | Nodes / Devices |
| Devices → Update | Change device fields and/or rack-unit mount position | Nodes / Devices |
| Devices → Delete | Remove a device record | Nodes / Devices |
| Racks → Create | Create a new rack container | Nodes / Racks |
| Racks → Get / List | Read one rack or a filtered/paginated rack collection | Nodes / Racks |
| Racks → Update | Change rack fields (name, type, capacity limits) | Nodes / Racks |
| Racks → Delete | Remove a rack record | Nodes / Racks |

## Verification checklist

- [ ] A bearer access token (not Basic auth) was used for every create/update/delete call
- [ ] Device-type/rack-type references were resolved against the existing type library before create,
      not guessed
- [ ] Create payloads carried no `href`; update payloads carried the target record's own `href`
- [ ] A device create/update specified exactly one placement mechanism (rack container + position, or
      parent diagram) — not both, not neither
- [ ] Capacity-consumption fields (`power_used`, `weight_used`, `available_rack_units`) were never sent
      on a write — only capacity-limit fields (`power`, `max_weight`) are settable
- [ ] Any remount, dismount, or delete affecting a device already in an in-service status was confirmed
      with the operator before submission
- [ ] Outcome confirmed via the documented status code (201 create, 200 read/update/delete, 404 missing,
      409 conflict) rather than assumed from the request alone
