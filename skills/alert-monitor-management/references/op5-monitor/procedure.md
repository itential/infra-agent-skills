# OP5 Monitor — Host/Service Check Creation & Problem Acknowledge Procedure

Creates a host and a service check on an OP5 Monitor server through its configuration REST API,
saves the pending changes so they take effect, and acknowledges a host or service problem through
the external-command API. Assumes an authenticated client for the target OP5 Monitor server is
already available; the sources consulted show HTTP basic authentication with a username and
password and JSON request bodies (see `endpoints.md`).

Sources consulted (retrieved 2026-10-19): ITRS Group knowledge base, "OP5 Monitor - How to
configure monitoring objects REST API"
(https://docs.itrsgroup.com/docs/faq/zendesk/articles/360020252273-OP5-Monitor-How-to-configure-monitoring-objects-REST-API);
ITRS Group knowledge base, "Creating an HTTP API driven command-line tool"
(https://docs.itrsgroup.com/docs/faq/op5/360020055294-op5-monitor-creating-an-http-api-driven-command-line-tool/index.html).
Secondary source, flagged: the OpenAPI copy in the `itential/assets` repository was used only to
choose operations. Command parameter names beyond those shown on the pages above, and the
acknowledgement-removal command, were not confirmed from a primary page (see Known limitations).

## Operational procedure — create a host and a service check

1. **Choose the configuration file location and a template for each object.** The host and the
   service each need a file location (the sources show the standard host and service
   configuration files) and a template reference. Templates can supply required settings, which
   keeps the create calls short. Do not substitute a template the caller did not name.
2. **Create the host.** Supply file location, host name and template; any other setting is either
   set on the object or inherited from the template (examples named in the sources: maximum check
   attempts, notification interval, notification options, notification period). Setting names
   match those in the web interface.
3. **Create the service check.** Supply file location, host name, service description, check
   command and service template. Supply only what the caller specified; do not invent thresholds
   or intervals.
4. **Review pending changes if the caller wants to inspect them.** Creation only stages the
   change; nothing is live yet.
5. **Save the pending changes.** Saving exports the configuration so it takes effect.
   **Stop and confirm with the operator before saving**, because saving applies every pending
   change in the staged set, including changes other users staged. Report `CREATED` when the save
   succeeds. If the caller changes their mind before saving, discard the staged set; the sources
   describe this as equivalent to the interface's undo and it likewise discards all pending
   changes, so confirm that too.
6. **Do not report an alert state as a creation failure** before the check has run at least once
   on its interval.

## Operational procedure — acknowledge a problem

1. **Identify the problem by host name, and by service description for a service problem.**
2. **Acknowledging records that the problem is being worked on and does not clear it.** The state
   returns to OK only when a later check result is healthy. Do not represent acknowledgement as
   resolution.
3. **Choose the options deliberately.** The host command takes the host name, a comment, and
   sticky, notify and persistent options; the service command additionally takes the service
   description. Provide a real comment describing why. The sources show the sticky option set to
   `1` and the notify and persistent options set to true in their examples, but do not describe
   what each does when changed, or their defaults: consult the platform's own command help
   (`help/command` on the server, as the sources point out) if the caller has not specified them.
4. **Submit the acknowledgement command.** Report `ACKNOWLEDGED` on a success response.
5. **Removing an acknowledgement is not covered by the sources consulted.** Do not guess a command
   name; consult the server's own command help page and confirm with the operator first.
6. **There is no manual "resolve" call.** The sources document no call that forces a state change;
   a problem leaves its non-OK state when a later check result is healthy. The external-command
   interface also lists submitting passive check results, but that applies to passively fed checks
   and is outside this procedure.

## Patterns

- **Create then save is a two-stage commit.** A host created but not saved is not monitored.
- **Output format.** The sources note the JSON response can be returned as XML by a query option;
  keep JSON for this procedure.

## Known limitations

- Acknowledgement removal, rate limits, error response bodies and how a failed save reports the
  problem are not documented in the sources consulted. Back off on an HTTP 429 or 5xx and honor
  any `Retry-After` header; report other errors verbatim.
- Parameter names for commands other than the two acknowledgement commands are not covered.
- Contact, contact group, host group and time period management are out of scope.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create host | Stage a new host configuration object | Configuration |
| Create service | Stage a new service check object | Configuration |
| List pending changes | Show staged configuration changes | Configuration |
| Save pending changes | Export the staged set so it takes effect | Configuration |
| Discard pending changes | Drop the staged set | Configuration |
| Submit acknowledge-host-problem command | Record an acknowledgement for a host | Commands |
| Submit acknowledge-service-problem command | Record an acknowledgement for a service | Commands |

## Verification checklist

- [ ] File location and template were supplied for both objects
- [ ] The operator confirmed before saving or discarding the staged set
- [ ] Save succeeded before the objects were reported live
- [ ] Acknowledgement carried a real comment and was not described as resolving the problem
- [ ] No acknowledgement-removal command was guessed
- [ ] Outcome reported with this skill's status vocabulary and the response body verbatim on failure
