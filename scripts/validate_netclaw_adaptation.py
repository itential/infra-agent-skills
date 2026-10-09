#!/usr/bin/env python3
"""Check the NetClaw migration manifest and its repository structure, offline.

This checks inventory and document structure, not vendor behavior or source accuracy.
Use --source with the pinned NetClaw checkout to verify the complete source inventory
and individual source hashes. No vendor integrations are invoked.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
ROUTER_SECTIONS = (
    "When to use", "Universal concepts", "Procedure", "Known limitations",
    "Contributing to this skill", "Tools", "Verification checklist",
)
PROCEDURE_SECTIONS = ("Patterns", "Known limitations", "Tools", "Verification checklist")


def git_lines(directory, *arguments):
    return subprocess.check_output(
        ["git", "-C", str(directory), *arguments], text=True
    ).splitlines()


def validate(source=None):
    manifest = json.loads((ROOT / "docs/netclaw-manifest.json").read_text())
    errors = []
    words = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    entries = manifest["sources"]
    names = [entry["name"] for entry in entries]
    check(len(names) == len(set(names)) == 235, "Expected 235 unique source skills")
    counts = Counter(entry["status"] for entry in entries)
    for status, count in counts.items():
        check(status in {"converted", "partial", "excluded", "blocked"},
              f"Unknown disposition: {status}")
        check(manifest["counts"].get(status) == count, f"Wrong count for {status}")
    check(manifest["counts"]["source_skills"] == len(entries), "Source count mismatch")
    for entry in entries:
        check(entry["source_path"] == f"workspace/skills/{entry['name']}/SKILL.md",
              f"Unexpected source path: {entry['name']}")
        check(bool(re.fullmatch(r"[0-9a-f]{64}", entry["source_sha256"])),
              f"Invalid source hash: {entry['name']}")
        if entry["status"] in {"converted", "partial"}:
            check(bool(entry["targets"]), f"Missing target: {entry['name']}")
        if entry["status"] in {"partial", "excluded", "blocked"}:
            check(bool(entry["omitted"]), f"Missing scope explanation: {entry['name']}")
        for target in entry["targets"]:
            check(target.startswith("skills/") and (ROOT / target).exists(),
                  f"Missing target: {entry['name']} -> {target}")

    capabilities = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    readme = (ROOT / "README.md").read_text()
    catalog = re.findall(r"^\| `([^`]+)` \|", readme, re.M)
    check(set(catalog) == capabilities and len(catalog) == len(capabilities),
          "README Current Skills and capability directories differ")
    check(manifest["counts"]["total_capabilities"] == len(capabilities),
          "Total capability count mismatch")
    for key, count_key in (
        ("new_capabilities", "new_capabilities"),
        ("updated_existing_capabilities", "updated_existing_capabilities"),
        ("new_platform_reference_directories", "new_platform_reference_directories"),
        ("changed_skill_files", "changed_skill_files"),
    ):
        check(len(manifest[key]) == len(set(manifest[key])) == manifest["counts"][count_key],
              f"Duplicate or wrong count: {key}")

    for relative in manifest["changed_skill_files"]:
        path = ROOT / relative
        check(path.is_file(), f"Missing changed file: {relative}")
        if not path.is_file() or path.suffix != ".md":
            continue
        check("source-extract" not in path.name, f"Raw source extract: {relative}")
        content = path.read_text()
        check(content.endswith("\n"), f"Missing terminal newline: {relative}")
        for destination in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if destination.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = (path.parent / destination.split("#", 1)[0]).resolve()
            check(target.exists(), f"Broken local link: {relative} -> {destination}")

        if path.name == "SKILL.md":
            match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
            check(match is not None, f"Missing frontmatter: {relative}")
            if match:
                frontmatter = match.group(1)
                keys = re.findall(r"^([\w-]+):", frontmatter, re.M)
                check(set(keys) <= {"name", "description", "argument-hint"},
                      f"Unsupported frontmatter key: {relative}")
                check("name" in keys and "description" in keys and len(keys) == len(set(keys)),
                      f"Missing/duplicate frontmatter key: {relative}")
                name = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.M)
                check(name is not None and name.group(1) == path.parent.name,
                      f"Skill name/directory mismatch: {relative}")
            positions = [re.search(r"^## " + re.escape(section), content, re.M)
                         for section in ROUTER_SECTIONS]
            check(all(positions), f"Missing router section: {relative}")
            if all(positions):
                offsets = [position.start() for position in positions]
                check(offsets == sorted(offsets), f"Router section order: {relative}")
            check(len(content.splitlines()) < 500 and len(content.split()) < 3750,
                  f"Router exceeds size budget: {relative}")
            words.append(len(content.split()))

        elif "/references/" in relative and path.name != "INDEX.md" and "endpoints" not in path.name:
            for section in PROCEDURE_SECTIONS:
                check(re.search(r"^## " + re.escape(section), content, re.M),
                      f"Missing {section}: {relative}")
            check(not re.search(r"\b(?:GET|POST|PUT|PATCH|DELETE)\s+/[a-z{]", content),
                  f"HTTP wiring belongs in endpoints: {relative}")
            references = next(parent for parent in path.parents if parent.name == "references")
            index = (references / "INDEX.md").read_text()
            rel_to_index = str(path.relative_to(references))
            check(rel_to_index in index or f"`{path.parent.name}/`" in index,
                  f"Procedure absent from index: {relative}")

    for relative in manifest["new_platform_reference_directories"]:
        directory = ROOT / relative
        procedures = [p for p in directory.glob("*.md") if "endpoints" not in p.name]
        if len(procedures) > 1:
            check(not (directory / "endpoints.md").exists(),
                  f"Multiple procedure modes need prefixed endpoints: {relative}")

    if source:
        source = source.resolve()
        check(git_lines(source, "rev-parse", "HEAD") == [manifest["source_commit"]],
              "Source checkout is not at the pinned commit")
        tracked = git_lines(source, "ls-tree", "-r", "--name-only", manifest["source_commit"],
                            "workspace/skills")
        tracked = {path for path in tracked
                   if re.fullmatch(r"workspace/skills/[^/]+/SKILL.md", path)}
        check(tracked == {entry["source_path"] for entry in entries},
              "Manifest does not cover the exact tracked source inventory")
        for entry in entries:
            path = source / entry["source_path"]
            check(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == entry["source_sha256"],
                  f"Source content differs: {entry['name']}")

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"FAILED: {len(errors)} checks", file=sys.stderr)
        return 1
    print(f"PASS: {len(entries)} source dispositions, {len(capabilities)} catalog capabilities, "
          f"{len(manifest['changed_skill_files'])} changed skill files")
    print(f"Router word counts: {min(words)}–{max(words)}; source hashes "
          f"{'verified' if source else 'not checked (supply --source)'}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Pinned local NetClaw checkout")
    arguments = parser.parse_args()
    raise SystemExit(validate(arguments.source))
