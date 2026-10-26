# LogicMonitor — DataSource/AlertRule Creation & Alert Acknowledge Procedure

Defines the alerting condition on LogicMonitor by importing a DataSource (whose datapoint
thresholds are what actually generate an alert) and routes matched alerts with an Alert Rule, then
manages acknowledgment of alerts raised. Uses LogicMonitor's REST API. Assumes an authenticated
REST client (an Access ID/Access Key pair used to build LogicMonitor's documented HMAC-SHA256
request signature) against the target portal is already available.

Sources (retrieved 2026-09-29): LogicMonitor "Add Alert Rules" REST API v1 reference
(https://www.logicmonitor.com/support/rest-api-developers-guide/v1/alert-rules/add-alert-rules);
LogicMonitor "Acknowledge Alerts" REST API v1 reference
(https://www.logicmonitor.com/support/rest-api-developers-guide/v1/alerts/acknowledge-alerts);
LogicMonitor "Import DataSources from XML" REST API v1 reference
(https://www.logicmonitor.com/support/rest-api-developers-guide/v1/datasources/import-datasources-from-xml);
LogicMonitor "Static Thresholds for Datapoints"
(https://www.logicmonitor.com/support/alerts/about-alerts/static-thresholds-for-datapoints);
LogicMonitor "6. Understanding LogicMonitor alerts"
(https://www.logicmonitor.com/support/getting-started/i-just-signed-up-for-logicmonitor-now-what/6-understanding-logicmonitor-alerts);
LogicMonitor "Guidelines for Responding to Alerts"
(https://www.logicmonitor.com/support/alerts/responding-to-alerts/guidelines-for-responding-to-alerts).
LogicMonitor's published REST API v3 OpenAPI description, for the alert-acknowledge and alert-rule
resources (literal routes in `endpoints.md`) and their required-field shape.

## Operational procedure — create a monitor (DataSource + Alert Rule)

LogicMonitor splits "what triggers an alert" from "who gets told and how" into two separate
objects — do not treat this as one create-monitor call the way the other platforms in this skill
do.

1. **Confirm the alerting condition belongs on a DataSource, not just an Alert Rule.** The actual
   detection logic — which metric (datapoint) is collected and what threshold makes it alert-worthy
   — lives on a DataSource definition, specifically each datapoint's static thresholds. LogicMonitor
   documents up to three severity-specific static thresholds per datapoint (Warning, Error,
   Critical); an Alert Rule cannot create a new detection condition on its own, only route ones a
   DataSource already defines.
2. **Obtain or author the DataSource definition.** LogicMonitor's own tooling exports/imports
   DataSources as XML (its "LogicModule" packaging format) rather than as a plain JSON object —
   confirm whether the caller has an existing DataSource XML definition to import (most common:
   adapting one already exported from the portal or LogicMonitor's module exchange) versus needing
   one authored from scratch. Authoring a new DataSource definition's collection/threshold logic
   from scratch is a significant task in its own right; this skill covers importing/registering the
   definition, not designing its collection method.
3. **Set each datapoint's threshold(s) you want to alert on**, within the DataSource XML, to the
   caller's requested value(s) and severity level(s) before import — do not import a definition
   with thresholds the caller didn't specify and expect to tune them afterward as part of this same
   procedure step.
4. **Import the DataSource.** Submit the XML definition to LogicMonitor's import endpoint. See
   `endpoints.md`. A successful import makes the DataSource available to be applied against
   matching devices (LogicMonitor's own device auto-discovery/AppliesTo logic determines which
   devices the DataSource actually monitors, based on the DataSource's own AppliesTo expression —
   confirm this expression matches the caller's intended device scope before import, since it is
   defined inside the XML itself, not as a separate API call).
5. **Confirm import** — report `CREATED` with the returned DataSource identifier on success. On
   failure, report `FAILED` with the response body verbatim.
6. **Create the Alert Rule that routes alerts this DataSource can now generate.** An Alert Rule
   matches incoming alerts by severity level, resource (device/group/name/property) filters, and
   LogicModule/datapoint filters, evaluated in ascending priority-number order against all defined
   rules until one matches — set `priority` deliberately if the caller has other alert rules that
   could otherwise intercept this alert first.
7. **Set the escalation target.** An Alert Rule references an escalation chain (by ID) that
   defines who is actually notified and via what channel — building a new escalation chain from
   scratch is out of scope for this skill (see `SKILL.md`'s "Known limitations"); use an existing
   chain ID the caller provides.
8. **Submit the create-alert-rule call.** See `endpoints.md`. Confirm success via the returned
   rule object; report `CREATED` with its identifier. On failure, report `FAILED` with the response
   body verbatim.

## Operational procedure — acknowledge an alert

1. **Confirm this is the intended action, not a resolve.** LogicMonitor's own documentation
   distinguishes acknowledging an alert (marking that specific alert occurrence as being handled,
   which suppresses further repeat notification of that occurrence) from Scheduled Downtime / SDT
   (which suppresses notification routing entirely for a device/instance/DataSource/website over a
   defined time window, regardless of which specific alert is involved). If the caller actually
   wants to silence a resource for planned maintenance rather than claim one active alert, that's
   SDT, not acknowledgment, and out of scope for this skill unless explicitly requested as separate
   monitor configuration.
2. **Provide an acknowledgment comment.** LogicMonitor's acknowledge-alert call requires a comment
   describing why/that the alert is being acknowledged — do not submit an empty or placeholder
   comment; use the reason the caller actually gave.
3. **Submit the acknowledge call** against the target alert's `id` (or `internalId`). See
   `endpoints.md`. Report `ACKNOWLEDGED` on success.
4. **There is no separate "resolve" call for a LogicMonitor alert.** Per LogicMonitor's own alert
   model, an alert clears on its own once the datapoint's value stops breaching its threshold for
   the DataSource's configured clear interval (the number of consecutive polling cycles required
   before LogicMonitor considers the condition genuinely resolved, mirroring the trigger interval
   used to raise the alert in the first place). Do not represent acknowledgment as resolving the
   alert, and do not fabricate a resolve endpoint the sources don't document — report
   that clearing happens automatically once the underlying condition normalizes.

## Patterns

- **Acknowledging suppresses repeat notification of one alert occurrence only** — if the same
  datapoint clears and re-breaches later, LogicMonitor treats that as a new alert occurrence,
  unacknowledged, per the sources.
- **Alert Rule priority is evaluated ascending, first match wins** — a rule with a numerically
  lower `priority` value that matches the same alert will claim it ahead of a later, more specific
  rule; order new rules deliberately relative to existing ones.

## Known limitations

- Authoring a brand-new DataSource's collection method (script, SNMP OID mapping, WMI query, etc.)
  from first principles is not covered — this procedure covers importing/registering a definition
  and setting its documented threshold fields, not designing new collection logic.
- Building a new escalation chain (the actual notification-delivery configuration an Alert Rule
  points to) is out of scope — see `SKILL.md`'s "Known limitations."
- The sources do not document a manual "resolve" or "clear" API call for
  an individual alert — see step 4 above; do not invent one.

## Tools

| Operation | Description | Category |
|---|---|---|
| Import DataSources from XML | Register/update the DataSource definition carrying datapoint thresholds | DataSources |
| Add Alert Rules | Create a rule that routes/escalates alerts matching severity/resource/datapoint filters | Alert Rules |
| Get Alert Rules | Confirm rule ordering/priority before adding a new one | Alert Rules |
| Acknowledge Alerts | Mark a specific active alert as being handled | Alerts |

## Verification checklist

- [ ] Confirmed whether the request needs a new DataSource (new detection condition) versus only a
      new Alert Rule against an existing DataSource's datapoints — not conflated
- [ ] Datapoint threshold severity/value set deliberately in the DataSource XML before import, not
      left at an imported default the caller didn't ask for
- [ ] Alert Rule `priority` set deliberately relative to existing rules
- [ ] Acknowledge call included a real, non-placeholder comment
- [ ] Acknowledge was not represented as resolving the alert — resolution is automatic and
      condition-driven
- [ ] Outcome reported using this skill's status vocabulary (`CREATED`, `ACKNOWLEDGED`, `FAILED`),
      with the response body verbatim on failure
