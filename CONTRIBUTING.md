# Contributing to Infrastructure Agent Skills

<!-- PLACEHOLDER — adapted from itential-mcp's CONTRIBUTING.md. Sections marked [PLACEHOLDER]
below depend on decisions not yet made (CI/lint tooling if any). License is now Apache-2.0, see
LICENSE. See TODO.md (untracked, local) for remaining open items. -->

Thank you for your interest in contributing to Infrastructure Agent Skills! This document provides
guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Contributor License Agreement](#contributor-license-agreement)
- [Repository Structure](#repository-structure)
- [Contributing Process](#contributing-process)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Pull Request Labels](#pull-request-labels)
- [Reporting Issues](#reporting-issues)
- [Getting Help](#getting-help)

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please report
unacceptable behavior to [PLACEHOLDER: contact email].

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes**
5. **Submit a pull request**

## Contributor License Agreement

**All contributors must sign a Contributor License Agreement (CLA) before their contributions can
be merged.** See [CLA.md](CLA.md).

When you submit your first pull request, you will be prompted to sign the CLA. Please complete
this process before your contribution can be reviewed.

## Signed Commits

Signing your commits is **strongly recommended**. A signed commit verifies who authored it and
earns the "Verified" badge on GitHub, which protects the project against impersonated commits. It
is recommended, not required by branch protection — an unsigned commit never blocks a
contribution.

SSH signing is the simplest path if you already use an SSH key with GitHub:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Then add the same key as a **signing key** in your GitHub account settings — this is separate from
registering it as an authentication key. GPG signing is also supported if you prefer it. After
setup, new commits show as Verified once the key is registered.

## Repository Structure

```
skills/<capability>/
  SKILL.md                       # thin, stable router
  references/
    INDEX.md                     # vendor/platform -> directory -> scope -> notes
    <vendor>/
      procedure.md
      endpoints.md
```

See the [README](README.md) for the full rationale behind this structure and the rule that keeps
`SKILL.md` stable as vendors are added. See [AGENTS.md](AGENTS.md) for the full authoring rules
and review checklist every skill contribution must follow — read it before writing or reviewing
any `SKILL.md` or `references/` content.

## Contributing Process

### Fork and Pull Model

This project uses a fork and pull request model for contributions:

1. **Fork the repository** to your GitHub account
2. **Create a topic branch** from `main`:
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** in logical, atomic commits
4. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a pull request** against the `main` branch

### Branch Naming Conventions

Use descriptive branch names with prefixes:
- `feature/` - New skills or new vendor coverage
- `fix/` - Corrections to existing content
- `chore/` - Maintenance tasks
- `docs/` - Documentation updates (README, this file, etc. — not skill content itself)

Examples:
- `feature/add-netbox-ipam`
- `fix/correct-servicenow-change-endpoint`
- `chore/reorganize-index-tables`
- `docs/clarify-contribution-process`

## Pull Request Guidelines

### Before Submitting

- [ ] Ensure your branch is up to date with `main`
- [ ] New/changed vendor content lives under that vendor's own `references/<vendor>/` files, not
      in the shared `SKILL.md` — unless this PR is specifically fixing a bug in the shared/router
      content (the one case where touching `SKILL.md` is expected)
- [ ] Every API call, field name, and endpoint path was checked against the vendor's current
      published documentation
- [ ] `references/INDEX.md` for the affected skill is updated to list the new/changed entry
- [ ] New companion files follow this skill's existing naming convention, so they don't silently
      overwrite another vendor's or platform-family's file of the same generic name
- [ ] Sign the Contributor License Agreement (CLA)

### Pull Request Description

Your pull request should include:

1. **Clear title** describing the change
2. **Detailed description** explaining:
   - What the change does
   - Which skill(s) and vendor(s) it affects
   - The source documentation it was built or verified from
3. **References to related issues** (if applicable)
4. **Any corrections to shared "universal concepts"** — called out explicitly, not folded silently
   into a vendor's own file

Use the [PR template](.github/PULL_REQUEST_TEMPLATE.md) — it already reflects this structure.

## Pull Request Labels

Please apply the label(s) that best describe your change:

- `new-capability` — an entirely new top-level skill
- `new-vendor` — a new vendor/platform added under an existing skill
- `enhancement` — an improvement that isn't cleanly a new vendor or new capability (e.g.
  reorganizing an `INDEX.md`, improving a `SKILL.md`'s clarity)
- `bug` — a correction to wrong, outdated, or broken existing content
- `chore` — repo maintenance, non-content changes
- `documentation` — README/CONTRIBUTING/governance changes
- `security` — anything flagged per [SECURITY.md](SECURITY.md)

### Other Labels
- `question`, `duplicate`, `invalid`, `wontfix`, `help wanted` — standard GitHub triage labels,
  used as usual

## Reporting Issues

When reporting issues, please include:

1. **Which skill and vendor** the issue is about
2. **Clear description** of what's wrong
3. **Steps to reproduce** — usually "follow `references/<vendor>/procedure.md` step X"
4. **Expected vs actual behavior** against the live vendor API/product
5. **Source** — a link to the vendor's current published documentation supporting the correction,
   if you have one
6. Whether this is vendor-specific or contradicts a **shared "universal concepts" assumption** in
   `SKILL.md` — that distinction determines whether the fix touches one file or the router itself

Use the [Bug Report issue template](.github/ISSUE_TEMPLATE/bug_report.md) for corrections to
existing content, the [New Vendor template](.github/ISSUE_TEMPLATE/new_vendor.md) to propose
adding a platform to an existing skill, or the
[New Capability template](.github/ISSUE_TEMPLATE/new_capability.md) to propose an entirely new
top-level skill.

## Getting Help

### Resources

- **Documentation**: Check the [README.md](README.md)
- **Issues**: Search existing issues for similar problems
- **Discussions**: Use GitHub Discussions for questions

### Asking Questions

- Use GitHub Discussions for general questions
- Search existing discussions and issues first
- Provide context and specific details

## Recognition

Contributors who have their pull requests merged will be recognized in the project's contributor
list.

Thank you for contributing to Infrastructure Agent Skills!

---

For questions about contributing, please contact [PLACEHOLDER: contact email].
