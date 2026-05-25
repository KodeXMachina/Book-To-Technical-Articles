#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path

TOKEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("qualified", re.compile(r"\b(?:[A-Za-z_]\w*::)+[A-Za-z_]\w*\b")),
    ("macro", re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")),
    ("dunder", re.compile(r"\b__\w+__?\b")),
    ("snake", re.compile(r"\b[A-Za-z_]\w*_[A-Za-z0-9_]\w*\b")),
    ("camel", re.compile(r"\b[a-z]+[A-Z][A-Za-z0-9_]*\b")),
    ("function", re.compile(r"\b[A-Za-z_]\w*\(\)")),
]
STOP = {
    "the", "and", "for", "with", "this", "that", "from", "into", "return", "class", "struct",
    "public", "private", "protected", "const", "static", "inline", "void", "int", "long", "short",
    "float", "double", "bool", "true", "false", "using", "namespace", "include", "define",
}


@dataclass(frozen=True)
class Occurrence:
    token: str
    kind: str
    file: str
    line: int


def iter_files(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for path in paths:
        if path.is_dir():
            out.extend(sorted(path.rglob("*.md")))
        elif path.exists():
            out.append(path)
    return sorted(dict.fromkeys(p.resolve() for p in out))


def load_ignore(path: Path | None) -> set[str]:
    if not path:
        return set()
    ignored: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.split("#", 1)[0].strip()
        if item:
            ignored.add(item)
    return ignored


def extract(paths: list[Path], ignored: set[str]) -> dict[str, list[Occurrence]]:
    tokens: dict[str, list[Occurrence]] = defaultdict(list)
    for path in iter_files(paths):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line_no, line in enumerate(lines, start=1):
            for kind, pattern in TOKEN_PATTERNS:
                for token in pattern.findall(line):
                    clean = token.rstrip("()")
                    if len(clean) < 3 or clean.lower() in STOP or clean in ignored:
                        continue
                    tokens[clean].append(Occurrence(clean, kind, str(path), line_no))
    return dict(tokens)


def first_occurrences(tokens: dict[str, list[Occurrence]], names: list[str]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for name in names:
        occ = tokens[name][0]
        out.append(asdict(occ) | {"count": len(tokens[name])})
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare API-like token coverage between source and generated materials.")
    parser.add_argument("--source", nargs="+", required=True, type=Path)
    parser.add_argument("--target", nargs="+", required=True, type=Path)
    parser.add_argument("--ignore-file", type=Path, help="Text file with one token to ignore per line; # comments allowed.")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()

    ignored = load_ignore(args.ignore_file)
    source = extract(args.source, ignored)
    target = extract(args.target, ignored)
    source_names = set(source)
    target_names = set(target)
    missing = sorted(source_names - target_names)
    kind_counts = Counter(source[token][0].kind for token in missing)
    result = {
        "source_tokens": len(source_names),
        "target_tokens": len(target_names),
        "missing_tokens": len(missing),
        "missing_by_kind": dict(sorted(kind_counts.items())),
        "missing_sample": first_occurrences(source, missing[: args.limit]),
    }

    if args.markdown:
        print("# Token Coverage Scan\n")
        print(f"- Source tokens: {result['source_tokens']}")
        print(f"- Target tokens: {result['target_tokens']}")
        print(f"- Missing tokens: {result['missing_tokens']}\n")
        print("## Missing by Kind\n")
        for kind, count in result["missing_by_kind"].items():
            print(f"- `{kind}`: {count}")
        print("\n## Missing Sample\n")
        for item in result["missing_sample"]:
            print(f"- `{item['token']}` ({item['kind']}, {item['count']}x) — {item['file']}:{item['line']}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
