#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def iter_md(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for path in paths:
        if path.is_dir():
            out.extend(sorted(path.rglob("*.md")))
        elif path.suffix.lower() == ".md":
            out.append(path)
    return sorted(dict.fromkeys(p.resolve() for p in out))


def stats_for(files: list[Path]) -> dict[str, int]:
    stats = {
        "markdown_files": len(files),
        "lines": 0,
        "words": 0,
        "code_fence_markers": 0,
        "code_blocks_estimated": 0,
        "mermaid_blocks": 0,
        "image_links": 0,
        "links": 0,
        "table_like_lines": 0,
    }
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        stats["lines"] += text.count("\n") + (1 if text and not text.endswith("\n") else 0)
        stats["words"] += len(re.findall(r"\S+", text))
        stats["code_fence_markers"] += len(re.findall(r"^```", text, re.M))
        stats["mermaid_blocks"] += len(re.findall(r"^```mermaid\s*$", text, re.M))
        stats["image_links"] += len(IMAGE_RE.findall(text))
        stats["links"] += len(LINK_RE.findall(text))
        stats["table_like_lines"] += sum(1 for line in text.splitlines() if line.strip().startswith("|") and line.strip().endswith("|"))
    stats["code_blocks_estimated"] = stats["code_fence_markers"] // 2
    return stats


def to_markdown(stats: dict[str, int]) -> str:
    rows = "\n".join(f"| {key} | {value} |" for key, value in stats.items())
    return f"# Markdown Stats\n\n| Metric | Value |\n| --- | ---: |\n{rows}\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan Markdown statistics for book-derived materials.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--markdown", action="store_true", help="Print Markdown instead of JSON.")
    args = parser.parse_args()
    files = iter_md(args.paths)
    stats = stats_for(files)
    print(to_markdown(stats) if args.markdown else json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
