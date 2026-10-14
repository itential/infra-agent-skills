# Software Upgrade Lifecycle — Vendor / Platform-Family Index

One row per vendor + platform-family/mode combination — **not** per exact model, unless a specific
model's behavior genuinely differs from its family (see "Grouping rule" below). This index is the part
of this skill expected to grow the most — a large permutation space (vendor × platform family × OS mode
× version line) is exactly the case this category was piloted against.

| Vendor | Platform Family / Mode | File | Notes |
|---|---|---|---|
| Cisco | IOS-XE, INSTALL mode (any Catalyst/IOS-XE platform) | `cisco/ios-xe-install-mode.md` | add→activate→commit with auto-abort timer; does not cover bundle mode |
| Cisco | IOS XR, classic 64-bit RPM install (confirmed identical on NCS 5500 and ASR 9000) | `cisco/iosxr-classic-install-mode.md` | add→activate→commit, no documented auto-abort timer (commit needs explicit confirmation on every use); does not cover the newer IOS XR7 install workflow (NCS 5700 Series) |
| Arista | EOS, Standard upgrade/downgrade (image replace + reload; single- and dual-supervisor) | `arista/eos-standard-upgrade.md` | No auto-abort timer; dual-sup uses `install source <image> reload` to avoid a documented pre/post-SSO heartbeat-mismatch disruption. Does not cover Smart System Upgrade (SSU/`reload fast-boot`) or MLAG-peer upgrades — separate procedures. |
| Juniper | Junos OS, EX Series Standard Installation (single-RE and redundant-RE) | `juniper/junos-ex-series-standard-install.md` | `request system software add` with validation on-by-default for cross-release installs; redundant-RE variant requires disabling GRES/NSR first and always upgrades the backup RE before the primary. No auto-abort timer. Does not cover Category Change or Recovery Installation, or non-EX platforms/Junos OS Evolved. |
| Extreme Networks | EXOS, Standard core-image/module upgrade (dual-partition) | `extreme/exos-standard-upgrade.md` | `download image ... install` to the inactive partition, confirmed via `show switch`'s `Image Booted:` line; core image and module versions must match. No auto-abort timer. Does not cover BootROM upgrade or NMS-based install. |
| NVIDIA | Cumulus Linux, all 3 documented upgrade methods (Optimized Image / Package / ONIE) | `nvidia/cumulus-linux-upgrade.md` | Only ONIE is destructive/crosses release trains; only Optimized Image and Package support ISSU (with day-0 BGP-graceful-restart + half-resource-mode prerequisites). No auto-abort timer on any method. Third-party signal (unconfirmed) that NVIDIA may be moving to NVOS — flagged, not assumed. |
| Palo Alto Networks | Prisma SD-WAN, ION device software upgrade (cloud-controller driven; single device, batch, HA pair) | `prisma_sdwan/ion-software-upgrade.md` (wiring in `prisma_sdwan/ion-software-upgrade-endpoints.md`) | REST API against the controller, not a device session. Download and install are scheduled together or separately; no commit step and no documented auto-abort timer, so the gate is before scheduling. Abort is console-only in the sources; rollback is a documented capability with no dedicated procedure (modeled as a scheduled install of the older image, marked as assumption). HA pairs upgrade backup first with role switches between. Does not cover unclaimed devices, cellular-module firmware, or vendor-run controller releases. The "commit" universal concept in `SKILL.md` was corrected for this vendor. |

## Grouping rule

Group by **platform family + OS mode**, not by exact model or version, unless a specific model's
behavior is documented as genuinely different (e.g. a stack-specific restriction that doesn't apply to
standalone units — capture that as a subsection inside the family file, not a new file). Splitting by
version line only when the *procedure itself* changes across versions (a new required flag, a removed
safety mechanism) — not for every point release.

**Confirmed case in point:** IOS-XE and IOS XR are both Cisco but get separate rows/files above — same
vendor, genuinely different install architecture (IOS-XE's `install`/`packages.conf` model vs. IOS XR's
`install add`/`activate`/`commit` against a per-VM repository). This validated the grouping rule as
designed: the split is on platform-family+mode, not on vendor name alone. Cross-checking a second
platform doc (ASR 9000) against the primary source (NCS 5500) before assuming a single file covers both
is also the expected workflow — in this case they turned out identical, so one file covers both; a
future comparison finding a real difference would justify separate files instead.

**Lesson learned from this addition — namespace companion files by platform-family+mode, not
generically.** `references/<vendor>/` holds multiple platform-family files once a vendor has more than
one (as Cisco now does), so a bare `endpoints.md` in that directory silently collides between them —
the first file written to that generic name gets clobbered by the second. Name every companion file
after its procedure file's own basename instead: `<platform-family-and-mode>-endpoints.md`. This
applies from the *first* file added for a vendor, not just once a second one shows up — retrofitting
the rename after a collision is how this was caught the hard way.

**Another documentation-hygiene lesson (found adding Arista):** the source's own Standard-upgrade
section (§8.3.1.1) reused a heading and subsections verbatim from its SSU chapter ("Preparing the
Switch for SSU," complete with SSU-specific BGP-graceful-restart and MLAG `reload-delay` guidance) —
publisher docs can themselves have copy-paste artifacts. Don't assume a source section's content
belongs to the procedure it's nested under just because of where it appears; cross-check against the
chapter's own stated scope (here, §8.1's explicit SSU-vs-Standard distinction) before carrying a
subsection forward. Flagged and excluded rather than reproduced.

Expected growth shape as more vendors/platform-families are added (not yet built — illustrative):

| Vendor | Platform Family / Mode | File |
|---|---|---|
| Cisco | IOS-XE, BUNDLE mode | `cisco/ios-xe-bundle-mode.md` |
| Cisco | NX-OS | `cisco/nx-os.md` |
| Cisco | IOS XR7 (NCS 5700 Series) | `cisco/iosxr7-install-mode.md` |
| Juniper | Junos OS Evolved | `juniper/junos-evolved-standard-install.md` |
| Juniper | Junos OS, routing devices / SRX Series (non-EX) | `juniper/junos-routing-srx-standard-install.md` |
| Arista | EOS, Smart System Upgrade (SSU) | `arista/eos-ssu.md` |
| Arista | EOS, MLAG peer upgrade | `arista/eos-mlag-peer-upgrade.md` |
| HPE Aruba | ArubaOS-CX | `hpe/arubaos-cx-upgrade.md` |
| Palo Alto | PAN-OS | `paloalto/pan-os.md` |

**Multiple methods within one platform-family file, when they're genuinely alternatives, not
sequential steps (found adding NVIDIA Cumulus Linux):** Cumulus Linux documents three upgrade methods
(Optimized Image, Package, ONIE) that are mutually exclusive choices for a given upgrade, not stages of
one procedure — unlike Cisco/Arista/Juniper/Extreme's single documented method each. One file
(`nvidia/cumulus-linux-upgrade.md`) covers all three with a comparison table up front so the caller
picks the right one, rather than three near-duplicate files or one file that reads like a single linear
procedure when it isn't. Use this shape (comparison table, then per-method sections) when a
platform-family genuinely offers alternative upgrade paths — don't force it into the single-procedure
template used elsewhere in this index if the source itself documents real alternatives.

**Retrieval-tool reliability is vendor-site-specific, not predictable in advance.** Direct `curl`
succeeded cleanly for Cisco (NCS 5500/ASR 9000 PDFs), Extreme's EXOS site, and Freshservice's API
reference, but returned HTTP 406 for Arista's site on every user-agent tried. Fetch-and-summarize
tooling worked for Juniper and NVIDIA but returned only navigation-shell content (no body text) for
Extreme's site across multiple pages before direct `curl` succeeded there instead. Try the
fetch-and-summarize path first for speed; fall back to direct `curl` + local HTML extraction when it
returns incomplete/summarized-without-substance content; ask the user for a PDF only when both fail
(as happened for Arista).

## Adding a new vendor or platform family

1. Create `references/<vendor>/<platform-family-and-mode>.md` following the shape of
   `cisco/ios-xe-install-mode.md` (Operational procedure with numbered steps → Patterns → Known
   limitations → Tools → Verification checklist).
2. If the procedure is CLI-driven, keep literal commands inline in that file (payload, not a
   tool-selection key) — no separate endpoints file needed. If it's REST/API-driven, add
   `<platform-family-and-mode>-endpoints.md` alongside it with the literal wiring, per the usual
   convention — **never a bare `endpoints.md`** in a vendor directory that has (or might later
   have) more than one platform-family file. See "Lesson learned" above.
3. Add one row to the table above.
4. Do NOT add vendor/platform-specific procedure content to the top-level `SKILL.md` — see that file's
   own contribution note. This is the rule most likely to be tempting to break here, precisely because
   this category has the most vendors — resist it; that's the whole reason `SKILL.md` stays small no
   matter how large this table gets.
