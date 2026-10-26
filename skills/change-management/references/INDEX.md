# Change Management — Platform Index

One row per supported ITSM/change-management platform. Each platform directory holds its own
`procedure.md` (the full step-by-step), plus wire-level `endpoints.md`.

| Platform | Directory | Scope | Notes |
|---|---|---|---|
| ServiceNow | `servicenow/` | Create, update, approve/reject, gate-check, close a change request via `sn_chg_rest` | Gate-check is the only source of truth for close-readiness; close requires operator confirmation; approve/reject and state-changing updates do too unless the operator's standing instructions pre-authorize them |
| Freshservice | `freshservice/` | Create, view/list, update, move, delete, notes, and full approval/approval-group/approval-chain management via API v2 `/api/v2/changes` | **Cannot approve/reject via API at all** — only cancel a pending approval. Approve/reject is exclusively the approver's own action in the product. No gate-check endpoint; `status` is a plain field the caller must sequence responsibly. |
| Jira Service Management | `jira-service-management/` | Create, status/history, discover-then-perform transitions, and approval observation/answering on a customer request configured as a change | **No dedicated change object** — a change request is just a customer request against a service-desk-configured request type; confirm the right `serviceDeskId`/`requestTypeId` per instance. Approve/decline is API-capable but assignee-only, one-shot (no re-decision, no approve-on-behalf) — a third variant distinct from both ServiceNow's full API approve/reject and Freshservice's cancel-only. |
| BMC Helix ITSM | `bmc-helix-itsm/` | Search, retrieve by ID, and partial-update a change request via the simplified REST API (`com.bmc.dsm.itsm.itsm-rest-api`) | BMC recommends this API over the older generic platform REST API. **No gate-check/transition-discovery mechanism is documented in the sources** — a fourth variant (ServiceNow: explicit gate-check; Freshservice: plain field, no gate; Jira: transitions discoverable; BMC: no discovery mechanism documented). Status-code values are instance/field-specific, not universal. |

There is no single cross-vendor standard here the way RFC 1035 grounds DNS — ITIL describes change
management as a *practice*, not a wire protocol, so each platform's procedure is drawn entirely from
that platform's own API, not a shared spec. `SKILL.md` therefore states practice-level concepts (states,
approval, gating) that are common ITSM vocabulary, not RFC-derived universal rules.

**Approval and gating are not symmetric across platforms.** Do not assume every platform supports
approve/reject as symmetric operations with gated state transitions. Freshservice has no gate-check
endpoint (`status` is a plain field with no transition-validation call) and cannot approve/reject via
API at all (only cancel). Check the target platform's row before assuming any approval or gating
capability.

**Four different transition/approval models exist across these platforms:**
- **Transition discovery, without a readiness gate:** Jira exposes "get available transitions" (so
  the caller isn't guessing IDs) but doesn't validate *readiness* to reach any particular one the way
  ServiceNow's gate-check does — it just lists what the workflow currently permits.
- **No discovery mechanism at all:** BMC's simplified REST API documents no "what transitions/states are
  available" call in the sources — the caller is expected to know the target instance's
  configured status values already.
- **Approve/reject as a third variant, not a second:** ServiceNow (full API approve/reject),
  Freshservice (cancel-only, no approve/reject), and Jira (API-capable approve/decline, but
  strictly assignee-only and one-shot — no re-decision, no approve-on-behalf) are three meaningfully
  different capability shapes, not a binary "can/can't." Check the specific platform's row, not a
  generalized assumption from any other platform in this table.
