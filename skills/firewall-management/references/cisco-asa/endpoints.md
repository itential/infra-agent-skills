# Endpoint Wiring — Cisco ASA REST API (partial — confirmed basics only)

This capability's primary, fully-confirmed path for ASA is the CLI procedure in `procedure.md`. ASA
also exposes a REST API; this file documents only the confirmed parts. Access-list and NAT-rule REST resource paths are Not documented in the confirmed material — do not assume they exist at a path mirroring the CLI
command names without checking Cisco's fuller ASA REST API reference for the target ASA version.

Citation: Cisco Systems, "Cisco ASA Series REST API Quick Start Guide"
(cisco.com/c/en/us/td/docs/security/asa/api/qsg-asa-api.html), retrieved 2026-09-17.

## Authentication

Two methods are documented: HTTP Basic authentication (username and password sent with every
request), or a pre-created token sent with every request instead. Required privilege level depends
on the operation: level 3 or higher for monitoring-style requests, level 5 or higher for `GET`, and
level 15 for `PUT`/`POST`/`DELETE`.

Every request must include the header `User-Agent: REST API Agent` — the documentation describes
this as required, not optional.

## Base URL and confirmed resource

Base: `https://<asa-management-ip>/api/`

Confirmed example resource: `objects/networkobjects`

Tool hint: `GET /api/objects/networkobjects` (list/read), `POST /api/objects/networkobjects` (create,
example body demonstrated in the guide for a network range object). `PUT`, `DELETE`, and `PATCH` are
documented as generally-supported methods across ASA REST resources, but a full worked example for
each is Not documented in the confirmed material.

## Configuration persistence

Confirmed, important: changes made via the REST API land only in the running configuration — they do
not automatically persist to the startup configuration. A separate request (documented as a
`writemem`-style request) is needed to persist changes so they survive a reload. The exact literal
path for that persist request is Not documented in the confirmed material — confirm it
against Cisco's fuller ASA REST API reference before relying on a specific path.

## Not confirmed

- Access-list (extended ACL) REST resource path and request/response shape.
- NAT-rule REST resource path and request/response shape.
- The literal `writemem`/persist request path.

Use the CLI procedure in `procedure.md` for these until a REST path is independently confirmed.
