# Prisma SD-WAN — Branch Site Onboarding from a Site Template

Onboard a branch site on Prisma SD-WAN: choose or build a site template, deploy the site from it,
attach the ION edge device (directly or through a device shell), confirm the site came up, and remove or
release what was created if it must be undone.

Written against the Prisma SD-WAN Administrator's Guide (last revised 2026-08-11) and the Prisma SD-WAN
Unified APIs OpenAPI specification (version label "Latest"), checked 2026-10-14. Where the sources do not
say how the platform behaves, this file says so instead of filling the gap.

Assumes an authenticated API client for the tenant is available. Token handling is described in
`endpoints.md` for reference only.

## Scope

In scope: branch sites deployed from a site template, the device states needed to attach an ION to
that site, and the removal path for a deployment, device, and site.

Out of scope, each a separate procedure if added later:
- Data-center sites, firewall-hosted SD-WAN sites, and virtual ION provisioning. The guide states that
  templates currently cover day-one deployment only and exclude FIPS mode and CloudBlades.
- Editing template variables, importing or exporting template files, and snapshot (YAML) import.
- Building the path, QoS, NAT, or security policy a site template refers to.
- Software upgrades, RMA replacement, and device mode changes on an onboarded site.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Deploy a site when the device is not yet in hand (shell first):** *Look up the template and the
  site name* → *Prepare the site data* → *Check the device inventory* → *Deploy the site* (gated) →
  *Confirm the deployment* → (device arrives, unclaimed) *Assign the device to the shell* (gated) →
  *Verify the site*.
- **Deploy a site with the device serial number supplied:** *Look up the template and the site name* →
  *Prepare the site data* → *Check the device inventory* → *Deploy the site* (gated) → *Confirm the
  deployment* → *Verify the site*. The guide says an available, unclaimed, online device named by serial
  number is configured during the deployment run itself.
- **Build a template from a proven site, then deploy:** *Look up the template and the site name* →
  *Create a template from a reference site* → then either sequence above.
- **Undo an onboarding:** *Verify the site* (to see current state) → *Release the device* (gated) →
  *Delete a device shell* (gated, only if a shell remains) → *Delete the site* (gated). The release
  step has no verified binding (see `endpoints.md`), and no operation here removes circuit labels; if
  either blocks, the sequence stops there and the site cannot be deleted while a device, shell, or WAN
  interface remains. *Remove the deployment* is optional and not a prerequisite: the guide's removal
  flow (unassign, remove circuits, put back in inventory) never mentions deployment records, and the
  site-delete refusals do not list one. Run it only if the operator wants the record discarded.

## Status vocabulary

| Status | Meaning |
|---|---|
| FOUND / NOT_FOUND | A lookup of a template, site, device, or deployment matched or did not |
| REJECTED_INVALID_INPUT | A pre-deploy check failed (missing mandatory variable, duplicate site name, unusable device); nothing was changed |
| TEMPLATE_CREATED | The template create returned success and a read-back shows it |
| DEPLOY_ACCEPTED | The deploy call returned a deployment identifier per site; the final outcome is not yet known |
| SITE_DEPLOYED_SHELL | Deployment reached a final non-failure state and the site holds a device shell with no device attached |
| DEVICE_ASSIGNED | The device took over the site's shell, and the shell no longer appears |
| ONBOARDED | Deployment finished, the device is bound to the site and reads connected, and the site is not reported inactive |
| ONBOARDING_UNCONFIRMED | The calls returned but a final state could not be read, or the reads disagree. Say what each shows |
| REMOVED | The delete or release call succeeded and a re-read no longer shows the object |
| DECLINED | The operator did not confirm |
| FAILED | The platform returned an error or a failure state. Include status and body |

## Operations

### Look up the template and the site name

Binds to: query_templates, read_template, query_sites.

- Query templates and find the one by exact name; read it to capture its site type and identifier.
- Query sites by the intended name. A site with the same name is an existing site, not a new one. The
  platform may update it or reject the deployment (inference: the guide's import screen flags an
  existing site and its day-two text says matching resources are updated; it does not state what the
  deploy call does). See *Deploy the site*.
- Success: FOUND with the template identifier and site type, plus either no site of that name or the
  existing site's identifier. NOT_FOUND for the template means *Create a template from a reference site*
  or stopping.

### Create a template from a reference site

Binds to: read_site, create_template, read_template.

- The guide recommends building a site by hand first, validating it works, and using that proven site as
  the template source. A source site may carry a device shell rather than a live device.
- Submit a unique template name (the guide says duplicates error; the specification limits it to 128
  characters), an optional description (256), the site type (branch for this procedure), and the
  identifier of the reference site.
- Success: the response carries a template identifier; read it back and report TEMPLATE_CREATED.
- The new template starts with a default variable set. Editing variables is out of scope; if the
  operator needs variables beyond the defaults, tell them it is done outside this procedure.
- Errors: name missing, name or description too long, bad site type, or duplicate name: report FAILED
  with the status and error code.

### Prepare the site data

Binds to: read_template.

- Every template requires these variables in the site data: the site name, the ION software version, and
  the first ION serial number; an HA pair also needs the second serial number. The controller rejects
  site data that lacks them. Variable names are listed in `endpoints.md`.
- Gather one data row per site. Check each row against the template's variable list; a variable the
  template defines but the row omits is a gap to resolve before deploying (assumption: the platform may
  reject it or apply the template's static value; the sources do not say which).
- Serial number is optional in the data. If given, that serial is bound to that device for good and cannot
  go to any other device; after deployment it cannot be changed. If omitted, a device shell is created
  and a device of a matching model can be attached afterwards.
- Reject (REJECTED_INVALID_INPUT) any row missing a mandatory variable. Also reject a row whose site name
  repeats another row in the same batch (inference: the guide's import screen shows a duplicate alert
  for repeated names, but does not say the controller refuses them).

### Check the device inventory

Binds to: query_machines, read_machine.

- For each serial number supplied, read the device. For the serial-in-template path the guide expects
  the device to be unclaimed and online at deployment time; a claimed device must first be returned
  to inventory before a different assignment (see *Release the device*).
- A physical device allocated to the tenant shows as unclaimed and offline until it is powered and has
  reached the controller through its controller port, which the guide says needs a DHCP network with
  internet access (a static address can be set through the auxiliary port). A virtual device shows as
  unclaimed and online-restricted.
- Success: each serial is FOUND with its model and state. A serial that is missing from inventory means
  the device is not allocated to this tenant; report REJECTED_INVALID_INPUT or switch that site to the
  shell path with the operator's agreement.

### Deploy the site

Binds to: deploy_template.

**Stop and confirm with the operator before deploying.** Show each site name, the template, whether the
name matches an existing site, and for each site whether a serial number is bound or a shell will be
created. Deployment creates real site and device configuration on the tenant, and a name that matches
an existing site may modify that site.

- If a name matches an existing site, call that out as a possible update of a live site (inference,
  see *Patterns*) and require the operator's explicit confirmation for that site separately.
- After deployment the template can no longer be edited, per the guide; reuse means exporting it,
  changing it, and importing the changed copy (out of scope here).
- If the operator declines, report DECLINED and make no call.
- Submit one data row per site; the request shape is only described as a variable map (see `endpoints.md`).
- Success: a deployment identifier per site (the guide says one job per site); report DEPLOY_ACCEPTED, then
  run *Confirm the deployment*.
- Errors: report FAILED with status and body; the named error codes are in `endpoints.md`.

### Confirm the deployment

Binds to: read_deployment_status, read_deployment, query_sites.

The accepted call only means a job was queued.

- Per site, read the deployment status until it is final. The guide says a few minutes, with per-site
  progress on a job history page; status values and timeouts are undocumented, so read the text as
  returned and ask the operator for a polling limit.
- Read the site by name (it should exist) and its elements (a shell appears if no device was supplied).
- Final without failure and an unattached shell present: SITE_DEPLOYED_SHELL; continue to *Assign the
  device to the shell*. Serial-number path: complete only after *Verify the site*.
- Status reads as a failure: FAILED with the status description.
- Status unreadable or never final: ONBOARDING_UNCONFIRMED with the deployment identifier.

### Assign the device to the shell

Binds to: list_element_shells, assign_device_to_shell, read_element.

**Stop and confirm with the operator before assigning.** The shell's whole configuration is pushed to the
device, after which the shell is gone; a wrong pairing puts the wrong configuration on a branch device.

- Pick the device and the target shell together; the guide requires the device to be an unclaimed one and,
  where the serial was not in the data, to be the same model as the shell. A device already claimed must be
  returned to inventory first (see *Release the device*).
- If the operator declines, report DECLINED and make no call.
- The guide's assign-to-site steps say the assignment occurs in the background; it gives no duration for
  assigning to a shell (its 10-15 minute figure belongs to device replacement, not this step). Poll the
  device and shell and let the operator set a limit.
- Success: the shell no longer exists and the device reads as assigned to the site; report
  DEVICE_ASSIGNED. Continue with *Verify the site*.
- Errors: `ELEMENT_SHELL_NOT_FOUND` or any other code: report FAILED with the status and body.

### Verify the site

Binds to: read_site, read_site_status, query_elements, read_element, read_deployment_status.

- The deployment for each site is final and not failed.
- The site exists and its status is not reported as inactive or disabled; the reason text, if any, is
  reported as returned.
- Each expected element exists, is bound to the site, and reads connected. The guide shows a connected
  device with a green indicator and an offline one in red.
- No leftover shell remains for a device that was supposed to be assigned.
- Report ONBOARDED when all hold. If any read is unavailable or the reads disagree, report
  ONBOARDING_UNCONFIRMED and list each result.

### Remove the deployment

Binds to: read_deployment, delete_deployment.

Optional; not required before deleting a site (see the undo sequence).

**Stop and confirm with the operator before deleting a deployment.** What the call does to the site,
its elements, and the device is not documented (assumption: it may remove only the deployment record,
leaving the site; read the site afterwards to see). Treat it as potentially destructive and permanent.

- If the operator declines, report DECLINED and make no call.
- Success: the call returns the deleted deployment record; re-read the site and its elements and
  report what remains, then REMOVED for the deployment record only.
- Errors: report FAILED with the status and body.

### Release the device

Binds to: read_element, unassign_device, declaim_device.

**Stop and confirm with the operator before releasing a device.** Unassigning removes an element from a
live site and can interrupt its service; putting it back in inventory returns it to unclaimed and reboots
it.

- Detach the device from its site. If the platform reports that a WAN interface still references the
  element, circuit labels must be removed from its WAN interfaces first, as the guide describes. No
  operation here does that: stop, tell the operator it is done in the management console, and re-read
  afterwards.
- To make the device claimable elsewhere, put it back in inventory; the guide says it moves from the
  claimed list to the unclaimed list and reboots. Returning it to the vendor is a separate, later step
  the guide describes and is out of scope.
- If the operator declines, report DECLINED and make no call.
- The specific calls for unassign and put-back-in-inventory are not documented as such in the
  specification; see `endpoints.md` for the unverified bindings.
- Success: a re-read shows the device unassigned (and unclaimed, if put back); report REMOVED.

### Delete a device shell

Binds to: list_element_shells, delete_element_shell.

**Stop and confirm with the operator before deleting a shell.** The shell holds the configuration meant
for a device; deleting it discards that configuration (assumption: permanent).

- List the site's shells; delete only the shell the operator named, and only if it is unattached.
- If the operator declines, report DECLINED and make no call.
- Success: the call returns the deleted shell; a re-list no longer shows it; report REMOVED.
- Errors: report FAILED with the status and body.

### Delete the site

Binds to: read_site, delete_site.

**Stop and confirm with the operator before deleting a site.** A deleted site's configuration is not
documented as recoverable (assumption: permanent).

- Prerequisites implied by the platform's refusal errors: no element or element shell remains at the site,
  no WAN interfaces or their link-quality settings remain, and no service endpoint remains. Release
  devices and delete shells first; WAN interfaces, link-quality settings, and service endpoints
  have no removal operation here, so if the refusal names one, the sequence stops and the operator
  clears it elsewhere.
- If the operator declines, report DECLINED and make no call.
- Success: the call returns the deleted site; a re-query no longer lists it; report REMOVED.
- Errors: a refusal naming an invalid state, a WAN, an element or shell, or a service endpoint means the
  site is not empty; report FAILED with the code and what to detach, and do not retry blindly.

## Patterns

- **Shell versus serial.** With a serial number in the data and the device unclaimed and online, the
  device comes up in the deployment. Without one, or if the device is unreachable at that moment,
  a shell holds the configuration and the device is attached later. An unreachable device is not an
  error.
- **Unclaimed is the starting state for a shell assignment.** Only unclaimed hardware may be a shell's
  target (the guide); do not claim a device before attaching it to a shell, since it would have to be put
  back in inventory first.
- **Same-name deploy may be an update (inference).** Basis: the guide's import screen marks a name that
  matches an existing site, and its day-two text says matching site and device resources are updated while
  non-matching ones create a new site or shell. The deploy call's own behavior is not stated, so treat it
  as possible and gate it. Day-two updates leave software version and serial unchanged, cannot rename an
  assigned device, and cannot switch layer 2 or layer 3 mode unless the device is unassigned first.
- **Source conflict.** The guide lists a pending shell under claimed devices yet says only unclaimed devices
  can be assigned to a shell; the unclaimed rule is followed here.
- **Stuck claim recovery.** If a device is stuck mid-claim or in the claim-failed state, the guide offers a
  recover action on the device from either inventory list, and a put-back-in-inventory then
  re-assignment to a shell as the alternative. Each is a device-affecting action and needs the same
  confirmation.
- **Rejected right after sign-in.** See `endpoints.md` (authenticate) before treating it as a permission gap.
- **Virtual devices.** The guide warns that a virtual ION must be retired through the vendor's return or
  replacement flow before its host instance is removed from its host, or the system is left inconsistent.

## Known limitations

- Branch sites from a site template only; day-one deployment. FIPS mode and CloudBlades are not supported by
  templates in the guide's current description.
- Claiming a device on its own and assigning a claimed device directly to a site are described in the guide
  but not bound here; the specification names no verified route.
- Template-based deployment needs ION software 5.6.x or later, per the guide.
- Not documented in the sources used: deployment status values and timeouts, what deleting a deployment
  removes, the request shape of the deploy call, the exact calls for unassign and put-back,
  and the response to a deploy with a missing variable. These are marked where they arise.
- **Deploying onto an existing site name may change that site, deleting a site or shell is treated as
  permanent, and assigning or releasing a device changes live equipment.** Each has a gate above.
- Circuit labels, WAN interfaces, link-quality settings, and service endpoints cannot be removed by this
  procedure; a site that has them cannot be deleted from here.

## Tools

| Operation | Description | Category |
|---|---|---|
| query_templates | List site templates | Read |
| read_template | Read one site template | Read |
| query_sites | Query sites by name or identifier | Read |
| read_site | Read one site | Read |
| read_site_status | Read a site's status | Read |
| query_machines | List devices in the tenant inventory | Read |
| read_machine | Read one device and its state | Read |
| query_elements | List elements (devices bound to sites) | Read |
| read_element | Read one element and its state | Read |
| list_element_shells | List the device shells at a site | Read |
| read_deployment | Read one deployment record | Read |
| read_deployment_status | Read a deployment's job status | Read |
| create_template | Create a site template from a reference site | Write |
| deploy_template | Deploy sites from a template | Write (gated) |
| assign_device_to_shell | Attach a device to a device shell | Write (gated) |
| delete_deployment | Delete a deployment record | Write (gated) |
| unassign_device | Detach a device from a site (unverified binding) | Write (gated) |
| declaim_device | Put a device back in inventory (unverified binding) | Write (gated) |
| delete_element_shell | Delete an unattached device shell | Write (gated) |
| delete_site | Delete a site | Write (gated) |

## Verification checklist

- [ ] The template was found by exact name, and every mandatory variable is present for every site
- [ ] No site name was reused without the operator's separate confirmation of an update
- [ ] Each device's inventory state was read before deploy or assignment
- [ ] The operator confirmed before every deploy, assignment, deployment delete, device release,
      shell delete, and site delete
- [ ] Deployment status was read per site until final, not assumed from the accepted call
- [ ] The site, its elements, shell state, and connectivity were re-read before reporting ONBOARDED
- [ ] Unverified and undocumented behaviors were reported as such, not presented as confirmed
