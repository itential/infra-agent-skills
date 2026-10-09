# Zscaler ZIA cloud firewall rule management

Manage a ZIA cloud firewall rule and complete the publisher's separate configuration-activation step.

Sources: [cloud firewall tools](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zia/cloud_firewall_rules.py), [rule helpers](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/common/zia_helpers.py), [activation tools](https://github.com/zscaler/zscaler-mcp-server/blob/master/src/zscaler_mcp/tools/zia/activation.py), [confirmation guide](https://github.com/zscaler/zscaler-mcp-server/blob/master/docs/guides/mcp-protocol.md), current master, retrieved 2026-10-09. Bindings and validation constraints are in [endpoints.md](endpoints.md).

## Common Sequences

- Inspect: List rules → Read rule.
- Create: List rules → Prepare payload → Confirmed create → Read rule → Confirmed activation → Read activation status.
- Update/delete: Read rule → Prepare payload → Confirmed update or Confirmed delete → Confirmed activation → Read activation status.

### List rules

The list operation can filter by rule-name substring. A successful result is the returned matching collection; an SDK error remains a failed query. The wrapper publishes no explicit pagination controls, so it does not establish additional page or rate-limit guarantees.

### Read rule

An explicit rule identifier selects the complete rule and references. Success is a record with the requested ID. An error remains the platform error; names are not silently substituted for identifiers.

### Prepare payload

The create schema requires a name and action. Existing reference IDs and match criteria are supplied in the approved advanced payload. Placement and administrative rank are distinct values. The publisher defaults a new rule to the first position and its lowest administrative rank; an omitted placement can therefore put a rule above existing rules. The approved payload includes these defaults or explicit alternatives. An update is documented as replacement: the intended full rule fields, including those preserved from the current record, are part of the replacement. Invalid rank/order values fail locally.

### Confirmed create

Adding a firewall rule changes staged enforcement configuration: stop and confirm with the operator before proceeding. The enabled write tool submits the approved payload. Success is the returned rule record and matching readback, including the assigned ID, action, enablement, scope and placement. An error remains failure; an ambiguous create outcome requires inspection before another create.

### Confirmed update

Replacement can remove omitted settings and change traffic decisions: stop and confirm with the operator before proceeding. The operation addresses the selected ID and carries the intended replacement payload. Success is the updated record; a subsequent read confirms the requested fields. The update remains staged until activation.

### Confirmed delete

Deleting the rule removes enforcement configuration: stop and confirm with the operator before proceeding. The publisher's native human prompt or fallback token challenge remains in place. A challenge, cancellation or unanswered prompt is not deletion. The completed result must indicate successful removal; SDK errors retain failure. Deletion still requires configuration activation.

### Confirmed activation

Activation applies pending configuration to live enforcement: stop and confirm with the operator before proceeding. The activation operation is not scoped to one rule identifier. Approval covers the pending tenant configuration, including the risk that other pending changes are included. A successful activation response carries the native status; failure does not undo the stored rule change and must remain visible.

### Read activation status

The status read returns the platform's status string. The cited model provides neither an exhaustive status enumeration nor a completion timeout; an unfamiliar or pending status remains unresolved pending platform-specific guidance. The result reports the record outcome and native activation status separately, without claiming traffic behavior was tested.

## Patterns

- Create/update/delete persistence and active enforcement are separate milestones.
- Rule placement is not administrative rank. Defaults can affect other rules' precedence.
- Advanced fields pass through the publisher SDK. A field not established by the installed schema is unverified; plausible names are not sufficient evidence.
- The token fallback cannot prove human participation. The publisher documents stronger client-mediated elicitation and process-bound confirmation state.

## Known limitations

- URL filtering, DLP and other ZIA rule families have different bindings.
- Activation is not a per-rule transaction and the source supplies no universal propagation timeout.
- The procedure requires existing scope-object identifiers; it does not create reference objects.
- No complete HTTP error/rate-limit catalogue is supplied by these wrapper sources. Actual errors remain explicit and any returned retry guidance governs retries.

## Tools

| Operation | Description | Category |
|---|---|---|
| List rules | Retrieve cloud firewall rules | Read |
| Read rule | Retrieve one rule and references | Read |
| Create rule | Stage a new rule | Write |
| Update rule | Stage a replacement rule | Write |
| Delete rule | Remove a rule through confirmation | Destructive |
| Activate configuration | Apply pending ZIA configuration | Activation |
| Read activation status | Retrieve platform activation state | Read |

## Verification checklist

- Rule ID, matching scope, action, enablement, placement and rank match the approved request.
- Replacement fields were preserved intentionally and every mutation retained its gate.
- Delete confirmation was completed by the operator rather than inferred from a token.
- The record result and activation result are both reported; unresolved activation remains unresolved.
