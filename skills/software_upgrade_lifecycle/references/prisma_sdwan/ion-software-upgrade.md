# Palo Alto Networks Prisma SD-WAN — ION Device Software Upgrade (controller-driven)

Upgrade the software on a claimed Prisma SD-WAN ION device by telling the cloud controller which image
to fetch and when to install it; the device then downloads and installs on its own. Covers one device,
a batch of devices, and a high-availability (HA) pair at a branch. Does not cover unclaimed devices,
cellular-module firmware, controller (cloud) releases, which the vendor operates itself, or the
physical replacement of a device.

Written against the Prisma SD-WAN Administrator's Guide (last revised August 11, 2026) and the
Prisma SD-WAN unified API specification (version labelled "Latest"), checked 2026-10-14. Where those
sources do not say how something behaves, this file says so instead of filling the gap.

Assumes an authenticated API client for the tenant is available (see the endpoints file for the
authentication quirk), and that the device is already claimed and running release 5.1.1 or later. On
older releases the scheduling features below do not exist and only an immediate upgrade is offered.

## Common Sequences

Steps marked (gated) contain an operator confirmation.

- **Upgrade one device now or at a set time:** *Identify the device* → *Choose and check the target
  image* → *Check for existing upgrade activity* → *Schedule the upgrade* (gated) → *Monitor the
  upgrade* → *Verify the result*.
- **Stage first, install later:** *Identify the device* → *Choose and check the target image* → *Check
  for existing upgrade activity* → *Schedule a download only* → *Monitor the upgrade* (until the image
  is downloaded) → *Schedule the upgrade* (gated) → *Monitor the upgrade* → *Verify the result*.
- **Upgrade an HA pair:** *Upgrade an HA pair* (it calls the single-device sequence for each member,
  with the role switches between them, all gated).
- **Upgrade a batch:** *Upgrade a batch* (the single-device sequence per device, one confirmation for
  the whole batch).
- **Recover from a failed or unwanted upgrade:** *Monitor the upgrade* → *Retry, edit, or abort* or
  *Roll back* (gated).

## Status vocabulary

Every run ends with exactly one of these. Report it with the evidence (state read, version read, error
code).

| Status | Meaning |
|---|---|
| SUCCESS | The device reports the target version as active and the verification checks pass |
| IDEMPOTENT | The device already runs the target version; nothing was scheduled |
| DOWNLOADED | A download-only request finished; the device still runs the old version |
| SCHEDULED | The request was accepted and is waiting for its time; final status only when the operator asked to stop at scheduling |
| REJECTED_INELIGIBLE | The device, image, or path between versions does not qualify; nothing was sent |
| DECLINED | The operator did not confirm |
| PARTIAL | The target version is active but a post-upgrade check failed (for example a tunnel, or a mode setting that needs re-enabling) |
| TIMED_OUT | The expected state was not reached within the operator's time limit (the sources give none) |
| FAILED | The platform reported a failed, aborted, or cancelled state, or an error. Include the state, failure text, and code |

## Operations

### Identify the device

Binds to: get_element, list_elements.

Read the claimed device record before anything else.

- Record its identifier, model, current software version, site, role, connection state, and whether it
  belongs to an HA pair. Look it up by identifier, or by listing devices and matching on name or serial.
- A device that is not connected to the controller cannot be reached for a download. The sources do not
  say what an upgrade request to a disconnected device does (assumption: it stays pending). Report
  REJECTED_INELIGIBLE rather than queueing blindly; the controller-connectivity troubleshooting in the
  vendor guide is a separate procedure.
- Success: one device record with a model and a current version.

### Choose and check the target image

Binds to: list_element_images, get_element_image.

Read the images allocated to the tenant. The vendor does not push device releases on its own; only the
images allocated to the tenant can be chosen.

- Pick the image whose per-model list includes the device's model. An image that does not list the
  model is not eligible.
- Each image carries a version, a state, a recommended-release flag, a long-term-support flag, an
  end-of-life date, FIPS-certification flags, and a release-notes link. The meaning of the image state
  values is not stated in the sources (unknown): prefer an image the platform itself flags as
  recommended and read its release notes before choosing.
- Scheduling for a time after an image's end-of-life date is rejected by the platform.
- Check the path between the current and target version against the vendor's documented limits:
  - Going from 6.1.x directly to 6.2.x, 6.3.x, 6.4.1, or 6.5.1 is unsupported; the vendor suggests
    6.3.6, 6.4.2, 6.4.3, or 6.5.2 and later as targets.
  - A device may need an intermediate version first. The bulk-upgrade screen hides targets that are
    incompatible with a device for this reason; the API route's behavior in this case is not documented
    (unknown), so treat the bulk screen's rule as binding.
  - Devices in FIPS mode cannot be upgraded to 6.2.3, 6.3.1, 6.3.2, or 6.3.3.
  - Reaching 6.5.x while in FIPS-CC mode requires meeting the key-size limits for ciphers, IKEv2 instead of IKEv1 for standard
    IPsec profiles, and BGP MD5 authentication disabled before the upgrade.
  - FIPS mode is not available in release 6.8.1 (the vendor says nothing about later releases); a device that must stay FIPS-compliant is not a candidate for that release.
- Check what blocks a later rollback and tell the operator now: post-quantum cryptography settings on a
  device on 6.8.1 or later block a downgrade until they are removed; layer-2 switch ports (ION 1200-S
  from 6.0.2, ION 3200 from 6.3.1) are documented as preventing a downgrade below those releases.
- Any failed check: REJECTED_INELIGIBLE, naming the check.

### Check for existing upgrade activity

Binds to: get_element_software_state, get_element_software_status.

Do this before scheduling, so a repeat run does not stack a second request on the first.

- Read the device's current upgrade configuration and its latest status records (the platform keeps up
  to five of the user's recent operations).
- If the active version already equals the target and no operation is pending: IDEMPOTENT. Report it.
- If a download or upgrade is already scheduled or running: stop and show the operator its state and
  times. Change it only through *Retry, edit, or abort*.
- Keep the configuration record's version marker (the optimistic-concurrency field), which the schedule
  call must send back.

### Schedule a download only

Binds to: update_element_software_state.

Stages the image on the device without installing it. The sources do not say whether forwarding is
affected while the device downloads (assumption: it is not, which is why this step has no gate).

- Send the chosen image identifier and a download time. Leave the upgrade time out; with only a
  download time the vendor says the upgrade does not follow and must be scheduled separately.
- Omit both times to start immediately; the platform then also installs right after downloading, so do
  not omit both when the intent is to stage only. Always send a download time for a staging request.
- Optionally send a download window in minutes (the maximum time over which the device keeps retrying)
  and up to four interface identifiers to download through. A blank interface list means the device picks the controller-facing interface or any
  interface flagged for internet access.
- The vendor's sources contradict each other on an unreachable chosen interface: one passage says only
  the listed interfaces are ever used, another says the download falls back to the controller or an
  internet interface. Follow the stricter one (assume only listed interfaces) and read the status to see
  which actually happened.
- A failed download means no upgrade is attempted. The device retries three times by default before
  reporting failure; a download window replaces the three-try limit with retries inside the window.
- Success: the status reaches the downloaded state (see *Monitor the upgrade*) and the device still
  reports the old version. Report DOWNLOADED.
- Errors: report FAILED with the code. The error list is in the endpoints file.

### Schedule the upgrade

Binds to: update_element_software_state.

This step makes the device install the new image. The sources do not state whether an install restarts
the device or interrupts forwarding (assumption: it does, since the vendor's HA procedure exists "to
avoid downtime"). Treat it as disruptive.

**Stop and confirm with the operator before scheduling.** State the device, site, current version, target
version, scheduled time (or "immediately"), whether the device is half of an HA pair, and the rollback
restrictions found in *Choose and check the target image*. If the operator declines, report DECLINED and
send nothing.

- Immediate upgrade (download then install, back to back): send only the image identifier and omit
  both times.
- Timed upgrade with download and install together: send the image identifier and an upgrade time; the
  device downloads and installs in sequence at that time.
- Install of an image already downloaded: send the same image identifier with an upgrade time
  (assumption: the platform recognizes the existing download; the sources only say this is possible
  from the console).
- With an upgrade window (0 to 59 minutes in the API; the console accepts 5 to 59) the device keeps
  retrying within it; the vendor's stated default is 30 minutes. Without one, three attempts. If the
  window ends while a download is in progress, the download is still allowed to finish.
- Times use month-day-year with 24-hour clock seconds. The time zone is not stated (unknown): confirm
  with the operator what the platform interprets, or schedule immediately.
- A window or interval is accepted only together with its matching time.
- Success: the request is accepted and the status reaches a scheduled or in-progress state. Report
  SCHEDULED if the operator is stopping here; otherwise continue to *Monitor the upgrade*.
- Errors: report FAILED with the code.

### Monitor the upgrade

Binds to: get_element_software_status, query_element_software_current_status, query_element_software_status (tenant-wide status), query_software_download_history (past downloads, to confirm an earlier download of the image).

Poll a read until the device reaches a terminal state. The sources give no poll interval, no overall
timeout, and no rate limits (unknown); back off on throttling responses and honor any retry-after
header. Ask the operator for a time limit, then report TIMED_OUT when it passes.

- The status record has a state, download percentage, failure text, active version, rollback version,
  and the image identifiers involved. The state list is long and the sources do not define each value.
  Treat them by name (inference, not documented):
  - Waiting: pending, init, discovery, download_discovery, download_scheduled, upgrade_scheduled,
    waiting_download_time, waiting_install_time.
  - Working: download, download_init, downloading, upgrade, upgrade_init, upgrading, install, installing,
    verify, verifying, in-progress.
  - Done, download only: download_complete.
  - Done, install: upgrade_complete, complete, done.
  - Failed or stopped: download_failed, install_failed, upgrade_failed, failed, download_abort,
    upgrade_abort, download_cancelled, upgrade_cancelled, the cancel and abort "pending" states, invalid.
- The console groups devices into download scheduled, download complete, upgrade scheduled, and "other"
  for anything in between; devices on releases before 5.1.1 always show under "other".
- Right after a download completes, an install-scheduled device briefly shows the download-complete
  state before the scheduled-upgrade state.
- Use the tenant-wide query to watch many devices at once instead of reading each one.
- The status history holds the five most recent operations on the device, so read it to see what
  already happened.
- Done and failed states: see *Verify the result* or *Retry, edit, or abort*.

### Verify the result

Binds to: get_element, get_element_software_status. Device CLI check: dump software status.

- The status record's active version equals the target, with a completed state, and the device record's
  software version agrees.
- Read the version on the device itself with `dump software status` where console or remote access is
  available; the vendor names this as the way to confirm the version.
- The device shows connected to the controller again.
- Mode-specific follow-ups the vendor lists after an upgrade: re-enable NTP authentication on devices
  in FIPS-CC mode (it must be enabled explicitly after the upgrade).
- For one half of an HA pair, also run the pair checks in *Upgrade an HA pair*.
- All pass: SUCCESS. Version correct but a check fails: PARTIAL, naming it. Version not the target after
  the device reports completion: FAILED with the observed version.

### Retry, edit, or abort

Binds to: update_element_software_state, get_element_software_status.

- Retry after failure: the vendor says a failed operation must be rescheduled. Run *Schedule a download
  only* or *Schedule the upgrade* again with the same image; the gate in the latter applies again. Read
  the failure text first and do not retry blindly if it points to a version-path or eligibility problem.
- Edit a scheduled operation (an edit that sets or changes an upgrade time goes through the same
  gate as *Schedule the upgrade*): the console lets an operator change a pending schedule. The API has one
  write for the configuration; sending a new schedule is assumed to replace the old one (assumption).
- Abort a pending or running download or upgrade: the console has an abort action, and the status
  vocabulary includes abort and cancel states. The sources document no API call or field that triggers
  an abort (unknown). Tell the operator the abort must be done in the console, and do not invent a
  field. Treat an abort of a running install as disruptive and confirm it with the operator first.
- Success: the status shows the new schedule, or the abort/cancel state. Report SCHEDULED, or FAILED
  with the final state if the platform ended in a failed or aborted state.

### Roll back

Binds to: update_element_software_state, get_element_software_status.

The vendor says rollback to an older version is possible but gives no dedicated procedure or call. The
status record exposes a rollback version and the previous image identifier. This file treats a rollback
as a scheduled install of the older image through the same write (assumption).

**Stop and confirm with the operator before rolling back.** State the device, the version it will move
to, and the restrictions below. Declined: DECLINED.

- The older image must still be allocated to the tenant and eligible for the model.
- Post-quantum settings (IPsec profiles that use a post-quantum shared key or extra key-exchange rounds,
  plus any standard VPN interface bound to such a profile) must be removed first, or the downgrade fails.
- Moving from FIPS-CC releases back to earlier ones requires NTP authentication to be turned off first.
- Downgrade to 6.2.3 or 6.3.x in FIPS mode is unsupported.
- Layer-2 switch port configuration blocks a downgrade below the release that introduced it.
- Success: *Verify the result* with the older version as the target.

### Upgrade an HA pair

Binds to: the single-device operations above, plus update_element for the redundancy priority (see Known limitations for what the specification leaves out).

The vendor's order is backup first, so traffic never loses both devices.

1. Identify which member is active and which is backup. The vendor's guidance is to mark the member administratively disabled in the HA group for the upgrade and enable it again afterwards; the guide describes this only for the console, so ask the operator to do it (unknown for the API). Run the single-device sequence on the backup member (all its gates apply). Verify its version.
2. **Stop and confirm with the operator** before changing roles. Give the backup member a higher priority than the active one, with preemption on (see Known limitations: the API cannot confirm preemption), so it becomes active. The vendor recommends keeping the two priorities at least 40 apart. The guide names 255 as the highest priority but the API schema allows 1 to 254; use the schema's range. Then check that every tunnel is up and traffic flows through the new active device.
3. Run the single-device sequence on the former active member (now backup). Verify its version.
4. **Stop and confirm with the operator** before switching back. Change the priorities again so the
   original member takes over, with preemption on. Check all tunnels and traffic again.

Success: both members report the target version, the original roles are restored, and tunnels and
traffic are normal. A failed check in step 2 or 4: stop, report PARTIAL, and leave the operator to
decide; do not upgrade the second member until step 2 is verified.

### Upgrade a batch

Binds to: the single-device operations above.

- The console allows at most 50 devices per batch and hides devices that are incompatible with the target.
  The API has no documented batch call (unknown): run the single-device sequence per device and keep to
  50 per batch (assumption that the console limit also applies to a script).
- Do not put both members of an HA pair in the same batch; use *Upgrade an HA pair*. (Author's safeguard, not stated by the vendor: it follows from the one-member-at-a-time order the vendor gives.)
- **Stop and confirm with the operator once for the whole batch**, listing each device, its current and
  target versions, and the schedule. Declined: DECLINED for every device.
- Report one status per device.

## Patterns

- **Scheduling is the commitment point.** There is no separate commit step: once an install has been
  scheduled or started the platform runs it to its own end, retrying on its own. The only documented
  ways back are an abort in the console or a rollback, so the confirmation sits before scheduling, not
  after.
- **Download-only and install-now differ only by which times are present.** Omitting both times is the
  immediate download-and-install case, so a staging request must always carry a download time.
- **A scheduled time is an upper bound for attempts.** The download window and the upgrade window limit how
  long the device keeps trying; they are not a delay.
- **Read the configuration record before writing it.** The write carries a version marker that came from
  the record; send back the latest.
- **Version checks beat time checks.** A device that has gone quiet after an install is not a failed one;
  read the status and the reported version before declaring failure.
- **Interfaces the device may use for downloading are capped at four.**
- **Bypass-pair ports that are down can interfere with an upgrade.** The vendor warns that after a bypass
  pair is brought down, its ports must each be brought up again individually or they stay down and can
  affect the upgrade. Check bypass-pair ports before scheduling on a device that has one.

## Known limitations

- Claimed ION devices only. The specification also has routes for machines (devices before they are
  claimed); a claimed-device error name suggests they reject claimed devices, which is an inference and
  not covered here.
- Not documented, so not invented: whether the install restarts the device and for how long; how to
  abort through the API; a dedicated rollback call; the time zone of scheduled times; rate limits;
  poll intervals; the meaning of each image state value; what the platform does for a disconnected
  device; a pre-check call for version compatibility.
- The HA redundancy priority is a field of the device record's HA settings (range 1 to 254, with the cluster id, source interface, and enable flag). The guide describes the change only in the console, and the HA settings schema has no preemption field, so how to turn preemption on through the API is unknown. Read the device record, change only the priority, and write it back; whether a write replaces the whole record is not stated, so send the full record from the read. Where preemption cannot be confirmed through the API, hand the role switch to the operator in the console.
- **Scheduling an install (and a rollback) is disruptive and effectively irreversible** from the
  automation's side once the device has started; the abort is console-only.
- Devices on releases before 5.1.1 only support an immediate upgrade without schedule, history, or
  download-only.

## Tools

| Operation | Description | Category |
|---|---|---|
| get_element, list_elements | Read claimed device records | Inventory |
| update_element | Write a device record, used here only for the HA priority | Write |
| list_element_images, get_element_image | Read the images allocated to the tenant | Software catalog |
| get_element_software_state | Read a device's upgrade configuration | Read |
| update_element_software_state | Write a device's download and upgrade schedule | Write (disruptive) |
| get_element_software_status, query_element_software_current_status, query_element_software_status | Read per-device or tenant-wide upgrade status | Monitoring |
| query_software_download_history | Read the tenant's past software downloads | Monitoring |
| Device CLI session | Run the vendor's software status check on the device | Device Access |

## Verification checklist

- [ ] The device record shows a connected, claimed device and the model was matched against the chosen
      image
- [ ] The version path was checked (no unsupported jump, no blocked mode combination) before scheduling
- [ ] The operator confirmed before the upgrade (or rollback) was scheduled
- [ ] The status record reports the target version as active with a completed state
- [ ] `dump software status` (or the device record) agrees on the version
- [ ] The device is connected to the controller again, and post-upgrade mode steps (such as re-enabling
      NTP authentication in FIPS-CC mode) were done
- [ ] For an HA pair: backup upgraded first, roles switched with confirmation, tunnels and traffic
      checked after each switch, original roles restored
