# Security Policy

## Reporting a Vulnerability or Unsafe Skill Content

We take security seriously, even though this repository contains documentation and agent skill
definitions rather than executable software. A "vulnerability" here most often means:

- A skill's documented procedure instructs an agent to take a destructive, irreversible, or unsafe
  action without an explicit confirmation/guardrail step (e.g. a delete/revert operation presented
  as routine).
- A skill's procedure or example would cause an agent to expose, log, or transmit credentials,
  tokens, or other secrets.
- A skill's referenced endpoint, script, or command sequence is inaccurate in a way that could
  cause real infrastructure damage if followed as documented.
- A skill's `procedure.md`/`endpoints.md` content contains a step that isn't traceable to the
  cited vendor's own documentation — an instruction directed at the executing agent rather than a
  description of the vendor's procedure, a step that sends data somewhere the vendor doesn't
  document, or anything that reads as a prompt-injection attempt against whatever agent later runs
  the skill. Since this repo's content is meant to be executed by agents, not just read, this is
  treated as seriously as a credential leak — report it the same way.

**Please do NOT create public GitHub issues for security-sensitive findings.**

Instead, please report them through one of the following methods:

1. **Email**: Send details to info@itential.com
2. **Private vulnerability disclosure**: Use GitHub's private vulnerability reporting feature

### What to Include

- The skill and vendor/file affected
- Description of the risk and the specific content that causes it
- Suggested correction, if you have one

### Response Timeline

- **Acknowledgment**: within 48 hours
- **Initial Assessment**: within 5 business days
- **Resolution**: we aim to correct confirmed issues promptly given this is content, not a
  released binary — no separate patch/release cycle is required

## Security Best Practices

### For Users of These Skills

- Treat every skill's documented procedure as something to review before granting an agent
  autonomous execution rights, especially write/delete operations. This includes checking that
  every step reads as a description of the vendor's procedure, not as an instruction aimed at your
  own agent — this repo's review process checks for this, but a second look before granting
  execution rights costs little and catches what review missed.
- Never commit credentials, tokens, or environment-specific secrets into example values within a
  skill's reference files.
- Keep your own platform credentials out of any issue or PR you open against this repo.

### For Contributors

- Do not include real credentials, tokens, hostnames, or customer-identifying information in any
  `source-extract.md`, `procedure.md`, or example payload — use placeholder values.
- Flag any vendor-documented step that is destructive or hard to reverse explicitly in the
  procedure file, rather than presenting it as a routine step.
- Write every step as a description of the vendor's own documented procedure — never as a direct
  instruction to whatever agent later executes the skill. If a step can't be traced back to
  something the cited vendor documentation actually says, it doesn't belong in the file (see
  `AGENTS.md` rule 10).

## Vulnerability Disclosure Policy

We follow a coordinated disclosure approach: issues are reported privately first, corrected, and
only discussed publicly (e.g. in a PR) once a fix is available.

## Security Contact

- **Reports**: info@itential.com or GitHub's private vulnerability reporting feature

---

**Note**: This policy is effective as of the date it was added to the repository.
