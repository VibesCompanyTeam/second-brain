#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Validate metadata, internal links and decision numbers.

Errors fail the run; expired reviews are only reported.
"""
import datetime as dt
from pathlib import Path
import re
import sys

import yaml

CHECKED = ("01-company", "02-projects", "03-areas", "04-knowledge", "05-decisions", "06-meetings")
TYPES = {"policy", "strategy", "project", "requirement", "architecture", "decision",
         "knowledge", "playbook", "research", "meeting"}
STATUSES = {"draft", "proposed", "active", "accepted", "rejected", "deprecated", "superseded"}
VISIBILITIES = {"team", "project"}
EXPIRED_EXEMPT = {"rejected", "deprecated", "superseded"}


def frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data


def check(meta, today):
    errors, warnings = [], []
    required = ["title", "type", "status", "owner", "created", "visibility"]
    if meta.get("type") != "meeting":
        required.append("review_at")
    errors += [f"missing {key}" for key in required if not meta.get(key)]
    for key, allowed in (("type", TYPES), ("status", STATUSES), ("visibility", VISIBILITIES)):
        if meta.get(key) and meta[key] not in allowed:
            errors.append(f"invalid {key}: {meta[key]}")
    created, review = meta.get("created"), meta.get("review_at")
    for key, value in (("created", created), ("review_at", review)):
        if value and not isinstance(value, dt.date):
            errors.append(f"{key} is not a YYYY-MM-DD date: {value}")
    if isinstance(created, dt.date) and isinstance(review, dt.date) and review < created:
        errors.append("review_at precedes created")
    if isinstance(review, dt.date) and review < today and meta.get("status") not in EXPIRED_EXEMPT:
        warnings.append(f"review expired on {review}")
    return errors, warnings


def slug(heading):
    """Approximate GitHub's anchor for a heading."""
    text = re.sub(r"[`*]", "", heading.strip().lower())
    return re.sub(r"[^\w\s-]", "", text).replace(" ", "-")


def strip_code(text):
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)


def check_links(root):
    errors = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if ".git" in rel.parts or ".venv" in rel.parts:
            continue
        for link in re.findall(r"\]\(([^)\s]+)\)", strip_code(path.read_text(encoding="utf-8"))):
            if re.match(r"[a-z][a-z0-9+.-]*:", link):
                continue
            target_name, _, anchor = link.partition("#")
            target = (path.parent / target_name).resolve() if target_name else path
            if not target.exists():
                errors.append(f"{rel}: broken link {link}")
            elif anchor and target.is_file():
                headings = re.findall(r"^#+\s+(.*)$", strip_code(target.read_text(encoding="utf-8")), re.M)
                if anchor not in {slug(h) for h in headings}:
                    errors.append(f"{rel}: broken anchor {link}")
    return errors


def check_decision_numbers(root):
    errors, seen = [], {}
    for folder in [root / "05-decisions", *(root / "02-projects").glob("*/decisions")]:
        seen.clear()
        for path in sorted(folder.glob("*.md")):
            if path.name == "README.md":
                continue
            rel = path.relative_to(root)
            match = re.match(r"(\d{4})-", path.name)
            if not match:
                errors.append(f"{rel}: decision file name must start with NNNN-")
            elif match[1] in seen:
                errors.append(f"{rel}: number {match[1]} already used by {seen[match[1]]}")
            else:
                seen[match[1]] = path.name
    return errors


def main():
    root = Path(__file__).resolve().parent.parent
    today, failed, count = dt.date.today(), False, 0
    for folder in CHECKED:
        for path in sorted((root / folder).rglob("*.md")):
            if path.name == "README.md":
                continue
            count += 1
            rel = path.relative_to(root)
            try:
                meta = frontmatter(path.read_text(encoding="utf-8"))
                errors, warnings = check(meta, today)
                supersedes = meta.get("supersedes")
                if supersedes and not (root / supersedes).is_file():
                    errors.append(f"supersedes points to a missing file: {supersedes}")
            except (ValueError, yaml.YAMLError) as exc:
                errors, warnings = [str(exc)], []
            for message in errors:
                print(f"ERROR {rel}: {message}")
                failed = True
            for message in warnings:
                print(f"WARN  {rel}: {message}")
    for message in check_links(root) + check_decision_numbers(root):
        print(f"ERROR {message}")
        failed = True
    print(f"{count} documents checked")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
