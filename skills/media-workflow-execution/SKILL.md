---
name: media-workflow-execution
description: >-
  Submit an approved media workflow and retrieve its generated output. Use for ComfyUI self-hosted workflow submission, progress tracking and image retrieval. Covers ComfyUI. Assumes a configured ComfyUI API client and an already validated workflow with installed models/nodes.
---

# Media workflow execution

Submit an approved media workflow and retrieve its generated output.

## When to use this skill

Use for ComfyUI self-hosted workflow submission, progress tracking and image retrieval.

## Universal concepts

No common wire protocol is implied by this capability. Submission acceptance is different from execution completion. Generated media does not independently verify the facts described by a prompt.

## Procedure

1. Identify the requested platform in [the reference index](references/INDEX.md).
2. Follow that platform's linked procedure exactly, including its scope and safeguards.
3. Report the result using that procedure's own status or result vocabulary.

## Known limitations

No model installation, custom-node installation, topology discovery, guaranteed structural fidelity or automatic alternate-backend selection is included.

## Contributing to this skill

Change this router only to correct shared concepts/routing or add a supported platform pointer.
Vendor operations, error handling, and literal bindings belong in that platform's references.

## Tools

Assumes a configured ComfyUI API client and an already validated workflow with installed models/nodes. The selected procedure lists its required operations and bindings.

## Verification checklist

- The selected platform and operation match the request and reference index.
- The procedure's documented success checks and error handling were applied.
- The reported outcome preserves incomplete results and platform limitations.
