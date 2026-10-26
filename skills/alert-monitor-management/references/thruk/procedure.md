# Thruk — Host/Service Configuration & Problem Acknowledge Procedure

Creates or changes host and service configuration objects through Thruk's REST API and its
configuration tool, applies the change, and acknowledges or removes the acknowledgement of a host
or service problem on a Naemon-compatible monitoring core that Thruk fronts. Assumes an
authenticated client for the Thruk instance is already available; the documentation describes an
API key sent in a header as the preferred method and says basic authentication works but is not
recommended (see `endpoints.md`).

Sources (retrieved 2026-10-19): Thruk documentation, "REST API"
(https://www.thruk.org/documentation/rest.html); "REST API Commands"
(https://www.thruk.org/documentation/rest_commands.html); "REST API" examples
(https://www.thruk.org/documentation/rest_examples.html).

## Common Sequences

- **Stand up a new check:** create configuration object (host, then service) -> read pending diff ->
  (operator confirmation) -> save, check, reload.
- **Acknowledge a problem:** acknowledge host or service problem.
- **Release an acknowledgement:** (operator confirmation) -> remove acknowledgement.

Each step names a section below; follow that section for inputs, errors and gates.

## Operational procedure — create a host or service check

1. **Create the object with the generic configuration-objects call, not a per-object config call.**
   The documentation states that brand-new objects must be created this way, and that the
   per-object config calls only overwrite objects that already exist. The call takes two special
   parameters naming the object type (host or service) and the configuration file, plus the
   object's own attributes. Supply only what the caller specified.
2. **Review what changed.** Read the pending configuration diff. If it contains changes the caller
   did not ask for, stop and report them.
3. **Save, check, then reload — in that order, verifying the output of each.** Save writes the
   staged change to disk, check validates the configuration, reload applies it to the core.
   **Stop and confirm with the operator before saving and again before reloading**, because both
   steps apply every staged change, including those made by other users. If the check step
   reports errors, do not reload; discard the staged changes (revert) after confirming with the
   operator, and report `FAILED` with the check output verbatim.
4. **Report `CREATED`** once reload succeeds.
5. **To change an existing object**, use the per-object config call: one form replaces the whole
   object, another changes only the attributes sent. Prefer the partial form so unspecified
   attributes are not lost. **Deleting an object is irreversible once saved and reloaded: stop and
   confirm first.**
6. **Whether a service must name its host, and the exact attribute names for a service, are not
   stated** in the sources (assumption: the usual Naemon attributes apply). Check the
   documentation for the target core before sending.

## Operational procedure — acknowledge or remove an acknowledgement

1. **Identify the problem by host name, and by host plus service description for a service.**
2. **Acknowledging records that the problem is being worked on and does not clear it.** The state
   returns to OK only when a later check result is healthy. Do not represent acknowledgement as
   resolution.
3. **Submit the acknowledge command for the host or service.** A comment is required. Optional
   arguments are sticky, send-notification, persistent-comment and comment-author. Provide a real
   comment; do not submit an empty or placeholder value. The pages do not describe the effect or
   default of each option; defer to the Naemon external-command documentation the pages point to if
   the caller has not specified them. Report `ACKNOWLEDGED` on success.
4. **To remove an acknowledgement**, submit the matching remove-acknowledgement command (no
   arguments). **Stop and confirm with the operator first**, because notifications resume.
   Report `ACKNOWLEDGEMENT_CANCELLED` on success.
5. **There is no manual "resolve" call.** A problem leaves its non-OK state when a later check
   result is healthy; the pages document no call that forces it.

## Patterns

- **Staged changes are shared.** Save, check and reload act on everything staged, not just the
  caller's change; always read the diff first.
- **A generic command endpoint exists** that takes the command name, host, service and comment as
  form data, which avoids escaping problems in names containing special characters.

## Known limitations

- Rate limits, response bodies for creation, and error formats are not documented in the
  sources. Back off on an HTTP 429 or 5xx and honor any `Retry-After` header; report other
  errors verbatim.
- Thruk fronts a monitoring core; check execution and thresholds belong to that core's own
  configuration, which this procedure only reaches through Thruk.
- Contacts, groups, time periods and commands are out of scope.

## Tools

| Operation | Description | Category |
|---|---|---|
| Create configuration object | Stage a new host or service object | Configuration |
| Update or delete configuration object | Replace, partially change, or remove an existing object | Configuration |
| Read pending diff | Show staged configuration changes | Configuration |
| Save, check, reload | Persist, validate and apply the staged set | Configuration |
| Revert staged changes | Discard the staged set | Configuration |
| Acknowledge host or service problem | Record an acknowledgement | Commands |
| Remove host or service acknowledgement | Clear an acknowledgement | Commands |

## Verification checklist

- [ ] Object created with the generic create call, not an overwrite call
- [ ] The diff contained only the intended change before saving
- [ ] The operator confirmed before save and before reload; check passed before reload
- [ ] Acknowledgement carried a real comment and was not described as resolving the problem
- [ ] Removing an acknowledgement or deleting an object was confirmed first
- [ ] Outcome reported with this skill's status vocabulary and output verbatim on failure
