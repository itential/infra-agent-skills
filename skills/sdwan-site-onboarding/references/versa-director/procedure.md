# Versa Director — Branch Device Onboarding from a Post-Staging Template

Onboard a branch edge device (VOS) on Versa SD-WAN through Versa Director: create the device from a
workflow that links it to a device group and its template, bring the physical or virtual device online
through one of the documented activation methods, and confirm Director sees it reachable and in sync.

Written against the Versa Networks documentation pages listed under Sources, all retrieved 2026-10-19.
Where those pages do not say how the platform behaves, this file says so instead of filling the gap.

Assumes an authenticated client for the Director is available (see `endpoints.md`).

## Sources

- Versa Director REST API Overview (docs.versa-networks.com, Director REST APIs section)
- Overview of Configuration Templates (SD-WAN configuration, basic SD-WAN configuration)
- Activate VOS Devices (Branch Deployment, initial configuration)
- Commit Template Modifications (SD-WAN configuration, basic SD-WAN configuration)

## Scope

In scope: creating a branch device through the Director device workflow, the activation methods for
getting the device to its controller, and confirming the result.

Out of scope, each a separate procedure if added later:
- Creating the organization (tenant), device group, device template, or service templates the device
  refers to. They must already exist.
- Removing or replacing a device. The pages above do not document a removal sequence for a workflow
  device, so this file gives none.
- Switch (SD-LAN) management interfaces, uCPE, cloud-connector deployments, and the global
  zero-touch path that depends on the vendor's own staging servers.
- Authoring routing, security, or QoS policy carried by service templates.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Onboard a new branch device:** *Check prerequisites* → *Create the device through the workflow* →
  *Activate the device* (gated when a factory reset is needed) → *Confirm the device* → *Commit template
  changes* (gated; only when the confirm step shows pending template differences).
- **Check a device that was already activated:** *Confirm the device*.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup of the organization, device group, template, or device matched or did not |
| REJECTED_INVALID_INPUT | A pre-check failed (missing prerequisite, name already used, device not in a clean state); nothing was changed |
| DEVICE_CREATED | The workflow create returned success and a read-back lists the device |
| ACTIVATION_STARTED | The activation method was begun; the device has not yet reported in |
| ACTIVATED | The device appears in the Director inventory and its onboarding task completed |
| COMMIT_ACCEPTED | A template commit was submitted; the final outcome is not yet known |
| ONBOARDING_UNCONFIRMED | Calls returned but a final state could not be read, or the reads disagree. Say what each shows |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error or a failure state. Include status code and body |

## Operations

### Check prerequisites

Binds to: read_organization, read_device_group, read_template, query_devices.

- Confirm the organization, the device group, and the post-staging template for that group exist. The
  documentation calls the post-staging template mandatory for creating a device; it holds the full
  configuration that deploys services, while a staging template carries only the connectivity needed to
  reach the controller.
- Query existing devices by the intended name. Whether the workflow rejects a duplicate name or updates
  the existing device is not stated in the sources (unverified); treat an existing device of the same
  name as an existing device, not a new one, and stop for the operator.
- Leave the default order in which the organization's datastore template and the main template are
  listed untouched. The documentation warns that reversing it lets the datastore template overwrite
  objects in the main template.
- Success: FOUND for each prerequisite and no existing device of that name. Otherwise
  REJECTED_INVALID_INPUT or NOT_FOUND, and stop.

### Create the device through the workflow

Binds to: create_workflow_device, read_workflow_device.

- The device workflow works like a configuration wizard: it creates the infrastructure objects the
  device needs and links the device to its device group. It sets up an initial configuration; the
  documentation says it cannot maintain an existing one, so later changes go through the template
  configuration screens, not a re-run of the workflow.
- Submit the device name, its organization and device group, and the workflow inputs the template
  requires (interfaces, addressing, and similar). The accepted request body is published only in the
  Director's own API documentation page, so the field list is unverified here; read it from the target
  Director before building the request (see `endpoints.md`).
- The workflow's review screen offers Clean & Recreate, Redeploy, and Save. Clean & Recreate deletes the
  device's earlier configuration objects first and is destructive: **stop and confirm with the operator
  before choosing it.** For a first-time create, Save is the non-destructive choice; the documentation
  does not say whether the REST create implies any of the three (unverified).
- Success: a read-back lists the device in its device group. Report DEVICE_CREATED.
- Errors: a validation failure returns an HTTP status and, for the custom APIs, a JSON body with a
  status code, application code, and message. Report FAILED with the body.

### Activate the device

Binds to: generate_activation_url (URL-based method only), query_devices.

The device must reach the controller before Director can manage it. The documentation lists five
methods. Choose by what the operator has on site:

| Method | Use when | Documented preconditions |
|---|---|---|
| Global zero-touch | Device serial numbers were given to the vendor and the vendor staging service is in use | Public controller exists; device powers on with internet access; reboots after each stage |
| URL-based zero-touch | A site administrator will activate on site from a link | Device at factory default; WAN on ports 0 and 1, LAN on ports 2 and 3 (model exceptions exist); ICMP allowed on WAN ports; feature enabled in the device group with a staging controller and VPN profile selected |
| Command-line staging | An operator has console or shell access | Run the staging script on the device with local ID, remote ID, controller address, WAN port, and addressing or DHCP |
| USB drive | Physical access, no network on site yet | Staging parameters file at the drive root; device configuration empty or factory default |
| Cloud-init | Virtual device on KVM, OpenStack, or a cloud | Config passed at instantiation; network setup plus the staging script run on first boot |

- Command-line form, as the page documents it (placeholder values):
  `sudo /opt/versa/scripts/staging.py -l <local-id> -r <remote-id> -c <controller> -w <wan-port-number> -s <ip/mask> -g <gateway>`
  with a DHCP option in place of the static address. The script's own help lists the rest.
- URL-based method: enable it in the device group, select the staging controller and VPN profile,
  optionally set a one-time password, then generate the activation URL for the device. The site
  administrator opens the emailed link on a laptop at the LAN port, confirms the device status light is
  green, and starts activation; with two-factor authentication on, the device is claimed and a
  registration code entered. The device reboots at the end.
- A device whose configuration is no longer empty (the page ties an amber status light to a changed
  configuration) must be factory-reset before URL-based or USB activation, using the device's load-default
  or erase-config-file command. This wipes the device configuration: **stop and confirm with the
  operator before running it.**
- Success: ACTIVATION_STARTED, then see *Confirm the device*.
- Errors: no documented error strings. For URL-based failures the page gives a debugging checklist:
  port 1 is the management NIC, WAN IP on port 2, default gateway reachable through the WAN port, LAN
  port receiving a DHCP address.

### Confirm the device

Binds to: read_tasks, query_devices, read_device_status.

- Director's task list shows whether the onboarding task completed.
- The device should appear in the Director inventory under hardware.
- Before any template commit, the device should read reachable (green) and its services up in the
  appliance view; the documentation says unreachable devices or down services can make a commit fail.
- Success: ACTIVATED when the task completed and the device is in inventory. If the task list or
  inventory cannot be read, or they disagree, ONBOARDING_UNCONFIRMED.

### Commit template changes

Binds to: commit_template.

Whether a new device needs a separate commit after activation is not stated in the sources (unverified);
run this only when the appliance view shows template differences still pending for the device.

- Choose the scope: all associated templates, or only selected templates (release 22.1.1 and later).
- Review the configuration differences before committing.
- Merge mode: automatic merge is the documented recommendation; manual merge moves configuration blocks
  by hand. **Overwrite replaces the device's existing configuration entirely, and the optional reboot and
  clear-sessions options disrupt traffic: stop and confirm with the operator before submitting with
  either.**
- Submit now, or schedule it. Success: COMMIT_ACCEPTED; confirm completion in the task list. The
  documentation describes no rollback.

## Patterns

- A workflow creates initial configuration only; ongoing edits belong to the template screens.
- Do not reorder the datastore and main template list (see *Check prerequisites*).
- Activation methods other than global zero-touch work only against a factory-default device.

## Known limitations

- No removal, replacement, or rollback procedure is covered; none is documented in the sources.
- Request and response schemas for the workflow create and the template commit are not published in the
  documentation pages used; they must be read from the Director's own API documentation.
- Duplicate-name behavior, whether REST create implies Clean & Recreate/Redeploy/Save, and whether a new
  device needs a post-activation commit are unverified.
- Rate limits and task-status endpoints are not stated in the sources.

## Tools

| Operation | Description | Category |
|---|---|---|
| read_organization, read_device_group, read_template | Confirm prerequisites exist | Read |
| query_devices, read_workflow_device | List or read devices | Read |
| create_workflow_device | Create a device through the device workflow | Write |
| generate_activation_url | Generate the URL-based activation link for a device (Director UI action; no verified REST call, see `endpoints.md`) | Write |
| read_tasks, read_device_status | Task list and device reachability/service state | Read |
| commit_template | Push template changes to devices | Write (disruptive) |
| Shell session on the device | Run the staging script or factory reset | Transport |

## Verification checklist

- [ ] Organization, device group, and post-staging template confirmed before creating the device
- [ ] No existing device of the same name, or the operator chose how to proceed
- [ ] Clean & Recreate, factory reset, overwrite commit, and reboot/clear-sessions each confirmed with
      the operator before running
- [ ] Device present in the Director inventory and its onboarding task completed
- [ ] Device reads reachable and services up before any commit
- [ ] Outcome reported with this file's status vocabulary
