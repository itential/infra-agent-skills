---
name: alert-monitor-management
description: Create a monitor or check that watches a metric/resource for a threshold breach, and acknowledge or resolve an alert it raises, on a supported observability platform — Datadog, New Relic, LogicMonitor, Paessler PRTG, Centreon, OP5 Monitor, or Thruk. Use when a caller needs to stand up new alerting coverage for a resource, silence/own an in-progress alert, or confirm an alert has cleared. Assumes an authenticated API client for the target platform (API key/app key pair, OAuth bearer token, or username/passhash, per platform) is already available; this skill does not provision or authenticate that client. Does not cover notification-channel/integration setup (Slack, PagerDuty, email routing), dashboard creation, log-pipeline configuration, or synthetic/browser-check authoring beyond what a platform's own monitor-creation call requires.
argument-hint: "[platform] [create-monitor|acknowledge|resolve] [target] [condition/alert_id]"
---

# Alert & Monitor Management

Creates a monitor/check that evaluates a condition against collected data, and acknowledges or
resolves an alert raised by one, on one of the supported observability platforms, following that
platform's own documented API and alert lifecycle.

## When to use this skill

- A monitor, check, alert condition, or alert rule needs to be created on Datadog, New Relic,
  LogicMonitor, Paessler PRTG, Centreon, OP5 Monitor, or Thruk so that a metric, log signal, sensor, or resource starts producing
  alerts when a threshold is breached.
- An already-raised alert on one of these platforms needs to be acknowledged (claimed/silenced
  while work is ongoing) or resolved/closed.
- Not for configuring where notifications get delivered (notification channels, escalation
  targets outside the alert-rule fields a platform's own create-monitor call requires), building
  dashboards, or authoring synthetic/browser test scripts — those are separate concerns even when
  the same platform's UI bundles them nearby.

## Universal concepts (apply regardless of platform)

- **A monitor/check is a standing evaluation, not a one-time test.** Every platform here re-runs its
  configured condition against fresh data on an ongoing basis; creating one does not itself raise an
  alert — an alert only appears once the condition's threshold is breached on a later evaluation.
- **Alerts trend toward auto-clearing, not manual closure, everywhere in scope.** Every platform
  documents that an active alert closes on its own once the signal that caused it returns to a
  non-violating state for the condition's own configured recovery window (Datadog monitors return to
  OK; New Relic NRQL violations close after the signal holds below threshold for the recovery period;
  LogicMonitor alerts clear once the datapoint fails the threshold for its configured clear interval;
  PRTG sensors leave the Down/alarm state once the channel is back within limits; Centreon, OP5
  Monitor and Thruk problems leave their non-OK state when a later check returns a healthy result). Do not assume a
  platform requires — or even offers — a manual "resolve" call as the normal path; check that
  platform's own `procedure.md` for whether one exists and what it actually does.
- **Acknowledging is ownership/notification control, not resolution.** On every platform in scope,
  acknowledging an alert marks it as being worked and typically suppresses further repeat
  notifications for that occurrence, but it does not change the underlying measured condition and
  does not by itself clear the alert — the alert still clears (or doesn't) based on the data, exactly
  as the point above describes.
- **Creating a monitor and routing its notifications are frequently two separate configuration
  objects.** Where a platform splits "what condition triggers an alert" from "who gets notified and
  how" (most visibly LogicMonitor's DataSource-datapoint-threshold vs. Alert Rule split), that split
  is platform-specific, not something this skill flattens away — follow the platform's own
  `procedure.md` for which object owns which part.
- This capability has no single wire-level standard grounding it (unlike, say, DNS with RFC 1035) —
  each platform below defines its own monitor/alert model from its own API documentation; treat any
  claim above as accurate only to the extent each vendor's own `procedure.md` confirms it holds for
  that platform.

## Procedure

1. **Identify the target platform** — from the caller's request or the `platform` argument. If it
   isn't one of the platforms in `references/INDEX.md`, stop: this skill doesn't cover it, and does
   not improvise a generic procedure for an unsupported platform.
2. **Open `references/<platform>/procedure.md`** and follow it exactly — it contains that platform's
   full operational procedure for creating a monitor/check and for acknowledging/resolving an alert,
   including its own error handling, patterns, known limitations, tools, and verification checklist.
   This file is intentionally the router; the real steps live per platform because the platforms
   genuinely do not share one alerting model (see `references/INDEX.md` for the shape differences,
   e.g. LogicMonitor's DataSource/AlertRule split vs. the other platforms' single monitor/check
   object).
3. **Report the outcome** using that platform procedure's own status vocabulary (e.g. `CREATED`,
   `ACKNOWLEDGED`, `RESOLVED`, `REJECTED_*`, `FAILED`) — don't normalize it away.

## Known limitations

- Does not cover notification-channel or escalation-chain setup as a standalone task — only the
  fields a platform's own monitor/alert-rule creation call requires inline (e.g. an escalation chain
  ID reference). Building a new notification channel or escalation policy from scratch is out of
  scope on every platform here.
- Does not cover dashboards, log-pipeline/processing configuration, or synthetic/browser-check
  script authoring, even on platforms where those live in the same product area as monitors.
- Platform coverage is exactly the seven vendors in `references/INDEX.md` — a platform not listed
  there needs a new `references/<platform>/procedure.md` before this skill can be used for it.
- Where a platform's own documentation does not state a manual "resolve" action exists (or states
  explicitly that creating new monitor objects outright isn't supported via API), that platform's
  `procedure.md` says so plainly rather than this skill inventing one — see each platform file's own
  Known Limitations.

## Contributing to this skill

**`SKILL.md` itself should only ever change for two reasons: a bug in the universal concepts/router
logic above, or adding a pointer to a newly-supported platform.** Platform-specific procedure
changes — a new error code, a corrected field name, a changed API path, a changed alert-lifecycle
detail — belong in that platform's own `references/<platform>/procedure.md` and `endpoints.md`,
never here. If you're about to add vendor-specific detail to this file, put it in the platform's
reference file instead.

## Tools

Each platform assumes its own authenticated client (REST API, GraphQL/NerdGraph API, PRTG's
HTTP/REST v2 API, or an external-command API) — see `references/INDEX.md` for which, and that platform's `procedure.md` for the
specific operations/mechanisms.

## Verification checklist

- [ ] Target platform confirmed against `references/INDEX.md` before proceeding
- [ ] That platform's own `procedure.md` was followed, including its own confirmation gates and
      error handling — not a generic/improvised sequence
- [ ] Outcome reported using the platform procedure's own status vocabulary
