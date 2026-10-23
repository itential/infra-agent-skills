# Cloudflare One CASB — Posture and Content Findings Assessment

Read the security findings Cloudflare CASB has recorded against connected SaaS and cloud
integrations, and report each one with its supporting evidence. Source: Cloudflare Docs "Cloud and
SaaS findings", "Manage findings", "Troubleshoot CASB", and the CASB API reference for findings,
finding instances, content findings, finding types, and integrations (retrieved 2026-10-23).

This is a read-only, diagnostic procedure. It maps a question ("what is exposed," "why does this
finding exist," "why is a finding stale") to a documented lookup and a documented interpretation.
It changes nothing on the platform. Dashboard-only steps are not covered; bind each lookup through
`endpoints.md`.

## Vocabulary

- **Finding type:** a definition of one issue CASB detects, for one vendor and asset class. It may
  apply to several integrations.
- **Posture finding:** the roll-up of one finding type within one integration. The same finding type
  appears as separate findings for separate integrations.
- **Finding instance:** one occurrence of a posture finding on one asset.
- **Content finding:** a record for a single asset in a single integration, listing each DLP profile
  that asset matched. It lives in its own list, apart from posture findings, with no finding type
  above it.
- **Severity:** Critical, High, Medium, or Low, from most to least urgent. The platform pairs these
  with a response window running from the same day for Critical to routine review for Low, so use
  severity to order triage.
- **Observation type:** Issue, Insight, or Activity. **Product:** SaaS or Cloud. **Origin of a
  finding type:** system-managed or customer-created.

## Common Sequences

1. **Triage the estate:** check preconditions → list findings (active only, highest severity first;
   get a finding for its counts) → for each one that matters, get its finding type for the threat, impact, and remediation
   guidance → list its instances for the affected assets.
2. **Assess one integration or one asset:** list findings filtered to the integration → list
   instances of the relevant finding, filtered to the asset IDs.
3. **Report data-exposure matches:** list content findings (optionally filtered to a DLP profile or
   integration) and report the assets and the profiles they match.
4. **Explain a stale, missing, or doubtful finding:** follow "Diagnose an unexpected result" below.

## Step 0: Preconditions

1. Confirm the target integration exists and is scanning: get the integration and check that it is
   not paused and that its status is healthy. An integration that has just been connected can take
   several hours to produce its first findings.
2. Confirm the plan allows what is being asked. Free-tier accounts are documented as limited to two
   integrations, and as unable to view the details of a finding instance. If instance details are
   refused or empty on a free account, report the plan limit rather than "no findings."
3. Confirm the API token carries a Zero Trust read permission (write also works). Behavior for a
   token without it is not documented; report the response body.

Success: the integration is present, not paused, and a finding list call returns a success response.

## Find findings

List findings. Useful filters, all optional: severity, observation type, product (SaaS or Cloud),
type (posture or content), vendor, integration, finding type IDs, an ignored flag, date bounds on
when the issue occurred, and free-text search. Order by severity, instance count, or latest
occurrence date.

Read each result as: the finding type (name, vendor, category, default severity, origin), the
integration it was found in, the count of active instances and of archived instances, and whether it
has been ignored.

- The list returns ignored findings as well unless the ignored flag is set to false. State whether
  the report is active-only or includes ignored ones.
- The severity on a finding type is a default. An integration-level override can exist, so when a
  severity decides priority, quote it from the finding and say it is the level reported for that
  integration (assumption: the reported level reflects any override; the documentation labels the
  type-level value as the default used when no override exists).
- Results page by page or by cursor. Follow the pagination fields until all results are read before
  stating a total.

Success: each finding in the answer cites its type name, integration, severity, and active count.

## Explain a finding type

If only a vendor or name is known, list finding types filtered by vendor to find the ID. Then get
the finding type. It carries a description, the vendor and asset class, whether it applies to
all integrations, its origin, how many active instances exist account-wide, and a remediation block
with threat, impact, remediation guidance text, and the compliance frameworks it relates to. Use the
threat, impact, and frameworks to explain why a finding matters; quote the guidance as the
platform's own, not as a verified fix.

A custom finding type carries the detection expression customers wrote; a system type carries the
platform's own. Do not treat a custom type's severity or wording as platform-vetted.

## List affected assets

List instances of one finding (use the finding's own identifier, not the finding type's). Filters:
archived or not, asset IDs, instance IDs, date bounds, remediation status, and search. For each
instance (get one for its full asset detail), report the asset (name, type, vendor and service, external ID, the asset's own field
list, and its link when present), the date the issue was identified, any DLP context, the most
recent remediation jobs, and the latest webhook delivery per configured destination.

Remediation job status is one of: pending, processing, validating, completed, failed (and, in the
dashboard, rejected for insufficient integration permissions). Validation after a fix can take up
to 48 hours, so a validating instance is not yet confirmed fixed. A remediation job flagged stale predates the
instance's current identification date, so it says nothing about the present state.

Success: every instance reported carries the asset identity and the identification date.

## Report content findings

List content findings. Each result is one asset with its DLP contexts: the profile ID, entry IDs,
when the context was created, updated, or deleted, and the match boundaries.

Content findings and instances can include the matched data itself in a match-context payload. Treat
that payload as sensitive (assumption: it holds the text that matched the DLP profile, which the
documentation does not spell out). Report the asset, profile, and entry IDs; leave the payload out
of summaries and logs unless the operator explicitly asks for it.

## Diagnose an unexpected result

- **A fixed issue still shows as active.** The platform scans periodically, not continuously: the
  first scan takes hours, and the documentation gives differing intervals for later scans (about
  1 to 24 hours in the overview, about 24 to 48 hours in the troubleshooting guidance). Treat a lag
  of up to 48 hours as normal and report the observed last-scan time. Check the integration
  status and pause flag, and the instance's remediation status (validating can last up to 48
  hours). Forcing an immediate rescan is a dashboard action by an operator and is not available
  here.
- **No findings, or far fewer than expected.** Check the filters first (a leftover ignored, severity,
  vendor, or date filter hides results), then integration status and pause flag, then whether the
  first scan has finished, then plan limits (Step 0).
- **A finding looks wrong.** Compare the instance's asset fields and link against the source
  system before trusting it; CASB can misjudge an asset. Known false positives: internal-only
  files labeled public, and archived Google Workspace accounts labeled inactive. Report the
  finding as doubtful with its evidence; vendor support asks for the finding ID. Ignoring or hiding a finding
  is a change and is out of scope here.
- **Remediation shows failed or rejected.** Report the status. Documented causes: a revoked or reduced grant on the
  connected app (a one-click remediation may then fail with a timeout error); Rejected means the
  integration lacks the permissions to remediate, and remediation requires read-write mode; and
  access inherited from a parent folder or shared drive blocks the child, with the platform showing
  a message that the resource has inherited permissions. Re-validating the integration or fixing the permission at
  its source is an operator action.
- **One finding type appears several times.** That is expected: one posture finding exists per
  integration.

## Patterns

- Quote counts with their meaning: active instances, archived instances, and total instances are
  separate numbers.
- A finding's list identifier and its finding-type identifier are different values. The instance
  lookup takes the list identifier (assumption: the identifier carried on the finding list result
  itself; the documentation does not say which field feeds the path parameter).
- Hidden instances and ignored findings are suppression states chosen by an operator, not
  resolution. Do not report them as fixed.
- Prefer filters over reading the full list when the estate is large.

## Known limitations

- Read-only. Ignoring or hiding findings, changing severity, archiving instances, exports, remediation
  jobs, and webhook sends are writes and are not covered here (remediation and webhook policy
  management are separate).
- The posture API covers the finding types the platform ships for its supported integrations. It
  does not expose shadow-IT discovery, OAuth-grant scoring, or an application risk score.
- Not documented: rate limits and quotas, maximum page size, exact error codes, and behavior on
  accounts without CASB. On HTTP 429, back off and honor any `Retry-After` header.
- Findings are as of the last scan, not live.

## Tools

| Operation | Description | Category |
|---|---|---|
| List findings | Posture and content findings with filters and counts | Read |
| Get finding | One finding with its type and integration | Read |
| List finding instances | Affected assets for one finding, with remediation status | Read |
| Get finding instance | One affected asset in full | Read |
| List content findings | Assets matching DLP profiles | Read |
| Get finding type | Definition, threat, impact, guidance, frameworks | Read |
| List finding types | Find a finding type ID, filterable by vendor | Read |
| Get integration | Status and pause state of one connected integration | Read |
| List integrations | Connected integrations, filterable by vendor | Read |

## Verification checklist

- [ ] Integration confirmed present, not paused, and healthy before reporting an absence of findings
- [ ] The report states whether ignored findings and archived instances were included
- [ ] Each finding is reported with type name, integration, severity, and active count
- [ ] Each affected asset is reported with its identity and the date the issue was identified
- [ ] All result pages were read before any total was stated
- [ ] Remediation status reported as the platform states it; "validating" not reported as fixed
- [ ] Any match-context payload left out of the report unless explicitly requested
- [ ] No write call was made
