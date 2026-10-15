# Extreme Networks EXOS — Standard Upgrade Process

Upgrade the ExtremeXOS (EXOS) core image and modular packages on a switch or SummitStack, per the
ExtremeXOS User Guide's own documented "ExtremeXOS Upgrade Process" (Version 32.7.1, published May
2024). This is EXOS's own primary-image-vs-secondary-image (dual-partition) upgrade model, distinct
from the separate BootROM upgrade procedure (referenced but not covered here — see Known limitations).
Assumes an authenticated CLI/console session against the target switch (or SummitStack master node)
with EXEC access, able to run exec-mode commands, reach an image server (TFTP/HTTP/anonymous FTP, or a
USB 2.0 device) from the switch's own network configuration, and detect switch reachability across a
reboot.

## Operational procedure

### Step 1 — Back up the running configuration

Save the configuration to the database so it can be reapplied after reboot:
```
save
```
Confirm with `y` at the prompt when asked to save changes.

Then create a version-stamped backup copy — the source's own recommended method:
```
show switch
```
Locate the `Config Booted:` line to identify the exact configuration filename and the EXOS version that
created it, then:
```
cp <config-booted-filename> <config-booted-filename>-<exos-version>
```
Example: `cp ssh-privatekey.cfg ssh-privatekey-15_7_1_5`. Naming the backup with the EXOS version
embedded is what the source recommends — makes it unambiguous later which backup corresponds to which
pre-upgrade state, not just "a backup."

### Step 2 — Download ExtremeXOS and module images to a server the switch can reach

Retrieve the target `.xos` (core image) and any `.xmod` (module) files from the Extreme Networks
eSupport portal (`http://esupport.extremenetworks.com`, account required — request one via the portal's
"Request Web Login" link if needed). **The core image and module versions must match** — the source is
explicit: "the version number of the core image and the module must match." Also check the release
notes on the same portal, since the source states they "will always have the most current download and
install instructions" — treat this file as the general shape, and the target release's own notes as the
authority on anything version-specific.

Save the files to a TFTP server on the network, or to a USB 2.0 device.

### Step 2a (SummitStack only) — Confirm network reachability before downloading

On a SummitStack, log into the master node and confirm which virtual router reaches the image server:
```
ping vr vr-Mgmt <host>
ping vr vr-Default <host>
```
At least one must succeed. Use whichever virtual router succeeds as the `vr` argument in the download
command in Step 4.

### Step 3 — Find the inactive partition

A switch holds up to two core images (primary and secondary). **You must install to the inactive
partition** — installing to the active one is not the documented path.
```
show switch
```
Read the `Image Booted:` line: if it says `primary`, install to `secondary`; if it says `secondary`,
install to `primary`.

### Step 4 — Download and install the image to the inactive partition

```
download image [hostname|ipaddress] <filename> <partition> {install {reboot}}
```
(Full documented syntax: `download [ url url { vr vrname } | image [ active | inactive ]
[[ hostname | ipaddress ] filename {{ vr } vrname } { block-size block_size }] { partition }
{ install { reboot }} }`; the two supported top-level forms since EXOS 16.1 are `download url <filename>`
(multiple files at once, over TFTP/HTTP/anonymous FTP) and `download image <filename>` (a single `.xos`/`.xmod`
file over TFTP).)

Example interactive sequence:
```
# download image 10.68.9.7 summitX-15.7.1.4.xos primary
Debug information files are present in internal-memory.
These files will be removed if you continue with download.
Do you want to continue with download and remove existing files from internal-memory? (y/N) Yes
Do you want to install image after downloading? (y - yes, n - no, <cr> - cancel) Yes
Downloading to Switch....................................................................
Installing to primary partition!
Installing to Switch............................................................................
Image installed successfully
This image will be used only after rebooting the switch!
```

**Known space-collision condition:** if the switch is configured to write core-dump (debug) files to
internal memory, a new image download may not have enough space to complete. The switch will prompt to
remove the existing core-dump files during download (as shown above) — answering `y` is the documented
way through this, not a sign something has gone wrong.

Install any `.xmod` module images to the **same** inactive partition, using the same `download` command
form. The source recommends upgrading the core image and all modular packages together in the same
pass, not core-only followed by modules later.

If prompted "Do you want to install image after downloading?" and you answer `n`, the image is still
downloaded and saved, but installation is deferred — a separate `install image` command (not detailed
in the extracted source) is needed later. Prefer answering `y` unless there's a specific reason to
stage without activating.

### Step 5 — Reboot

**Stop and confirm with the operator before proceeding** — this is the disruptive step in this
procedure: the switch (or stack) goes down and comes back up, and there's no documented auto-abort
timer or rollback-on-timeout to fall back on if something goes wrong (see Known limitations). The CLI's
own `(y/N)` prompt below is a mechanical confirmation, not a substitute for the operator's go-ahead.

After installing the `.xos` and all `.xmod` images:
```
reboot
```
Confirm with `y` at the "Are you sure you want to reboot the switch?" prompt. The newly-installed image
only takes effect after this reboot — installation alone does not activate it.

On a SummitStack, this may instead be a stack-wide or per-node reboot — the source references separate
"Reboot the Switch" and "Reboot a Node in a SummitStack" options; confirm which applies to the target
topology before issuing a bare `reboot`.

### Step 6 — Verify

```
show switch
```
Confirm `Image Booted:` now reflects the newly-active partition and `Primary ver:`/`Secondary ver:`
show the target version on the partition just installed.
```
show version
```
Confirm the reported version matches the target.

## Patterns

- **You always install to the inactive partition, never the active one.** Step 3 exists specifically so
  this isn't gotten backwards — the currently-booted partition stays untouched as a fallback until the
  new one is confirmed good.
- **Core image and module versions must match — this isn't a suggestion.** Installing a core image
  without also upgrading its matching modules (or vice versa) is a documented version-mismatch condition
  to avoid, not just a best practice.
- **The install doesn't take effect until reboot.** A successful `download ... install` still requires
  the explicit `reboot` step — don't report success from the "Image installed successfully" message
  alone; that message itself states "This image will be used only after rebooting the switch!"
- **Release notes, not this file, are authoritative for version-specific upgrade instructions.** The
  source itself defers to release notes for "the most current download and install instructions" — treat
  this procedure as the stable shape and check the target release's notes for anything that might have
  changed.

## Known limitations

- Covers the core-image/modular-package upgrade process only — does not cover the separate BootROM
  upgrade procedure ("Upgrading the BootROM," cross-referenced in the source but not extracted here) or
  NMS-based installation ("Installing a Core Image with NMS," also cross-referenced but not extracted).
- Does not detail the standalone `install image` command for the "download now, install later" deferred
  path — only the combined `download ... install` form is covered in depth.
- No documented auto-abort-timer or rollback-on-timeout exists — once `reboot` executes, there's no
  built-in safety window. Recovery from a bad image relies on the untouched other partition (reboot again
  and select it) rather than any automatic mechanism this procedure triggers.
- SummitStack-specific reboot behavior ("Reboot a Node in a SummitStack" vs. a full stack reboot) is
  referenced but its exact distinction/commands were not extracted — confirm which applies before
  issuing `reboot` on a stack.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| CLI/console exec session (SSH or console), master node for a SummitStack | Sends every `save`/`show`/`cp`/`download`/`reboot`/`ping vr` command in this procedure; must survive the reboot to confirm the switch comes back up on the target version | Device Access |
| Image server reachable from the switch (TFTP/HTTP/anonymous FTP server, or a USB 2.0 device) | Serves the `.xos`/`.xmod` files the `download` command retrieves; SummitStack topologies must confirm virtual-router reachability to this server before downloading | Device Access |

## Verification checklist

- [ ] `show switch`'s `Image Booted:` line was checked before installing, to confirm the target
      partition was actually the inactive one
- [ ] Core image and all module (`.xmod`) versions being installed match each other
- [ ] A version-stamped configuration backup was created before starting, not just the in-database
      `save`
- [ ] `reboot` was confirmed and completed — installation success alone was not reported as the
      procedure's completion
- [ ] `show switch` / `show version` post-reboot confirmed the target version on the now-active
      partition
