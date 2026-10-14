# AWS EC2 — Instance Lifecycle

Launch, check, start, stop, reboot, resize, back up, and terminate an Amazon EC2 virtual machine
instance. Covers the instance and the snapshots or image taken from it. Networks, security groups,
standalone volumes, images as a catalog, Auto Scaling, load balancers, and Spot or capacity purchasing
are out of scope except where an operation below must read or set one on the instance.

Written against the Amazon EC2 API reference (API version 2016-11-15) and the Amazon EC2 User Guide
topics on instance states, stop and start, instance type changes, and termination, checked
2026-10-14. Where the documentation does not say how the API behaves, this file says so instead of
filling the gap.

Assumes an authenticated client for the target AWS account and Region is available. Instances belong to
one Region, so every call must go to the Region that holds the instance.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Launch a new instance:** *Check what a launch depends on* → *Check permissions with a dry run*
  (optional) → *Launch* (gated) → *Wait for the expected state*.
- **Stop or start an instance:** *Read an existing instance* → *Stop* (gated) or *Start* (gated) →
  *Wait for the expected state*.
- **Reboot an instance:** *Read an existing instance* → *Reboot* (gated) → *Wait for the expected state*
  (the instance returns to running with passing status checks).
- **Resize an instance:** *Read an existing instance* → *Resize* (gated once, covers the stop, the type
  change, and the start) → *Wait for the expected state*.
- **Back up an instance:** *Read an existing instance* → *Back up* (gated for an image that reboots) →
  *Wait for the expected state*.
- **Decommission an instance:** *Read an existing instance* → *Back up* if anything must survive →
  *Terminate* (gated) → *Wait for the expected state*.

## Status vocabulary

Every operation ends with exactly one of these. Report it with the evidence (state read, error code).

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A read matched or did not match |
| LAUNCHED, STARTED, STOPPED, RESIZED, TERMINATED | The expected state was read back after the call |
| BACKED_UP | The snapshots are `completed` or the image is `available` |
| REBOOT_QUEUED | The reboot call was accepted. This is the final status for a reboot: the documentation gives no completion signal (see *Reboot*) |
| REJECTED_INVALID_REFERENCE | A launch dependency is missing or mismatched; nothing was called |
| REJECTED_INCOMPATIBLE_TYPE | The requested instance type cannot be applied in place; nothing was changed |
| DECLINED | The operator did not confirm |
| TIMED_OUT | The expected state was not reached within the operator's time limit (the documentation gives none) |
| FAILED | The platform returned an error, or a snapshot or image ended in error or failed. Include the code and message |

## Operations

### Read an existing instance

Binds to: describe_instances, describe_instance_attribute.

Do this before any change to an existing instance. Its state decides what is allowed.

- Read state, instance type, root device type, tenancy, and each volume's delete-on-termination setting
  with the instance read. Where a resize may need it, read the current bandwidth weighting by filtering the
  instance read on that setting (the documented route; whether it is also a returned field is an
  assumption). Read the termination-protection and stop-protection settings with the
  instance attribute read; the instance read does not return them.
- Look up by instance identifier or by filter (state, tag). State names: pending, running,
  shutting-down, terminated, stopping, stopped.
- Never run an unfiltered read: it returns every instance in the Region; the documentation recommends
  paging.
- A recently terminated instance can still appear for under an hour. An invalid identifier returns an
  error. An instance in another account is silently omitted, so an empty result may mean "not yours".
- Success: FOUND, with the facts above. A launch has no instance to read; use *Check what a launch
  depends on*.

### Check permissions with a dry run

Binds to: the write operation itself, sent with the dry-run flag.

Optional, for any write. Send the request with the dry-run flag.

- The platform answers `DryRunOperation` if the caller has the permissions and the call would succeed.
- It answers `UnauthorizedOperation` if not.
- Neither answer changes anything.
- The documentation describes this as a permissions check. Whether it also catches a bad subnet, group,
  or image is not stated (inference: treat it as permissions only), so it is not a substitute for the
  next operation.

### Check what a launch depends on

Binds to: describe_subnets, describe_security_groups, describe_vpcs, describe_images, describe_instance_types, describe_instance_type_offerings.

Read each item before asking the operator to confirm a launch. The platform does reject a bad
reference (`InvalidSubnetID.NotFound`, `InvalidGroup.NotFound`, `InvalidAMIID.NotFound`,
`InvalidVpcID.NotFound`, `InvalidInstanceType`), but checking first puts the problem in front of the
operator before the confirmation. On any failure, report REJECTED_INVALID_REFERENCE naming the item.

- **Subnet:** exists and is `available`. Record its Availability Zone, its network (VPC), and its free
  address count.
- **Network (VPC):** exists and is `available`. If no subnet is given, a default network must exist, or
  the platform fails with `VPCIdNotSpecified`; require a subnet in that case.
- **Security groups:** each exists and belongs to the subnet's network; the platform rejects a group
  and subnet from different networks (`InvalidParameter`). Use group identifiers, not names, outside
  the default network.
- **Image:** exists, is `available`, and its architecture matches the instance type's.
- **Instance type:** offered in the chosen Availability Zone and supports the image's architecture.
- **Key pair,** if named, exists (`InvalidKeyPair.NotFound` otherwise). Instance profiles, if named: no
  describe call was read for them, so the check is skipped (assumption: the platform rejects an unknown
  profile).
- No pre-check for capacity is documented. On `InsufficientInstanceCapacity`, the error text says to reduce
  the count or wait.

### Launch

Binds to: run_instances, create_tags (for tags added later).

Preconditions: the dependency checks passed. An image and an instance type are required, directly or
through a launch template, as are the minimum and maximum counts.

**Stop and confirm with the operator before launching:** each running instance is billed from the moment
it reaches running, with a one-minute minimum. State the instance count, type, subnet, groups, and image.

- Include a client token. A retry with the same token and parameters succeeds without launching again;
  the same token with different parameters fails with `IdempotentParameterMismatch`.
- Without a token the platform generates one; whether a separate retry reuses it is not stated, so
  supply your own.
- If subnet or groups are omitted, the platform uses a default subnet and the default security group.
  State the intended ones instead.
- Add tags for the instance and its volumes at launch.
- The minimum count is all-or-nothing: if it cannot be met, nothing launches. Above the minimum, the
  platform launches up to the maximum it can.
- Launch large fleets in smaller batches.
- Success: the response lists instances; they are usable at `running` (see *Wait for the expected state*).
- Errors: report FAILED with the code. Throttling returns `RequestLimitExceeded`; see Patterns.
- If the operator declines, report DECLINED and make no call.

### Wait for the expected state

Binds to: describe_instances, describe_instance_status, describe_snapshots, describe_images.

A write call returns before the work finishes. Poll with a read until the target is reached.

| Operation | Success state | Failure signal |
|---|---|---|
| Launch, Start | `running`, and system and instance status checks `ok` | Not documented as failure criteria; an immediate `terminated` after launch or `impaired` checks should be reported as evidence (assumption) |
| Stop | `stopped` | Stuck in `stopping` (assumption: the page mentions the state but gives no failure criterion; see *Stop*) |
| Terminate | `terminated` | Stuck in `shutting-down` (assumption: same) |
| Volume snapshots | `completed` | `error` |
| Image | `available` | `failed` |
| Reboot | No documented completion signal. Reading `running` with checks `ok` afterward is weak evidence only (assumption) | None documented |

- The documentation gives no poll interval and no timeout. Use backoff, and report TIMED_OUT after the
  operator's limit; if the operator set none, ask for one rather than guessing.
- By default, status checks cover only running instances; the check values are `ok`, `impaired`,
  `initializing`, `insufficient-data`, and `not-applicable`.
- A read right after a write may lag; see Patterns on eventual consistency.

### Stop

Binds to: stop_instances.

Preconditions: root device is an EBS volume (an instance-store-backed instance cannot be stopped); the
instance is `running`; stop protection is not set (assumption: the pages name the setting but do not describe its effect or the error returned).

**Stop and confirm with the operator before stopping.** Tell them what a stop does:

- It shuts the instance down (a graceful operating system shutdown by default).
- Data in memory and on instance store volumes is lost.
- A public address that was not allocated as an Elastic IP is given up and a new one is assigned at the next start.
- Volumes, the private address, and any IPv6 address are kept. Instance time is not billed while stopped;
  volumes still are.

Options (each is off unless chosen):

- **Hibernate:** saves memory to the root volume, only where the instance is enabled for it. If hibernation cannot complete, a plain stop happens and memory is lost. The
  operator chooses it.
- **Force:** only for an instance stuck in `stopping`. Use only on the operator's explicit request.
- **Skip the graceful shutdown:** risks data integrity. Use only on the operator's explicit request.
- Errors: `IncorrectInstanceState` (not running) and `OperationNotPermitted` (for example protection).
  Report FAILED with the code.
- Success: STOPPED after `stopped` is read.
- If the operator declines, report DECLINED and make no call.

### Start

Binds to: start_instances.

Preconditions: root device is EBS; the instance is `stopped`.

**Stop and confirm with the operator before starting:** billing resumes with a one-minute minimum, and
the instance may move to new hardware and receive a new public address.

- A T3 instance on host tenancy with unlimited CPU credits fails to start until the credit option is
  `standard` or the tenancy changes.
- `InsufficientInstanceCapacity` can also occur on start; the error text for it says capacity may come
  later (retry timing is the operator's call).
- Errors: `IncorrectInstanceState`. Success: STARTED after `running` is read with checks `ok`.
- If the operator declines, report DECLINED and make no call.

### Reboot

Binds to: reboot_instances.

**Stop and confirm with the operator before rebooting.** The operator decides what counts as production.

- Acceptance only means the request was queued. A request aimed at a terminated instance does nothing,
  and a forced reset follows if the guest does not stop in time.
- Final status: REBOOT_QUEUED. The documentation gives no way to confirm the reboot finished. If the
  operator wants evidence, read the instance state and status checks afterward and report what was seen
  as evidence, without calling it confirmation (an instance can read `running` and `ok` both before and
  after the guest restarts).
- If the operator declines, report DECLINED and make no call.

### Resize (change the instance type)

Binds to: stop_instances, modify_instance_attribute, modify_instance_network_performance_options, start_instances, describe_instance_types.

Run these in order. Do not ask for confirmation until step 3.

1. *Read an existing instance*, including stop protection. Reject if the root device is instance store,
   the instance is Spot, or stop protection is set (REJECTED_INCOMPATIBLE_TYPE; assumption, as for *Stop*).
2. Check compatibility with the target type.
   - Readable through the API: processor architecture (compare the instance types) and whether the
     target supports the number of volumes already attached.
   - Ask the operator to confirm, since no bound operation reads them: that the guest has the drivers
     for the new network adapter and enhanced networking, that the virtualization type suits the target,
     and whether the instance belongs to an Auto Scaling group (a group can replace an instance while it is
     stopped, so its scaling processes must be suspended first).
   - If anything is incompatible or unconfirmed, report REJECTED_INCOMPATIBLE_TYPE (or DECLINED). The
     documented route for an incompatible type is to launch a new instance and migrate; not carried out
     here.
3. **Stop and confirm once with the operator** for the whole resize: downtime while stopped and started,
   the *Stop* effects (memory and instance store data lost, public address replaced), and billing at the
   new type's rate.
4. Stop the instance under *Stop*'s preconditions (the confirmation was already given) and wait for
   `stopped`.
5. Change the instance type:
   - Bandwidth first, if needed: when the original type uses configurable network bandwidth and the target
     does not, set the bandwidth weighting to `default` (network performance options call). Check the current
     weighting by filtering the instance read on that setting, and the target type's support by filtering the
     instance-type read on weighting support.
   - Then change only the instance type attribute (one attribute per call).
   - Errors: `InvalidInstanceAttributeValue` (invalid type), `IncorrectInstanceState` (not stopped).
6. Start the instance and wait for `running` with checks `ok`.

If any step after the stop fails, leave the instance in its current state, report FAILED with the code
and the instance's state, and do not retry without the operator.

Success: RESIZED after the read shows the new type with the instance running.

If the operator declines at step 3, report DECLINED; nothing has been changed.

### Back up

Binds to: create_snapshots, create_image.

Two documented routes with different effects. Pick by the operator's goal; ask if unclear.

- **Volume snapshots:** one crash-consistent snapshot per attached volume, consistent across the instance.
  The root or specific data volumes can be excluded. The instance is not stopped or rebooted. Snapshots
  stay in the instance's Region (or the parent Region or same Local Zone or Outpost, where those apply).
- **Image (AMI):** from a running or stopped EBS-backed instance; a name is required (3 to 128 characters).
  **Stop and confirm with the operator before creating an image unless no-reboot is set:** by default the
  instance is rebooted first so buffered data reaches disk. With no-reboot the result is crash-consistent
  and omits data still in memory or buffers.

Success: BACKED_UP only when the snapshots are `completed` or the image is `available`. A snapshot in
`error` or an image in `failed` is FAILED. The documentation reviewed describes no in-place revert of an
instance to a snapshot (assumption: none exists); a restore means creating a volume or launching from an
image.
- If the operator declines, report DECLINED and make no call.

### Terminate

Binds to: terminate_instances, describe_instances, describe_instance_attribute.

Preconditions: read the instance, its volumes' delete-on-termination settings, and its termination
protection. Two pages describe the default differently: the instance-states page says the root volume is deleted and other EBS
volumes are preserved, while the attribute call's page gives the delete-on-termination default as true when
unspecified. Do not state a default; read each volume's setting.

**Stop and confirm with the operator before terminating. Termination is permanent and cannot be undone.**
The confirmation names every instance and lists, per instance, each volume with its delete-on-termination
value, and says instance store data is lost. Back up anything that must survive first.

- Termination protection blocks the call (`OperationNotPermitted`). It cannot be enabled for Spot
  instances. Do not remove protection unless the operator asks for that specifically.
- Several instances in one call: one invalid identifier fails the whole request. Protection on one
  instance blocks the other instances in its Availability Zone; instances in zones with no protected
  instance are still terminated.
- The call is idempotent. The instance passes through `shutting-down` to `terminated` and stays visible
  for about an hour.
- Force tries a graceful shutdown first and, if that does not finish in time, shuts the instance down without flushing the file system. The separate skip-graceful-shutdown option bypasses the graceful step and risks data integrity. Use either only on the operator's explicit request.
- Success: TERMINATED after `terminated` is read.
- If the operator declines, report DECLINED and make no call.

### Change an attribute other than type

Binds to: modify_instance_attribute, describe_instance_attribute.

Not part of the sequences above. Used only when the operator explicitly asks (for example to set or
clear termination protection, stop protection, or shutdown behavior). **Stop and confirm with the
operator**, naming the attribute and its new value; one attribute per call. Some attributes need the
instance stopped (`IncorrectInstanceState` otherwise). Success: read the attribute back with `describe_instance_attribute` and report FOUND with the new value as evidence; report FAILED with the code if the platform refused.
- If the operator declines, report DECLINED and make no call.

## Patterns

- **Accepted is not done.** Launch, stop, start, terminate, and snapshot calls return before the state
  changes. Read until the target is reached; do not infer success from the call's return.
- **Eventual consistency.** A read right after a write may lag, and may even report the instance as not
  found (`InvalidInstanceID.NotFound`). Retry the read after a short wait before calling it an error.
- **Throttling.** Request-rate and resource-rate limits apply; `RequestLimitExceeded` means retry with
  exponential backoff and smaller batches.
- **Billing by state.** Instances are billed while running (and while stopping if hibernating), not while
  stopped or terminated. Volumes and Elastic IP addresses keep incurring charges in every state.
- **Shutdown from inside the guest.** The shutdown-behavior attribute decides whether an operating system
  shutdown stops (default) or terminates the instance; read it before relying on an in-guest shutdown to
  stop only. An in-guest shutdown always terminates an instance-store-backed instance.
- **Tags** can be set at launch for the instance, its volumes, and a few related resources, or later on
  any resource through a separate tagging call.

## Known limitations

- Covers the instance lifecycle only; networks, security groups, Elastic IPs, standalone volumes, images
  as a catalog, Spot and Reserved capacity, Auto Scaling, and load balancers are not covered.
- Migration to a new instance type when the change is not compatible is only named, not carried out.
- The regional endpoint form and the credential model are not defined here; the assumed client supplies
  them.
- **Terminating an instance cannot be undone,** and any volume set to delete with it is deleted too.

## Tools

| Operation | Description | Category |
|---|---|---|
| describe_instances | Read instances by identifier or filter, with volume settings | Read |
| describe_instance_attribute | Read one instance attribute, such as protection or shutdown behavior | Read |
| describe_instance_status | Read system and instance status checks | Read |
| describe_subnets | Read subnets (state, zone, network, free addresses) | Read |
| describe_security_groups | Read security groups and their network | Read |
| describe_vpcs | Read networks (state, default flag) | Read |
| describe_images | Read an image's state and architecture | Read |
| describe_snapshots | Read snapshot state | Read |
| describe_instance_type_offerings | Read instance types offered in a location | Read |
| describe_instance_types | Read an instance type's supported architectures | Read |
| run_instances | Launch instances | Write (gated) |
| start_instances | Start stopped instances | Write (gated) |
| stop_instances | Stop or hibernate instances | Write (gated) |
| reboot_instances | Queue a reboot | Write (gated) |
| modify_instance_attribute | Change one instance attribute (type; protection only on request) | Write (gated) |
| modify_instance_network_performance_options | Set the bandwidth weighting (used to reset to default before a type change) | Write (gated through *Resize*) |
| create_snapshots | Snapshot the instance's volumes together | Write (no effect on the running instance) |
| create_image | Create an image from an instance | Write (gated unless no-reboot) |
| terminate_instances | Terminate instances | Write (gated) |
| create_tags | Tag existing resources | Write (no effect on the running instance) |

## Verification checklist

- [ ] The Region and account match the instance being acted on
- [ ] An existing instance was read before any change to it (state, root device type, protection)
- [ ] A launch's subnet, network, security groups, image, and instance type were each read and shown to
      exist and fit together before the operator was asked to confirm
- [ ] The operator confirmed before every launch, start, stop, reboot, resize, image that reboots,
      attribute change, and terminate
- [ ] A launch carried a client token and tags
- [ ] A resize passed the compatibility checks before the single confirmation and ended running with
      checks `ok`
- [ ] Every write was followed by a read that reached the expected state, or ended in TIMED_OUT or FAILED
- [ ] A backup ended in `completed` or `available` before BACKED_UP was reported
- [ ] A termination confirmation listed each volume's delete-on-termination value
