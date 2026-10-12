# Cisco Genie — Robot Suite Execution

Loads a testbed in a Robot suite, executes selected keywords, and reads the Robot result.

Sources (Cisco rolling documentation; retrieved 2026-10-09):

- [Genie Robot Framework Guide](https://pubhub.devnetcloud.com/media/genie-docs/docs/userguide/robot/index.html).
- [Unicon Robot Framework](https://pubhub.devnetcloud.com/media/unicon/docs/robot/index.html).

## 1. Prepare the keyword libraries

Genie's Robot support is optional. The environment includes the requested Genie, pyATS, and Unicon
Robot libraries before suite execution. [robot-endpoints.md](robot-endpoints.md) lists their exact
imports and an original suite. Success is importable libraries; missing imports or unknown keywords
remain harness setup errors and require the matching installed library documentation.

## 2. Define the suite

The suite loads the Genie testbed before connecting. Device names/aliases and connection selection
come from that testbed. A teardown disconnects the session. Success is a suite whose keyword names
and arguments match the installed keyword reference. The parse example proves only that collection
succeeds; any network-state assertion must be supplied separately.

## 3. Execute

**Before keywords or connection initialization change a live device: stop and confirm with the
operator before proceeding**, covering setup, triggers, configuration, and teardown actions.

```bash
robot suite.robot
```

Success is a Robot run with the intended tests and its generated report/log. Missing parser support,
keyword errors, and connection failures remain failing or erroneous test evidence. The cited guide
does not supply universal network error messages or retry intervals.

## 4. Read results

Robot's native results and per-keyword evidence determine completion. Genie exposes profile and
comparison keywords as well as trigger/verification keywords, but their device/mapping inputs
remain required. A failed profile comparison remains a failed comparison; this procedure does not
invent exclusions or replace it with an AEtest status ordering.

## Patterns

The test format changes to Robot keywords; the device/connection and underlying operation effects
remain those of the selected library. Importing multiple keyword libraries is documented.

## Known limitations

- A mock or captured-output test does not prove live network correctness.
- Available keywords and parser/model coverage depend on installed packages and platform.
- Source examples contain malformed Settings headings in places; this reference uses Robot's
  complete section delimiter rather than reproducing the typo.

## Tools

| Mechanism | Description | Category |
|---|---|---|
| Local Robot runner | Execute a suite through the imported keyword libraries | Test harness |

## Verification checklist

- [ ] Library imports and keyword resolution succeeded.
- [ ] Testbed and connection selection match the request.
- [ ] Test/teardown results and the Robot report were inspected.
