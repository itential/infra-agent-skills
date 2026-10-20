# Morpheus — Instance Lifecycle

Create, read, stop, start, resize, snapshot, and delete an instance through the Morpheus API. Morpheus is
a management layer over other clouds and hypervisors, so an instance here may sit on VMware, AWS, Azure,
Google, and others. Clouds, groups, layouts, plans, networks, and policies are out of scope except where a
step must reference one.

Written against the Morpheus API reference pages listed in `endpoints.md`, retrieved 2026-10-19. The
pages give request shape but little behavior, so this file says "not documented" where the pages are
silent instead of filling the gap.

Assumes an authenticated Morpheus API client (a bearer token) is available.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Create an instance:** *Read an existing instance* (name free) → *Create* (gated) → *Wait for the
  expected state*.
- **Stop or start:** *Read an existing instance* → *Stop* (gated) or *Start* (gated) → *Wait for the
  expected state*.
- **Resize:** *Read an existing instance* → *Resize* (gated) → *Wait for the expected state*.
- **Snapshot:** *Read an existing instance* → *Snapshot* → *Wait for the expected state*.
- **Decommission:** *Read an existing instance* → *Snapshot* if anything must survive → *Delete* (gated) →
  *Wait for the expected state*.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A read matched or did not match |
| CREATED, STARTED, STOPPED, RESIZED, DELETED | The expected state was read back |
| SNAPSHOT_REQUESTED | The snapshot call returned process identifiers |
| NOT_COVERED | The operation has no counterpart in the pages reviewed (revert, restart) |
| DECLINED | The operator did not confirm |
| TIMED_OUT | The expected state was not reached within the operator's time limit |
| FAILED | The platform returned an error. Include its message and any validation errors |

## Operations

### Read an existing instance

Binds to: get_instance, list_instances.

- The read returns the instance with its cloud, group, plan, volumes, interfaces, and servers, and
  timing fields for status changes (a status date, percent, and estimated completion).
- The set of status values is not documented in the pages read. Report the returned value verbatim and
  do not normalize it.
- One instance can have several servers; actions affect all of them.
- Success: FOUND.

### Create

Binds to: create_instance.

Required by the documented request: an instance name, a group, an instance type, a layout, and a plan,
plus a cloud-specific `config` object. Volumes and network interfaces are also sent. Their exact form
depends on the cloud the instance lands on; take it from that cloud's entry, which this file does not
carry. Creating the group, layout, plan, or network is out of scope.

**Stop and confirm with the operator before creating:** state name, group, cloud, instance type, layout,
plan, volumes, and networks. The platform may apply approval or policy rules (a sample read showed a
"denied" status); the pages do not describe them.

- No idempotency token is documented: do not blindly retry a timed-out create. Read by name first.
- Success: CREATED once the instance reads in a running state. Report the status text as read.
- If the operator declines, report DECLINED and make no call.

### Stop

Binds to: stop_instance.

**Stop and confirm with the operator before stopping.**

- By default the call stops the service in the instance's containers and also stops the underlying
  server (the server flag defaults to true). Setting it to false stops only the service.
- A force flag performs a hard power-off with no graceful shutdown of the guest; use it only after a
  further confirmation, and say so to the operator.
- A flag can mute monitoring alerts during the stop.
- Success: STOPPED once the read shows a stopped state. If the operator declines, report DECLINED.

### Start

Binds to: start_instance.

**Stop and confirm with the operator before starting.** The server flag decides whether the underlying
server starts too; when unset only the service starts (note this differs from stop's default; pass the
flag explicitly). Success: STARTED. If the operator declines, report DECLINED.

### Resize

Binds to: resize_instance.

**Stop and confirm with the operator before resizing,** naming the new plan or custom values.

- The body names the instance and the target plan, with optional custom CPU, cores per socket, and memory,
  volume growth in GB, storage controllers, and network interface changes.
- A force flag overrides a restriction that blocks resizing when snapshots exist; the pages do not say what
  happens to those snapshots. Do not set it without telling the operator and getting a further confirmation.
- Whether the instance must be stopped, and whether approval applies, is not documented. Report what the
  platform returns.
- A flag that deletes original volumes applies to Amazon only; leave it off unless the operator asks.
- Success: RESIZED once a read shows the new values.

### Snapshot

Binds to: snapshot_instance.

- Optional body: name (generated from the server name and time if omitted), description, a memory flag
  (VMware and a few other provision types only), and an export flag.
- Returns process identifiers; an instance with several servers yields one process each. Poll the
  instance, not the identifiers (the pages give no process read; see Known limitations).
- A revert operation is not in the pages reviewed. Report NOT_COVERED if asked. Do not assume one.
- Success: SNAPSHOT_REQUESTED.

### Delete

Binds to: delete_instance.

**Stop and confirm with the operator before deleting.** Deletion cannot be undone. Tell the operator
what each flag will do before sending it:

- Volumes are kept only if the preserve-volumes flag is set; a separate remove-volumes flag deletes them.
  The pages list both with defaults of off, so the result of sending neither is not stated. Set the
  intended one explicitly.
- Backups are kept only if the keep-backups flag is set (default off, so backups may go with the instance).
- Floating addresses are released by default.
- A force flag attempts deletion when normal removal fails; use it only after a further confirmation.
- Success: DELETED once a read returns not found. If the operator declines, report DECLINED.

### Wait for the expected state

Binds to: get_instance.

Writes return before the work ends. Poll the instance read until its state matches the target or a
documented error appears. The pages give no status vocabulary, poll interval, or timeout. Use backoff
and report TIMED_OUT after the operator's limit; if none was set, ask for one.

## Patterns

- **Service versus server.** Stop and start default differently; always pass the server flag explicitly.
- **Force flags are separate decisions.** Stop, resize, and delete each have one with different effects.
- **Delete flags decide data loss.** Volumes and backups survive only with explicit flags.
- **Cloud-specific create.** The same call takes different config per target cloud.

## Known limitations

- Covers the instance lifecycle only; clouds, groups, layouts, plans, networks, policies, and approvals
  are not covered.
- No restart, revert, or process-status read was reviewed. Do not improvise them.
- The status value set is undocumented in the pages read.
- Credential handling is not defined here.
- **Deleting an instance cannot be undone.**

## Tools

| Operation | Description | Category |
|---|---|---|
| get_instance, list_instances | Read instances | Read |
| create_instance | Create an instance | Write (gated) |
| stop_instance | Stop service and optionally the server | Write (gated) |
| start_instance | Start service and optionally the server | Write (gated) |
| resize_instance | Change plan, CPU, memory, volumes, NICs | Write (gated) |
| snapshot_instance | Snapshot an instance | Write (no effect on the running instance) |
| delete_instance | Delete an instance | Write (gated) |

## Verification checklist

- [ ] The instance and its cloud were read before any change
- [ ] The operator confirmed before every create, stop, start, resize, and delete
- [ ] Stop and start were sent with the server flag stated explicitly
- [ ] No force flag was sent without a further confirmation
- [ ] A delete named what happens to volumes, backups, and addresses before it was confirmed
- [ ] Every write was followed by a read that reached the target, or ended in TIMED_OUT or FAILED
- [ ] No revert or restart was improvised
