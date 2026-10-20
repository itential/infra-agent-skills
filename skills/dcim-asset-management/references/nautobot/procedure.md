# Nautobot — DCIM Device Asset & Rack Procedure

Create, read, update, or delete a device record and a rack record in Nautobot's DCIM app, including
placing a device at a rack-unit position. Covers the `devices` and `racks` object types only. Does not
cover cables, interfaces, power objects, modules, device types, or locations as managed objects, and
does not cover Nautobot IPAM — see `ipam-allocation` for that. Assumes an authenticated
tool for the Nautobot REST API with permission on the DCIM device and rack objects is already available
to the calling agent.

Sources (see `endpoints.md` for the literal wiring):
- Nautobot documentation, "REST API Overview",
  https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/rest-api/overview/,
  retrieved 2026-10-19.
- Nautobot documentation, "Device" and "Rack" data model pages,
  https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/device/ and
  .../rack/, retrieved 2026-10-19.
- Secondary source: the Nautobot OpenAPI spec and Studio Project in the `itential/assets` repository
  (Itential-authored, not vendor documentation), used only to scope operations. Marked "per assets
  spec" where used; confirm against the target instance's own API schema.

## Operational procedure

1. **Establish credentials and base path.** Calls are rooted at the instance's API base path (see `endpoints.md`). Write
   calls authenticate with a token header (see `endpoints.md`). Send an explicit API version on the
   request when the instance serves more than one.
2. **Resolve prerequisite references.** A device requires a location, a role, a status and a device
   type, all of which must already exist; a rack requires a location, a rack type, a status, a name and
   a height. Related objects can be referenced by primary key (UUID), by a natural key, or by a set of
   identifying attributes. Prefer the UUID after lookup; if a lookup is ambiguous or empty, stop and
   report REJECTED_AMBIGUOUS_REFERENCE.
3. **Create a rack.** Submit name, location, status, type and height (per the model page); optional
   facility id, serial, asset tag, group and tenant. Confirm success from the returned record.
4. **Create a device.** Submit location, role, status and device type, plus optional name, rack,
   position, face, serial and asset tag. A device occupies the lowest-numbered rack unit it uses; a
   full-depth device blocks the opposite face in the same units. Name uniqueness is enforced by the
   application according to the instance's `DEVICE_UNIQUENESS` setting (unique within location and
   tenant, globally unique, or none), so a duplicate name may or may not be rejected; read the setting
   from the operator when it matters. Confirm success from the returned record.
5. **Read.** Fetch one record by UUID or list with filters and offset pagination. Lists return
   `count`, `next`, `previous`, `results`. The depth parameter controls how much of each related object
   is inlined; use the default minimal form unless nested data is needed.
6. **Update.** Use a partial update with only changed fields. A full replacement needs every mandatory
   field. Moving a device means changing rack, position and face together.
7. **Delete.** Confirm with the operator first when the device's status indicates it is in service or
   when a rack still holds devices. Verify by a follow-up read returning not-found.
8. **Bulk changes.** Bulk create, update and delete are all-or-none. Bulk deletes require the step 7
   confirmation.

## Patterns

- **Identifiers are UUIDs, not integers.**
- **Uniqueness is configurable.** Do not assume a duplicate device name is rejected.
- **Status is an object reference, not free text.** Look the status up first.

## Known limitations

- The rack page retrieved does not state validation rules for starting unit or descending units, nor
  required-field behavior beyond name, location, type, status and height. Not verified.
- Behavior of deleting a rack that still contains devices is not stated in the pages retrieved. Not
  verified.
- Whether a status must be sent as a UUID or a name on a write is not stated in the pages retrieved;
  the reference forms above are all documented, but confirm which the instance accepts.
- Not verified against a live instance.

## Tools

| Operation | Description | Category |
|---|---|---|
| Reference lookup | Resolve location, role, status, device type, rack type | Prerequisites |
| Racks → Create / Get / List / Update / Delete | Manage rack records | DCIM / Racks |
| Devices → Create / Get / List / Update / Delete | Manage device records and rack placement | DCIM / Devices |
| Bulk write | All-or-none multi-object write | DCIM |

## Verification checklist

- [ ] Prerequisite references resolved to exactly one object before create
- [ ] Rack placement supplied rack, position and face together, or none
- [ ] Updates were partial
- [ ] In-service deletions and bulk deletes were confirmed with the operator
- [ ] Outcome confirmed from the response, not assumed
