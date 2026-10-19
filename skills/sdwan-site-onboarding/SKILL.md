---
name: sdwan-site-onboarding
description: Bring a new branch site onto an SD-WAN fabric from a reusable site blueprint, attach its edge devices, confirm it is operating, and back it out if needed — currently Prisma SD-WAN (site template creation and deployment, device-shell assignment, deployment status, removal) and Versa Director (device creation from a post-staging template, device activation, confirmation). Use when onboarding one or more branch sites. Not for authoring routing or security policy (see sdwan-policy-management). Assumes an authenticated client for the target SD-WAN controller is already available; this skill does not provision or authenticate it. Check references/INDEX.md for which platforms and operations are covered.
argument-hint: "[platform] [action: find_template|create_template|deploy_site|assign_device|verify_site|release_device|remove_site] [site name, template, device serial]"
---

# SD-WAN Site Onboarding

Takes a branch site from nothing to an operating member of the SD-WAN fabric — site and device
configuration created from a blueprint, edge hardware attached, health confirmed — and, where the
platform allows, reverses it, following the target platform's own documented procedure.

## When to use this skill

- Creating a site blueprint from a proven reference site, then deploying one or more new sites from it,
  with or without the edge device already in hand.
- Attaching or releasing an edge device for a site that is being onboarded.
- Checking whether a deployed site finished onboarding, or removing a site that should not exist.
- Not for building the routing, security, or path policy a site uses — see `sdwan-policy-management`.
- Not for wireless SSID/WLAN setup, even where one vendor sells both — see
  `wireless-network-management`.
- Not for point-to-point VPN tunnels — see `vpn-tunnel-management`.
- Not for device software upgrades on an already-onboarded site — see `software-upgrade-lifecycle`.

## Universal concepts (shared SD-WAN vocabulary, not a wire standard)

Only two platforms are documented today, so these are claims expected to hold for any SD-WAN platform and
must be re-checked when another is added (`AGENTS.md` rules 4 and 14). Where a platform differs,
its own procedure wins.

- **A site and its edge device are separate objects.** Where the platform allows it, site
  configuration can be created before the physical device is available and bound to the device later.
- **A device must be known to the controller before it can carry a site.** How and when it is
  attached (during deployment or in a later step) varies by platform; follow the platform procedure.
- **Deployment is asynchronous where documented.** An accepted request is not a finished site; confirm
  the final state of each site separately.
- **A site name may already be in use.** Check for an existing site of the same name first; the platform
  may update it or reject the request.
- **Removal usually has ordering constraints** (device detached before the site can go); where the
  platform documents them, follow that order.

## Procedure

1. **Identify the target platform** — from the request or the `platform` argument. Check
   `references/INDEX.md`; if no matching row exists, stop: this skill doesn't cover it yet.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it holds that platform's
   sequences, confirmation gates, error handling, patterns, limitations, tools, and verification
   checklist.
3. **Report the outcome** using that procedure's own status vocabulary — don't normalize it away.

## Known limitations

- Platform coverage is in `references/INDEX.md`; a platform not listed there needs a new reference
  file first.
- Does not cover authoring routing, security, or path policy, wireless networks, or software upgrades.
- Does not cover data-center sites, firewall-hosted SD-WAN, or virtual edge instance provisioning unless
  the platform procedure says so.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal concepts/router logic above, or
adding a pointer to a newly-supported platform.** Platform-specific changes — a new error code, a
corrected field, a changed API route — belong in that platform's own `references/<platform>/` files,
never here.

## Tools

Each platform assumes its own authenticated client — see `references/INDEX.md` for which, and that
platform's `procedure.md` for the operations.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its confirmation gates on deploying,
      assigning or releasing devices, and removing deployments, shells, or sites
- [ ] Outcome reported using the platform procedure's own status vocabulary
