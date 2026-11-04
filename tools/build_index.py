#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Generate INDEX.md from document metadata. With --check, fail if it is out of date."""
from pathlib import Path
import sys

from check_docs import CHECKED, frontmatter

HEADER = """# Indice

Generato da `tools/build_index.py`: non modificarlo a mano. Lo stato indica quanto fidarsi di un
documento, come spiegato nella [policy di governance](01-company/policies/knowledge-governance.md). Le note
in `00-inbox/` non sono elencate.
"""


def render(root):
    lines = [HEADER]
    for folder in CHECKED:
        rows = []
        for path in sorted((root / folder).rglob("*.md")):
            if path.name == "README.md":
                continue
            meta = frontmatter(path.read_text(encoding="utf-8"))
            rel = path.relative_to(root).as_posix()
            title = str(meta.get("title", "")).replace("|", "\\|")
            rows.append(f"| [{title}]({rel}) | {meta.get('type')} | {meta.get('status')} "
                        f"| {meta.get('owner')} | {meta.get('review_at', '-')} |")
        if rows:
            lines += [f"## {folder}\n", "| Documento | Tipo | Stato | Responsabile | Revisione |",
                      "| --- | --- | --- | --- | --- |", *rows, ""]
    return "\n".join(lines).rstrip() + "\n"


def main():
    root = Path(__file__).resolve().parent.parent
    index, content = root / "INDEX.md", render(root)
    if "--check" in sys.argv[1:]:
        if not index.exists() or index.read_text(encoding="utf-8") != content:
            print("INDEX.md is out of date: run uv run tools/build_index.py")
            return 1
        print("INDEX.md is up to date")
        return 0
    index.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
