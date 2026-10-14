# Prisma SD-WAN — Site Snapshot Capture and Redeploy

Capture a site's configuration as a YAML file, follow the job, retrieve the file, and redeploy a YAML
file to create a site or refresh an existing one, on Prisma SD-WAN through the unified API (site
snapshot operations).

Written against the Prisma SD-WAN Administrator's Guide (2026 edition) and the Prisma SD-WAN unified
API specification (version listed as "Latest"), checked 2026-10-14. The sources are thin on job states and
on what a capture leaves out; this file says so where it matters. Covers site-level snapshots only.
Device-level snapshots (a UI action in the device replacement flow), site templates in Jinja form, and
bulk site-template deployment are different features and out of scope.

Assumes an authenticated API client is available. The specification says a token must be used for one
profile read right after it is minted, or later SD-WAN calls return 403; this is wiring handled by the client setup, not by the agent's steps, and is in `endpoints.md`.

## Common Sequences

Steps marked (gated) contain an operator confirmation. Every sequence starts with a freshly minted token's one profile read
(wiring in `endpoints.md`), which is not repeated below.

- **Back up a site:** *Capture a site snapshot* → *Check a capture job* until it ends → *Retrieve the
  snapshot file* → store the file (storage is the caller's concern).
- **Refresh or recreate a site from a saved file:** *Check the file's required fields* → *Redeploy a site
  snapshot* (gated) → *Check a redeploy job* until it ends → confirm the site.
- **Review history:** *List captures* or *List redeploys*.

## Status vocabulary

| Status | Meaning |
|---|---|
| CAPTURED | The capture job ended successfully and the file was retrieved |
| IN_PROGRESS | The job has not reached an end state |
| DEPLOYED | The redeploy job ended successfully |
| WARNING | The redeploy job reports a warning: the site may exist while a later step (attaching the device, for example) did not complete. Report the status description |
| NOT_ALLOWED | The site holds only a device shell, so capture is refused |
| DECLINED | The operator did not confirm |
| FAILED | The job ended failed, or the platform returned an error. Include the status description or error |

Stop rule: when a job status is neither a documented failure or warning nor recognisably a finished success (the sources give no success string), report the raw status and description and ask the operator; do not report CAPTURED or DEPLOYED on a guess.

The platform returns job status as free text with a separate description. The sources name only
"warning" and "failed" as values; the strings for in-progress and success are not stated (unverified).
Map them from the returned values and report the raw status and description alongside.

## Operations

### Capture a site snapshot

Starts an asynchronous export of one site's current configuration to YAML, optionally with a snapshot
name.

Binds to: generate_site_snapshot (site identifier, optional name).

- Documented precondition: the site must be either fully provisioned with a device or entirely empty. A site
  holding only a device shell is refused; report NOT_ALLOWED (the error text is in `endpoints.md`).
- Success: the response carries a job identifier with status and description. That is acceptance only;
  continue with *Check a capture job*.
- The platform lists an already-in-progress error code for capture (its meaning is inferred from the name); if a request is rejected with it, wait for the running job instead of repeating. Whether a repeat after completion makes a second copy is not stated (unverified).
- The sources do not state what the capture leaves out (unverified). Treat the file as a site
  configuration copy, not proof that every setting, secret, or device-local value is included.

### Check a capture job

Binds to: read_snapshot_job_status (site identifier, job identifier).

- Repeat until the status is an end state. The polling interval and timeout are not stated; back off
  between polls and stop polling after a period the operator accepts (assumption).
- A warning status on a capture job (the guide says either job type can show one) is reported with its description; ask the operator how to proceed.
- A failed status is reported with its description. The description is the only documented diagnostic.

### Retrieve the snapshot file

Binds to: retrieve_snapshot_yaml (site identifier, job identifier).

- Success: the response carries the YAML text along with status and the snapshot name. Report CAPTURED
  only when the job status ended successfully and the YAML text is present.
- The file holds literal values. The guide's route for changing any is to edit a local copy and import it; this skill does not edit configuration.
- Handle the file as sensitive (assumption; see Patterns).

### List captures

Binds to: query_snapshot_exports (optional paging and filters).

- Returns past capture jobs with site, name, status, and description. The filter and sort fields are
  described only as generic query parameters; their accepted values are not stated (unverified). Send at least one paging field such as a limit; an empty body may be rejected with an empty-input error (see `endpoints.md`).

### Check the file's required fields

No call; a local check.

Before a redeploy, confirm the YAML carries four mandatory values under the site's address block: name, city,
country, and software release. The guide says an import lacking any of them fails. The deployment job is
tracked under the site name written in the file.

### Redeploy a site snapshot

Submits a YAML file to create a site, or to redeploy a site whose name already exists.

Binds to: create_site_deployment (YAML text).

**Stop and confirm with the operator before submitting.** State the site name found in the YAML. No bound operation reads sites, so whether a site of that name already exists is outside this procedure: ask the operator, and say that it was not checked if they do not know. For a name that already belongs to a site, the guide says the outcome is a retry, a redeploy, or a new job, without saying which applies or what changes on the live site (unverified). If the operator declines, report DECLINED and make no call.

- Success: the response carries a job identifier with status and description. That is acceptance only;
  continue with *Check a redeploy job*.
- A rejected request carries error entries with codes (listed in `endpoints.md`); report FAILED with them. The site-address-missing and YAML-syntax codes likely mean the file needs fixing, and the in-progress code likely means wait (all inferred from the code names).
- There is no documented dry run and no documented undo. Author's recommendation, not from the sources: if the operator says the site already exists and is eligible, offer a capture first so a prior copy is on hand; do not capture without their agreement.

### Check a redeploy job

Binds to: read_site_deployment (job identifier).

- Repeat until an end state. Report DEPLOYED, WARNING, or FAILED with the status description.
- On WARNING the site may have been created while a follow-up step, such as attaching hardware, failed. Do not treat it as success; hand the description to the operator.

### List redeploys

Binds to: query_site_deployments (optional paging and filters).

- Returns past redeploy jobs with YAML name, status, and description. Filter details are unverified as
  for *List captures*.

## Patterns

- **Accepted is not done.** Both capture and redeploy return a job; only its end state counts.
- **Site name is the identity of a redeploy.** The platform keys the job on the name in the YAML, so a
  file edited for a different site but left with the old name targets the old site (inferred from the guide's statement that the name is taken from the YAML).
- **A restore here is a redeploy.** The sources describe redeploying a YAML file; they do not describe a
  separate restore operation or a rollback to a prior state. A restore of an existing site is therefore
  a gated redeploy whose exact effect is unverified.
- **Shell-only sites are excluded.** Capture is refused for a site holding just a device shell; attach
  hardware first or capture an empty site.
- **Sensitive content (assumption).** The sources do not say whether credentials or keys appear in the
  file. Keep it out of tickets and chat, and apply the operator's own storage rules.
- **Authentication.** Tokens expire and the profile read is required after minting; see `endpoints.md`.
  Rate limits are not stated; on an HTTP 429 back off and honor any `Retry-After` header.

## Known limitations

- Site-level only; device snapshots, Jinja site templates, and bulk template deployment are not covered.
- Job status strings, capture exclusions, query filter values, and the effect of redeploying onto an
  existing site are unverified.
- No scheduling, retention, or comparison of copies.
- Redeploy has no documented undo.

## Tools

| Operation | Description | Category |
|---|---|---|
| generate_site_snapshot | Start a site configuration export | Write (creates a job) |
| read_snapshot_job_status | Read a capture job's status | Read |
| retrieve_snapshot_yaml | Read a capture's YAML and status | Read |
| query_snapshot_exports | List capture jobs | Read |
| create_site_deployment | Submit YAML to create or redeploy a site | Write (gated) |
| read_site_deployment | Read a redeploy job's status | Read |
| query_site_deployments | List redeploy jobs | Read |

## Verification checklist

- [ ] The site was not a shell-only site before capture (or NOT_ALLOWED was reported)
- [ ] Capture job reached an end state before the file was relied on, and the YAML text was present
- [ ] YAML carried the four mandatory address values before any redeploy
- [ ] Operator confirmed the redeploy, naming the site and what is known about whether it already exists
- [ ] Redeploy job end state read and reported with its description; WARNING not reported as success
- [ ] Raw status and description reported alongside the mapped status
