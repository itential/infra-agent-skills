# Centreon — Host/Service Check Creation & Problem Acknowledge Procedure

Creates a monitored host and a service check on a self-hosted Centreon platform through its REST
API v2, applies the configuration to the poller, and acknowledges or cancels the acknowledgement of
a host or service problem. Assumes an authenticated client holding a Centreon API token is already
available (see `endpoints.md` for how the token is obtained and sent). Centreon's own API reference
states that the configuration create calls behave differently on Cloud environments and points to a
separate Cloud API document; this procedure covers the on-premises behavior only.

Sources consulted (retrieved 2026-10-19): Centreon REST API v2 OpenAPI definition, version 25.10
(https://raw.githubusercontent.com/centreon/centreon/refs/tags/25.10-latest/centreon/doc/API/centreon-api.yaml
and the `latest/onPremise` files it references); Centreon documentation, "REST API v2"
(https://docs.centreon.com/docs/api/rest-api-v2/). Secondary source, flagged: the OpenAPI copy in
the `itential/assets` repository was used only to choose which operations to cover.

## Operational procedure — create a host and a service check

1. **Confirm the target monitoring server exists** and note its ID. A host is always attached to
   one monitoring server (poller); creating monitoring servers is out of scope.
2. **Create the host.** Supply the monitoring server ID, a host name and an address; optionally
   supply check settings (check command and arguments, check period, attempt count, intervals,
   notification settings) and host templates, groups or categories by ID. Supply only what the
   caller specified. On success Centreon reports the object as created. A conflict response means a
   host with that name already exists: report `REJECTED_DUPLICATE` and do not retry blindly.
3. **Create the service check.** Supply the service name and the ID of the host from step 2;
   optionally supply a service template, check command and arguments, check period, attempt count
   and intervals. The service's alerting behavior comes from these check settings and from its
   template — do not invent thresholds the caller did not ask for. A conflict response means the
   service already exists on that host.
4. **The new objects are not yet live.** Centreon holds configuration changes until the monitoring
   server's configuration is generated and the poller reloaded. **Stop and confirm with the
   operator before generating and reloading**, because the reload applies every pending
   configuration change on that poller, not only the ones just created.
5. **Generate and reload the monitoring server's configuration.** Success is an empty
   confirmation response. Report `CREATED` once this succeeds. If generation or reload fails,
   report `FAILED` with the response body verbatim; the created objects remain in the
   configuration and are not rolled back automatically (the sources document no rollback call).
6. **Do not report an alert state as a creation failure** before the check has run at least once
   on its configured interval.

## Operational procedure — acknowledge or cancel an acknowledgement

1. **Identify the problem by its host ID (and service ID for a service problem).**
2. **Acknowledging marks the problem as being worked on and does not clear it.** The status
   returns to OK only when a later check result is healthy. Do not represent acknowledgement as
   resolution.
3. **Choose the options deliberately.** The service acknowledgement accepts a comment, and flags
   for notifying contacts, keeping it sticky, and keeping the comment persistent. Provide a real
   comment describing why; do not submit an empty or placeholder value. The sources do not state
   the default of each flag when omitted — consult the platform's reference if the caller has not
   specified them.
4. **Submit the acknowledgement.** Centreon answers with a "command sent" confirmation: the
   acknowledgement is queued to the monitoring engine, not yet confirmed as applied. Report
   `ACKNOWLEDGED` on that response and confirm by reading the problem's acknowledgement list if the
   caller needs certainty.
5. **To cancel**, submit the cancel-acknowledgement call for the same host or service. **Stop and
   confirm with the operator first**, because cancelling resumes notifications for a problem
   someone was handling. Report `ACKNOWLEDGEMENT_CANCELLED` on the "command sent" response.
6. **There is no manual "resolve" call.** A problem leaves its non-OK state when a later check
   returns a healthy result; the sources document no API call that forces this. Say so rather than
   inventing an endpoint.

## Patterns

- **Reload is the commit step.** Creating configuration objects and applying them are separate
  calls; a created-but-not-reloaded host is invisible to monitoring.
- **Host acknowledgement body fields are unverified.** The service acknowledgement body fields are
  stated in the API definition; the host acknowledgement's fields could not be confirmed from the
  sources consulted (assumption: it mirrors the service call). Check the platform's reference
  before relying on any flag for a host.

## Known limitations

- On-premises behavior only; the create calls differ on Cloud.
- Monitoring server (poller), command, template and timeperiod creation are out of scope; they are
  referenced by ID.
- No documented rollback for created configuration, and no documented manual resolve.
- Rate limits, and the exact error bodies for 400/403/404/500 responses, are not documented in the
  sources consulted: treat a 429 or 5xx as retryable with backoff, and surface other errors verbatim.

## Tools

| Operation | Description | Category |
|---|---|---|
| Authenticate | Exchange credentials for an API token | Session |
| Create host | Add a host configuration to a monitoring server | Configuration |
| Create service | Add a service check to a host | Configuration |
| Generate and reload monitoring server configuration | Apply pending configuration on the poller | Configuration |
| Acknowledge host problem | Queue an acknowledgement for a host | Monitoring |
| Acknowledge service problem | Queue an acknowledgement for a service | Monitoring |
| Cancel acknowledgement | Queue removal of a host or service acknowledgement | Monitoring |
| List acknowledgements | Confirm acknowledgement state | Monitoring |

## Verification checklist

- [ ] Monitoring server existed and its ID was used for the host
- [ ] Host and service creation both returned a created response
- [ ] The operator confirmed before the poller reload
- [ ] Generate-and-reload returned success; the objects were not reported live before that
- [ ] Acknowledgement carried a real comment and was not described as resolving the problem
- [ ] Cancelling an acknowledgement was confirmed with the operator first
- [ ] Outcome reported with this skill's status vocabulary and the response body verbatim on failure
