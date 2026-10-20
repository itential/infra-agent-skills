# NetBox — DCIM Device Asset & Rack Procedure

Create, read, update, or delete a device record and a rack record in NetBox's DCIM app, including
placing a device at a rack-unit position. Covers the `devices` and `racks` object types only. Does not
cover cables, interfaces, power feeds/panels, modules, device or rack type definitions, or sites and
locations as managed objects, and does not cover NetBox IPAM — see `ipam-allocation` (`netbox/`) for
that. Assumes an authenticated tool for the NetBox REST API with add/view/change/delete permission on
`dcim.device` and `dcim.rack` is already available to the calling agent.

Sources (see `endpoints.md` for the literal wiring):
- NetBox Labs, "REST API" (NetBox documentation), https://netboxlabs.com/docs/netbox/integrations/rest-api/,
  retrieved 2026-10-19.
- NetBox Labs, "Device" model page, https://netboxlabs.com/docs/netbox/models/dcim/device/, retrieved
  2026-10-19.
- NetBox Labs, "Rack" model page, https://netboxlabs.com/docs/netbox/models/dcim/rack/, retrieved
  2026-10-19.
- Secondary source: the NetBox OpenAPI spec and Studio Projects in the `itential/assets` repository
  (Itential-authored, not vendor documentation). Used only to scope the operations and to confirm which
  fields are required on create and writable; those items are marked "per assets spec" below and should
  be confirmed against the target instance's own published API schema (its path is in `endpoints.md`).

## Operational procedure

1. **Establish credentials and base path.** Every call is rooted at the instance's own API base path
   (see `endpoints.md`). The instance accepts a bearer-style token (current token format) or the older
   plaintext token scheme; use whichever the instance issued and confirm the write permissions on it
   before building requests.
2. **Resolve prerequisite references.** A device needs an existing device type, role, and site; a rack
   needs an existing site. NetBox lets a related object be referenced by numeric id or by a set of
   attributes that uniquely identify it. Prefer the id after looking the object up; if the lookup
   returns zero or more than one match, stop and report REJECTED_AMBIGUOUS_REFERENCE rather than
   guessing.
3. **Create a rack.** Submit a create with the rack name and site (required per assets spec), plus
   optional location, status, height in rack units, starting unit, and descending-units flag. Rack names
   must be unique within their location. Confirm success from the returned record carrying an id.
   NetBox's docs say rack-type assignment becomes required in a future major version; if the target
   instance rejects a create for a missing rack type, look one up and retry once.
4. **Create a device.** Submit a create with device type, role, and site (required per assets spec),
   plus optional name, rack, position, face, status, serial, and asset tag. Names, when set, must be
   unique within the site and tenant. To rack-mount, supply the rack together with the base rack unit
   and the mounting face; a multi-unit device is addressed by the lowest-numbered unit it occupies. A
   device with no rack is simply unmounted. Confirm success from the returned record.
5. **Read.** Fetch one record by id, or list with filters (name, site, rack, status) and offset
   pagination. The list response wraps records in a `results` list with `count`, `next`, `previous`.
   Request the brief form when only identity is needed.
6. **Update.** Use a partial update carrying only changed fields. A full replacement requires every
   mandatory field and is easy to get wrong; avoid it. Moving a device means changing its rack, position
   and face together. Supplying a conditional-update precondition (the entity tag from the earlier
   read) guards against concurrent edits; a mismatch is reported as a conflict.
7. **Delete.** Confirm with the operator first when the device's status indicates it is in service, or
   when a rack still holds devices (see Known limitations). A delete returns no content on success;
   verify by a follow-up read returning not-found.
8. **Bulk changes.** Bulk create, update and delete are all-or-none; a single invalid object fails the
   whole request. Never batch destructive deletes without the same confirmation gate as step 7.

## Patterns

- **References accept ids or identifying attributes.** Use the attribute form only when the attributes
  identify exactly one object.
- **Status is an instance-configurable vocabulary.** The docs say additional choices can be defined per
  instance; read the instance's own choices rather than hard-coding values.
- **Write responses are the confirmation signal.** A returned id on create, a 200 on update, a 204 on
  delete.

## Known limitations

- Documented behavior of deleting a rack that still contains devices is not stated in the pages
  retrieved; check the target instance before assuming it is blocked or cascades. Not verified.
- Rack field validation rules (height, starting unit, descending units) are not detailed in the model
  page; field names come from the assets spec only.
- Which status values exist by default is not listed in the docs retrieved.
- Not verified against a live instance.

## Tools

| Operation | Description | Category |
|---|---|---|
| Device lookup | Resolve device type, role, site references | Prerequisites |
| Racks → Create / Get / List / Update / Delete | Manage rack records | DCIM / Racks |
| Devices → Create / Get / List / Update / Delete | Manage device records and rack placement | DCIM / Devices |
| Bulk write | All-or-none multi-object create/update/delete | DCIM |

## Verification checklist

- [ ] Prerequisite references were resolved to exactly one object before create
- [ ] Rack placement supplied rack, base unit and face together, or none of them
- [ ] Updates were partial and carried only changed fields
- [ ] In-service device deletions and bulk deletes were confirmed with the operator
- [ ] Outcome confirmed from the response status/record, not assumed
