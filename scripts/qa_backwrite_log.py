#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

LABELS = {
    "en": {
        "not_recorded": "Not recorded",
        "not_decided": "Not decided",
        "created": "Created",
        "status": "Status",
        "impact": "Impact",
        "backwrite_targets": "Backwrite targets",
        "suggested_targets": "Suggested targets",
        "applied": "Applied",
        "changed_files": "Changed files",
        "reader_question": "Reader question",
        "answer_summary": "Answer summary",
        "book_evidence": "Book/project evidence",
        "web_supplements": "Web supplements",
        "inference_notes": "Inference notes",
        "unresolved_points": "Unresolved points",
        "reader_gap": "Reader gap",
        "organic_backwrite_direction": "Organic backwrite direction",
        "evidence_to_preserve": "Evidence to preserve",
        "rationale": "Rationale",
        "audit_updates": "Audit/index updates",
        "question_log_title": "Reader Question Log",
        "question_log_intro": "Reader questions answered from book/project evidence, optional web supplements, and explicit inference.\n",
        "candidate_title": "Backwrite Candidates",
        "candidate_intro": "Questions that may reveal reusable explanation gaps. Confirm before editing articles.\n",
        "applied_title": "Applied Backwrites",
        "applied_intro": "Confirmed explanation improvements made from reader-question signals.\n",
        "default_direction": "Add a bridge, judgment table, code-path explanation, misconception note, or reference patch based on the confirmed gap.",
    },
    "zh": {
        "not_recorded": "未记录",
        "not_decided": "未决定",
        "created": "创建日期",
        "status": "状态",
        "impact": "影响类型",
        "backwrite_targets": "反写目标",
        "suggested_targets": "建议目标",
        "applied": "应用日期",
        "changed_files": "修改文件",
        "reader_question": "读者问题",
        "answer_summary": "回答摘要",
        "book_evidence": "书内/项目证据",
        "web_supplements": "网络补充来源",
        "inference_notes": "推导说明",
        "unresolved_points": "未解决点",
        "reader_gap": "读者理解缺口",
        "organic_backwrite_direction": "有机反写方向",
        "evidence_to_preserve": "需要保留的证据",
        "rationale": "反写理由",
        "audit_updates": "审计/索引更新",
        "question_log_title": "读者问题记录",
        "question_log_intro": "记录基于书内/项目证据、可选网络补充和显式推导回答过的读者问题。\n",
        "candidate_title": "反写候选",
        "candidate_intro": "记录可能暴露可复用解释缺口的问题；编辑文章前需要确认。\n",
        "applied_title": "已应用反写",
        "applied_intro": "记录基于读者问题信号完成的解释增强。\n",
        "default_direction": "根据已确认的理解缺口，增加过渡段、判断表、代码路径解释、误解说明或 reference patch。",
    },
}


def slugify(text: str, max_len: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return (slug[:max_len].strip("-") or "question")


def entry_slug(text: str) -> str:
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    return f"{slugify(text)}-{digest}"


def infer_language(text: str) -> str:
    return "zh" if re.search(r"[\u4e00-\u9fff]", text) else "en"


def resolve_log_dir(project_root: Path, raw: str) -> Path:
    relative = Path(raw)
    if relative.is_absolute():
        raise ValueError("--log-dir must be a relative path under project_root")
    candidate = (project_root / relative).resolve()
    if candidate != project_root and project_root not in candidate.parents:
        raise ValueError("--log-dir must stay under project_root")
    return candidate


def bullet_list(items: list[str], fallback: str) -> str:
    values = [item.strip() for item in items if item.strip()]
    if not values:
        return f"- {fallback}\n"
    return "".join(f"- {item}\n" for item in values)


def parse_web_sources(values: list[str]) -> tuple[list[str], list[str]]:
    sources: list[str] = []
    warnings: list[str] = []
    for raw in values:
        parts = [part.strip() for part in raw.split("|", 2)]
        if len(parts) == 1:
            title, url, note = "Web source", parts[0], ""
        elif len(parts) == 2:
            title, url = parts
            note = ""
        else:
            title, url, note = parts
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            warnings.append(f"Web source does not look like an HTTP URL: {raw}")
        suffix = f" - {note}" if note else ""
        sources.append(f"[{title}]({url}){suffix}")
    return sources, warnings


def ensure_file(path: Path, title: str, intro: str) -> None:
    if not path.exists():
        path.write_text(f"# {title}\n\n{intro}\n", encoding="utf-8")


def append(path: Path, text: str, dry_run: bool) -> None:
    if dry_run:
        print(f"--- {path} ---")
        print(text)
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def build_entry(args: argparse.Namespace, entry_id: str, web_sources: list[str], labels: dict[str, str]) -> str:
    fallback = labels["not_recorded"]
    not_decided = labels["not_decided"]
    return f"""
## {entry_id}

- {labels['created']}: {args.created}
- {labels['status']}: {args.status}
- {labels['impact']}: {args.impact}
- {labels['backwrite_targets']}: {', '.join(args.backwrite_target) if args.backwrite_target else not_decided}

### {labels['reader_question']}

{args.question.strip()}

### {labels['answer_summary']}

{args.answer_summary.strip()}

### {labels['book_evidence']}

{bullet_list(args.book_evidence, fallback)}
### {labels['web_supplements']}

{bullet_list(web_sources, fallback)}
### {labels['inference_notes']}

{bullet_list(args.inference, fallback)}
### {labels['unresolved_points']}

{bullet_list(args.unresolved, fallback)}
"""


def build_candidate(args: argparse.Namespace, entry_id: str, labels: dict[str, str]) -> str:
    fallback = labels["not_recorded"]
    not_decided = labels["not_decided"]
    direction = args.backwrite_direction.strip() if args.backwrite_direction else labels["default_direction"]
    return f"""
## {entry_id}

- {labels['status']}: {args.status}
- {labels['impact']}: {args.impact}
- {labels['suggested_targets']}: {', '.join(args.backwrite_target) if args.backwrite_target else not_decided}

### {labels['reader_gap']}

{args.question.strip()}

### {labels['organic_backwrite_direction']}

{direction}

### {labels['evidence_to_preserve']}

{bullet_list(args.book_evidence, fallback)}
"""


def build_applied(args: argparse.Namespace, entry_id: str, labels: dict[str, str]) -> str:
    fallback = labels["not_recorded"]
    return f"""
## {entry_id}

- {labels['applied']}: {args.created}
- {labels['changed_files']}: {', '.join(args.changed_file) if args.changed_file else fallback}
- {labels['backwrite_targets']}: {', '.join(args.backwrite_target) if args.backwrite_target else fallback}

### {labels['rationale']}

{args.backwrite_direction.strip() if args.backwrite_direction else args.answer_summary.strip()}

### {labels['audit_updates']}

{bullet_list(args.audit_update, fallback)}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Append reader Q&A and organic article-backwrite records.")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--question", required=True, help="Reader question or confusion signal.")
    parser.add_argument("--answer-summary", required=True, help="Short answer summary, not a full pasted transcript.")
    parser.add_argument("--book-evidence", action="append", default=[], help="Local book/project evidence; repeat for multiple items.")
    parser.add_argument("--web-source", action="append", default=[], help="Optional web supplement as 'title|url|note'; repeat for multiple items.")
    parser.add_argument("--inference", action="append", default=[], help="Reasoning that connects evidence to the answer.")
    parser.add_argument("--unresolved", action="append", default=[], help="Unresolved point or follow-up needed.")
    parser.add_argument("--backwrite-target", action="append", default=[], help="Candidate article path or section; repeat for multiple targets.")
    parser.add_argument("--backwrite-direction", default="", help="Organic rewrite direction, not raw Q&A copy.")
    parser.add_argument("--changed-file", action="append", default=[], help="File changed when status is applied.")
    parser.add_argument("--audit-update", action="append", default=[], help="Audit/index update made when status is applied.")
    parser.add_argument("--status", choices=["needs-confirmation", "candidate", "approved", "applied", "rejected"], default="candidate")
    parser.add_argument("--impact", default="reader-gap", help="Short label such as reader-gap, source-gap, current-context, or code-path.")
    parser.add_argument("--created", default=datetime.now().strftime("%Y-%m-%d"), help="Record date, default today.")
    parser.add_argument("--language", choices=["auto", "en", "zh"], default="auto", help="Markdown log heading language; auto infers from question text.")
    parser.add_argument("--log-dir", default="course_materials/reader_questions", help="Relative log directory under project root.")
    parser.add_argument("--dry-run", action="store_true", help="Print entries instead of writing files.")
    args = parser.parse_args()

    log_language = infer_language(f"{args.question} {args.answer_summary}") if args.language == "auto" else args.language
    labels = LABELS[log_language]
    project_root = args.project_root.resolve()
    try:
        log_dir = resolve_log_dir(project_root, args.log_dir)
    except ValueError as exc:
        parser.error(str(exc))
    if not args.dry_run:
        log_dir.mkdir(parents=True, exist_ok=True)

    question_log = log_dir / "question-log.md"
    candidates = log_dir / "backwrite-candidates.md"
    applied = log_dir / "applied-backwrites.md"

    if not args.dry_run:
        ensure_file(question_log, labels["question_log_title"], labels["question_log_intro"])
        ensure_file(candidates, labels["candidate_title"], labels["candidate_intro"])
        ensure_file(applied, labels["applied_title"], labels["applied_intro"])

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    entry_id = f"{stamp}-{entry_slug(args.question)}"
    web_sources, warnings = parse_web_sources(args.web_source)

    append(question_log, build_entry(args, entry_id, web_sources, labels), args.dry_run)
    if args.status in {"needs-confirmation", "candidate", "approved"}:
        append(candidates, build_candidate(args, entry_id, labels), args.dry_run)
    if args.status == "applied":
        append(applied, build_applied(args, entry_id, labels), args.dry_run)

    for warning in warnings:
        print(f"warning: {warning}")
    if not args.dry_run:
        print(f"logged: {entry_id}")
        print(f"directory: {log_dir}")


if __name__ == "__main__":
    main()
