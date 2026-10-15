---
name: software-upgrade-lifecycle
description: Upgrade the running software/firmware on a network device or stack, following that platform's own documented stage/activate/confirm/commit procedure and safety mechanisms (auto-abort timers, commit gates, health checks) where the platform provides them. Currently covers Cisco IOS-XE INSTALL mode, Cisco IOS XR classic RPM install mode (NCS 5500, ASR 9000), Arista EOS Standard upgrade/downgrade (single- and dual-supervisor), Juniper Junos OS EX Series Standard Installation (single- and redundant-RE), Extreme Networks EXOS Standard upgrade, NVIDIA Cumulus Linux (all 3 documented upgrade methods), and Palo Alto Networks Prisma SD-WAN ION devices (controller-driven upgrade). Use when a device needs an OS version upgrade and the platform's own upgrade procedure must be followed exactly (not improvised). Assumes an authenticated CLI/console or API session against the target device (or its management controller) is already available; this skill does not provision or authenticate it. Does not cover initial device bring-up, downgrade-specific procedures beyond what a platform's own rollback/abort covers, or any platform/mode not yet listed in references/INDEX.md.
argument-hint: "[vendor] [platform_family] [device] [image_path] [target_version]"
---

# Software Upgrade Lifecycle

Runs a device software upgrade on whichever vendor/platform the caller is targeting, following that
platform's own documented procedure, safety mechanisms, and pass/fail criteria exactly as published —
never an improvised or by-analogy sequence.

## When to use this skill

- A network device or stack needs an OS/firmware version upgrade and a documented, deterministic
  procedure for the target platform exists under `references/`.
- Not for initial device bring-up, or any vendor/platform-family/mode not yet listed in
  `references/INDEX.md` — see that file before assuming coverage.

## Universal concepts (the shape every platform's procedure follows, not a wire standard)

There is no single IETF/wire spec grounding this the way RFC 1035 grounds DNS — but every platform
procedure under this skill follows the same underlying shape, worth stating once instead of per vendor:

- **Stage the new image before touching the running state.** Where a platform separates image
  transfer from activation, the transfer step does not itself change what's running. Some platforms
  (e.g. Prisma SD-WAN ION) can chain download and install in one scheduled request; there, a
  download-only request is the staging step, and the request that includes install is the gated one.
- **Activation is the risky step, and some platforms give it a reversible window — not all do.** Where a
  platform provides a safety net (an auto-abort timer, a manual rollback command), never treat that
  window as equivalent to explicit confirmation — they solve different problems (the timer protects
  against an unreachable device, not against proceeding without sign-off). Where a platform has no
  documented safety net (e.g. Arista's standard `reload`/`install ... reload`), treat every activation
  step as needing the same operator confirmation discipline a timer would otherwise partially provide —
  don't assume one exists just because other platforms in this skill have one.
- **Where a platform has a separate, later "commit" (or equivalent) step, that step is what makes the
  change durable.** Until then, reverting to the prior version is the platform's own built-in path, not a
  manual reconstruction. Treat it as a required confirmation gate, not just on platforms that call it
  "commit" by name. Some platforms have no such step (e.g. Prisma SD-WAN ION upgrades run to completion
  once scheduled): there, the confirmation gate sits before the step that schedules or starts the install.
- **Where a platform documents an idempotency/already-on-this-version check, run it first** rather than
  discovering the no-op by re-running the whole procedure. Not every platform documents one explicitly
  (e.g. none of Cumulus Linux's three methods state an idempotency check) — where it's absent, confirm
  the current version before starting rather than assuming the platform will short-circuit a redundant
  upgrade on its own.

See `references/INDEX.md` for which platforms have a procedure, and each platform file for how it
implements this shape concretely (exact commands/calls, exact state names, exact error conditions).

## Procedure

1. **Identify vendor + platform family + mode** — from the caller's request or arguments. Check
   `references/INDEX.md`; if no matching row exists, stop: improvising a generic upgrade sequence for an
   undocumented platform is out of scope for this skill (get the vendor's own procedure documented as a
   new reference file first).
2. **Open the matching `references/<vendor>/<platform-family>.md`** and follow it exactly — numbered
   steps, safety mechanisms, error handling, patterns, known limitations, tools, and verification
   checklist all live there.
3. **Report the outcome** using that platform file's own status vocabulary (e.g. `SUCCESS`,
   `IDEMPOTENT`, `PARTIAL`) — don't normalize it away.

## Known limitations

- Platform coverage is exactly what's listed in `references/INDEX.md` — currently Cisco IOS-XE INSTALL
  mode, Cisco IOS XR classic RPM install mode, Arista EOS Standard upgrade/downgrade, Juniper Junos OS
  EX Series Standard Installation, Extreme EXOS Standard upgrade, NVIDIA Cumulus Linux, and Prisma SD-WAN ION devices. A
  platform/mode not listed needs a new reference file before this skill can be used for it.
- Does not cover initial device bring-up or downgrade procedures beyond what a platform's own built-in
  rollback/abort mechanism provides.

## Contributing to this skill

**`SKILL.md` only changes for two reasons: a bug in the universal-shape/router logic above, or adding a
pointer to a newly-documented vendor/platform-family.** This category is expected to accumulate the most
vendor/platform entries of any skill in this repo — resist the temptation to inline any platform's
procedure here as it grows. Every platform-specific fact (exact commands, exact state names, a new error
condition, a version-specific quirk) belongs in that platform's own `references/<vendor>/*.md`.

## Tools

Each platform procedure assumes its own execution mechanism (CLI/console session, REST API session) —
see `references/INDEX.md` for which, and that platform's file for the specific mechanisms.

## Verification checklist

- [ ] Vendor + platform family + mode confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own procedure file was followed exactly, including its own confirmation gates and
      error handling — not a generic/improvised sequence
- [ ] Outcome reported using the platform procedure's own status vocabulary
