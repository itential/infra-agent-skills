# Endpoint Wiring — Jira Service Management Change Request Lifecycle

Literal API calls behind each capability named in `procedure.md`. Base URL:
`https://<site>.atlassian.net`. Auth: OAuth 2.0 (3LO) with the scopes noted per endpoint, or basic
auth with an API token for server/data-center deployments. Sourced from Atlassian's own machine-
readable OpenAPI spec (`https://developer.atlassian.com/cloud/jira/service-desk/swagger.v3.json`),
retrieved directly.

## Create a Customer Request

Tool hint: `POST /rest/servicedeskapi/request` — OAuth scope `write:servicedesk-request`.

Body fields: `serviceDeskId` (string), `requestTypeId` (string), `requestFieldValues` (object, keyed
by field ID), `form.answers` (object, for form-based request types), `raiseOnBehalfOf` (string,
permission-gated), `requestParticipants` (array of account IDs, permission-gated),
`isAdfRequest` (boolean).

Example:
```json
{
  "form": {
    "answers": {
      "1": {"text": "Answer to a text form field"},
      "2": {"date": "2023-07-06"}
    }
  },
  "isAdfRequest": false,
  "requestFieldValues": {
    "description": "I need a new *mouse* for my Mac",
    "summary": "Request JSD help via REST"
  },
  "requestParticipants": ["qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d69abfa3980ce712caae"],
  "requestTypeId": "25",
  "serviceDeskId": "10"
}
```

## Get Request Status

Tool hint: `GET /rest/servicedeskapi/request/{issueIdOrKey}/status`.

Query params: `start` (pagination offset, base 0), `limit` (page size, default 50).

Response is paginated; `values[]` entries carry `status` (string) and `statusDate` (an object with
`epochMillis`/`friendly`/`iso8601`/`jira` representations), most recent first.

## Get Customer Transitions

Tool hint: `GET /rest/servicedeskapi/request/{issueIdOrKey}/transition`.

Returns the list of transitions currently available on the request, each with an `id` to use in
Perform Customer Transition.

## Perform Customer Transition

Tool hint: `POST /rest/servicedeskapi/request/{issueIdOrKey}/transition` — OAuth scope
`write:servicedesk-request`.

Body: `{"id": "<transition-id>", "additionalComment": {"body": "<optional comment>"}}`.

Response: `204 No Content` on success.

Documented errors: `400` — "transition ID is invalid or the comment is too long"; `401` — not logged
in; `403` — "user does not have permission to complete this request" (requires Transition Issues
permission, plus Add Comments if a comment is included); `404` — request doesn't exist; `500` —
internal server error.

## Get Approvals

Tool hint: `GET /rest/servicedeskapi/request/{issueIdOrKey}/approval` — OAuth scopes
`read:request.approval:jira-service-management`, `read:user:jira`.

Response schema: `PagedDTOApprovalDTO` — a paginated list of approval objects.

## Get Approval by ID

Tool hint: `GET /rest/servicedeskapi/request/{issueIdOrKey}/approval/{approvalId}`.

## Answer Approval

Tool hint: `POST /rest/servicedeskapi/request/{issueIdOrKey}/approval/{approvalId}`.

Documented description (verbatim): "This method enables a user to Approve or Decline an approval on a
customer request. The approval is assumed to be owned by the user making the call." Permission
required: "User is assigned to the approval request."

Body: `{"decision": "approve"}` or `{"decision": "decline"}` (schema:
`ApprovalDecisionRequestDTO`).

Response (`200`, schema `ApprovalDTO`) example (verbatim, abbreviated):
```json
{
  "id": "1",
  "name": "Please approve this request",
  "finalDecision": "approved",
  "canAnswerApproval": false,
  "approvers": [
    {
      "approver": {"accountId": "qm:...", "displayName": "Fred F. User", "active": true},
      "approverDecision": "approved"
    }
  ],
  "createdDate": {"iso8601": "2016-09-28T14:01:00+0700"},
  "completedDate": {"iso8601": "2016-09-29T14:30:00+0700"},
  "_links": {"self": "https://your-domain.atlassian.net/rest/servicedeskapi/request/2/approval/1"}
}
```
Note `canAnswerApproval: false` in the response once `finalDecision` is already set — this is the
API's own signal that the approval is terminal and cannot be re-decided.

Documented errors: `400` — request not valid; `401` — not logged in; `403` — "user does not have
permission to complete this request" (not the assigned approver); `404` — "the customer request or
the approval do not exist."
