# Cisco XPRESSO — Run One Registered Job

Submits a single registered job/profile and reads its execution results.

Sources: Cisco XPRESSO rolling documentation, retrieved 2026-10-09:
[Configuring and Executing Job Requests](https://developer.cisco.com/docs/xpresso/configuring-executing-job-requests/)
and [Viewing Job Test Results](https://developer.cisco.com/docs/xpresso/viewing-job-test-results/).

## 1. Open the job

From Execution → Jobs, the selected registered job's Run DEFAULT action opens the request wizard.
Success is the intended job/profile in that wizard; the procedure assumes registration already exists.

## 2. Resolve execution inputs

The wizard contains request options, profile information, profile options, resources, Clean,
and arguments. The resource selection determines eligible testbeds; executing on all testbeds
expands the run beyond the first available one. Success is the intended resolved selection.
Missing resources require correcting the registered job, outside this procedure.

## 3. Submit

**Before the run, Clean, or associated hooks change live state or send notifications: stop and
confirm with the operator before proceeding.** Submission creates an identified request and queues
it for resources. Request creation is not test completion. The cited wizard description does not
name the final submit button; its label must be checked in the installed version.

## 4. Inspect results

Execution → Requests exposes the request by ID. Expanding it shows profiles; opening its details
provides results and logs. Queued/Running remain pending. Failed, Stopped, Errored, or Expired
require their recorded reasons; Passed remains the platform's reported result. Expiry can end a
run before all tests execute.

## Patterns

A request ID connects submission to its results; retries create separate runs and are not inferred.

## Known limitations

Deployment, job registration, scheduling, bundles, baselines, and group administration are excluded.


## Tools

| Mechanism | Description | Category |
|---|---|---|
| Authenticated XPRESSO UI | Submit and inspect a registered job request | Browser |

## Verification checklist

- [ ] Job/profile/resources match the request.
- [ ] Request ID and actual terminal state were recorded.
- [ ] Test results and incomplete sections were inspected.
