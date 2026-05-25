#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```", re.M)
OLD_RESIDUE = [
    "本段主旨", "原文核对", "中文教材正文", "讲解：",
    "Section summary", "Source check", "Generated article body", "Explanation:",
    "<details>",
]
STRICT_MARKERS = {
    "uncertainty": {
        "zh": ["待确认"],
        "en": ["Needs confirmation", "To confirm", "Unconfirmed"],
    },
    "qa": {
        "zh": ["Q&A"],
        "en": ["Q&A"],
    },
    "update_log": {
        "zh": ["更新记录"],
        "en": ["Update log", "Updates", "Change log"],
    },
}
AUDIT_NAMES = {"source_coverage_audit.md", "v1_source_coverage_audit.md", "v3_source_coverage_audit.md"}
READER_LOG_FILES = ["question-log.md", "backwrite-candidates.md", "applied-backwrites.md"]


def iter_md(root: Path, excludes: set[Path]) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        resolved = path.resolve()
        if any(resolved == item or item in resolved.parents for item in excludes):
            continue
        files.append(path)
    return files


def local_target(path: Path, raw: str) -> Path | None:
    raw = raw.strip()
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1]
    raw = raw.split("#", 1)[0]
    if not raw or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
        return None
    return (path.parent / unquote(raw)).resolve()


def strip_fenced_blocks(text: str) -> str:
    return re.sub(r"(?ms)^```.*?^```", "", text)


def rel_display(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def check_reader_question_logs(root: Path, issues: list[str], warnings: list[str]) -> None:
    reader_dir = root / "course_materials" / "reader_questions"
    if not reader_dir.exists():
        return
    if not reader_dir.is_dir():
        issues.append("reader_questions exists but is not a directory: course_materials/reader_questions")
        return
    for name in READER_LOG_FILES:
        path = reader_dir / name
        rel = rel_display(path, root)
        if not path.exists():
            issues.append(f"Missing reader-question log: {rel}")
        elif not path.read_text(encoding="utf-8", errors="replace").strip():
            warnings.append(f"Empty reader-question log: {rel}")


def marker_options(language: str, marker_group: dict[str, list[str]]) -> list[str]:
    if language == "auto":
        return sorted({item for items in marker_group.values() for item in items})
    return marker_group[language]


def validate(root: Path, strict: bool = False, scope: str = "project", excludes: set[Path] | None = None, language: str = "auto") -> dict[str, object]:
    root = root.resolve()
    excludes = excludes or set()
    issues: list[str] = []
    warnings: list[str] = []
    md_files = iter_md(root, excludes)

    if scope == "project":
        for name in ["markdown_output", "course_materials"]:
            if not (root / name).exists():
                warnings.append(f"Missing expected layer: {name}")
        if not any(p.name in AUDIT_NAMES for p in md_files):
            warnings.append("No source coverage audit Markdown found")
        check_reader_question_logs(root, issues, warnings)
    elif scope == "skill":
        for rel in ["SKILL.md", "agents/openai.yaml"]:
            if not (root / rel).exists():
                issues.append(f"Missing required skill file: {rel}")
        for dirname in ["references", "scripts"]:
            if not (root / dirname).exists():
                warnings.append(f"Missing optional skill resource directory: {dirname}")

    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root)
        if len(FENCE_RE.findall(text)) % 2:
            issues.append(f"Unbalanced code fence: {rel}")
        prose = strip_fenced_blocks(text)
        check_residue = scope == "project" or (scope == "skill" and rel.parts[0] not in {"references"})
        if check_residue:
            for residue in OLD_RESIDUE:
                if residue in prose:
                    issues.append(f"Old template residue `{residue}` in {rel}")
        for raw in IMAGE_RE.findall(text):
            target = local_target(path, raw)
            if target is not None and not target.exists():
                issues.append(f"Missing image from {rel}: {raw}")
        for raw in LINK_RE.findall(text):
            target = local_target(path, raw)
            if target is not None and target.suffix.lower() == ".md" and not target.exists():
                issues.append(f"Missing Markdown link from {rel}: {raw}")

    if strict:
        joined = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in md_files)
        for name, marker_group in STRICT_MARKERS.items():
            options = marker_options(language, marker_group)
            if not any(marker in joined for marker in options):
                expected = ", ".join(options)
                warnings.append(f"Strict-mode marker not found: {name} (expected one of: {expected})")

    return {
        "root": str(root),
        "scope": scope,
        "language": language,
        "markdown_files": len(md_files),
        "excluded_paths": sorted(str(p) for p in excludes),
        "issues": issues,
        "warnings": warnings,
        "ok": not issues,
    }


def to_markdown(result: dict[str, object]) -> str:
    issues = result["issues"]
    warnings = result["warnings"]
    lines = [
        "# Book Materials Validation",
        "",
        f"- Root: `{result['root']}`",
        f"- Scope: {result['scope']}",
        f"- Language: {result['language']}",
        f"- Markdown files: {result['markdown_files']}",
        f"- Result: {'PASS' if result['ok'] else 'FAIL'}",
        "",
        "## Issues",
        "",
    ]
    lines.extend([f"- {item}" for item in issues] or ["- None"])
    lines.extend(["", "## Warnings", ""])
    lines.extend([f"- {item}" for item in warnings] or ["- None"])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate book-to-article project materials or this skill repository.")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--scope", choices=["project", "skill"], default="project", help="Validate generated book output or a skill repository.")
    parser.add_argument("--exclude", action="append", default=[], help="Relative path under project_root to exclude; can be repeated.")
    parser.add_argument("--strict", action="store_true", help="Check strict knowledge-base markers.")
    parser.add_argument("--language", choices=["auto", "zh", "en"], default="auto", help="Output language used for strict marker checks.")
    parser.add_argument("--markdown", action="store_true", help="Print Markdown instead of JSON.")
    args = parser.parse_args()
    root = args.project_root.resolve()
    excludes = {(root / item).resolve() for item in args.exclude}
    result = validate(root, strict=args.strict, scope=args.scope, excludes=excludes, language=args.language)
    print(to_markdown(result) if args.markdown else json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
