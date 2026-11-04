#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Turn this demo into a clean starting point: dry run by default, --apply to write."""
import argparse
import datetime as dt
from pathlib import Path
import re

from build_index import render
from check_docs import CHECKED, frontmatter

DEMO_BLOCK = re.compile(r"<!-- demo:start -->.*?<!-- demo:end -->\n*", re.S)
CI_JOB = re.compile(r"^  new-client:\n(?:(?:    .*)?\n)*", re.M)
REVIEW_DAYS = 90


def is_demo(path):
    try:
        return frontmatter(path.read_text(encoding="utf-8")).get("demo") is True
    except ValueError:
        return False


def reset(text, owner, today):
    head, body = text[4:].split("\n---", 1)
    head = re.sub(r"^status: (active|accepted)$", "status: proposed", head, flags=re.M)
    head = re.sub(r"^owner: .*$", f"owner: {owner}", head, flags=re.M)
    head = re.sub(r"^created: .*$", f"created: {today}", head, flags=re.M)
    review = today + dt.timedelta(days=REVIEW_DAYS)
    head = re.sub(r"^review_at: .*$", f"review_at: {review}", head, flags=re.M)
    return f"---\n{head}\n---{body}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", required=True, help="owner of the system documents")
    parser.add_argument("--apply", action="store_true", help="write the changes")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    today = dt.date.today()

    demo_files = [path for path in root.rglob("*.md")
                  if ".git" not in path.relative_to(root).parts and is_demo(path)]
    demo_files.append(root / "DEMO.md")
    keep = [path for folder in CHECKED for path in (root / folder).rglob("*.md")
            if path.name != "README.md" and path not in demo_files]

    for path in demo_files:
        print(f"remove {path.relative_to(root)}")
    for path in keep:
        print(f"reset  {path.relative_to(root)}")
    print("remove tools/new_client.py and its CI job")
    if not args.apply:
        print("Dry run: nothing changed. Add --apply to write.")
        return

    for path in demo_files:
        path.unlink()
    for path in keep:
        path.write_text(reset(path.read_text(encoding="utf-8"), args.owner, today), encoding="utf-8")
    readme = root / "README.md"
    readme.write_text(DEMO_BLOCK.sub("", readme.read_text(encoding="utf-8")), encoding="utf-8")
    for folder in sorted(root.glob("0*/**/"), reverse=True):
        children = list(folder.iterdir())
        if not children:
            if folder.parent.name == "02-projects" or "02-projects" in folder.parts:
                folder.rmdir()
            else:
                (folder / ".gitkeep").touch()
    (root / "INDEX.md").write_text(render(root), encoding="utf-8")
    workflow = root / ".github" / "workflows" / "check.yml"
    workflow.write_text(CI_JOB.sub("", workflow.read_text(encoding="utf-8")), encoding="utf-8")
    Path(__file__).unlink()
    print("Done. Next steps: 04-knowledge/playbooks/prima-installazione.md")


if __name__ == "__main__":
    main()
