# Book to Technical Articles Skill

[中文](README.md) | [English](README.en.md)

> Convert technical books, PDFs, extracted Markdown, or long-form documentation into readable, auditable, and continuously improvable technical article systems. Output can be Chinese, English, or bilingual, chosen from the user request, project context, or a short confirmation question.

## What This Skill Solves

Many technical books should not be directly translated or shallowly summarized. Direct translation preserves the original order but may not match the reader's learning path. Shallow summaries often lose code, figures, APIs, tables, constraints, and edge cases.

This skill builds layered materials: a traceable source parsing layer, reader-facing technical articles, targeted reference patches, source coverage audits, and a reader Q&A feedback loop.

## Language Support

Supported output language modes:

- `zh`: Chinese technical articles and reader Q&A logs.
- `en`: English technical articles and reader Q&A logs.
- `bilingual`: Chinese and English output with aligned explanations, evidence, and source coverage.

Language selection order:

1. Use the language explicitly requested by the user.
2. If the project already records `Output language:`, keep it.
3. If existing articles have a dominant language, continue that language.
4. Otherwise infer from the current conversation language.
5. If still ambiguous, ask for a short confirmation.

## Use Cases

- Turn a technical book or official documentation into a Chinese, English, or bilingual article/course system.
- Extract chapters, images, code, and tables from PDFs while keeping audit evidence.
- Reorganize book knowledge around engineering problems instead of paragraph-by-paragraph translation.
- Check whether generated articles miss key APIs, code paths, figures, or dense reference content.
- Answer reader questions from source-backed evidence and backwrite valuable confusion signals into articles.
- Maintain a reusable workflow for GitHub repositories, course materials, or knowledge bases.

## Output Structure

```text
<Book Name>/
  pdf_to_markdown_plan.md          # includes Output language: zh | en | bilingual
  markdown_output/                 # source parsing layer, factual and traceable
    README.md
    chapters/
    assets/images/
    work/
  course_materials/                # reader-facing article layer
    00-course-plan.md              # includes Output language
    source_coverage_checklist.md
    source_coverage_audit.md
    validation_report.md
    reader_questions/              # only needed after reader questions appear
      question-log.md
      backwrite-candidates.md
      applied-backwrites.md
    v1/ or v3/
      00-index.md
      01-module-name/
        01-article-name.md
```

Core layering principles:

- `markdown_output/` preserves extracted source facts for tracing and audit.
- `course_materials/` contains the articles readers actually read.
- Reference patches cover dense APIs, macros, enums, tables, limits, and other details.
- Coverage audits record strong, weak, missing, and intentionally excluded coverage.
- Reader Q&A feedback turns reader questions into article improvement signals.

## Workflow

1. Decide and record `Output language`.
2. Inspect source materials: PDF pages, outline, images, fonts, code blocks, OCR risk, and existing Markdown.
3. Build `markdown_output/` first so the factual layer is traceable.
4. Write `pdf_to_markdown_plan.md` with tools, splitting strategy, output language, risks, and source ranges.
5. Plan modules by reader learning path rather than copying the table of contents.
6. Write technical articles in the selected language: problem opening, mental model, code path, judgment table, and source coverage supplement.
7. Audit source coverage across chapters, images, code, API/token names, tables, and high-risk reference sections.
8. Add reference patches for weak coverage.
9. Answer reader questions from local evidence first; use web sources only with citations.
10. After user confirmation, organically backwrite valuable reader questions into articles.

## Reader Q&A Feedback Loop

Reader questions are valuable because they show where an article may not be clear enough. This skill does not recommend pasting raw Q&A into articles. Instead, rewrite the underlying gap into natural article content:

- Add a bridging paragraph.
- Add a code-path explanation.
- Add a judgment table.
- Add a misconception note.
- Add a reference patch.

When answering reader questions, cite sources and distinguish:

- Book/project evidence: extracted source, generated articles, patches, or audits.
- Web supplements: official docs, standards, source repositories, release notes, or other external sources.
- Inference: reasoning that connects evidence to the answer.

## Repository Layout

```text
.
├── README.md
├── README.en.md
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── coverage-audit.md
│   ├── full-playbook.zh-cn.md
│   ├── full-playbook.en.md
│   ├── output-contract.md
│   ├── reader-qa-feedback-loop.md
│   ├── strict-knowledge-base-mode.md
│   ├── validation.md
│   ├── workflow.md
│   └── writing-style.md
├── scripts/
│   ├── extract_pdf_images.py
│   ├── inspect_pdf.py
│   ├── qa_backwrite_log.py
│   ├── scan_markdown_stats.py
│   ├── token_coverage.py
│   └── validate_book_materials.py
└── tests/
    ├── test_qa_backwrite_log.py
    └── test_validate_book_materials.py
```

## Installation

Copy or symlink this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R book-to-technical-articles ~/.codex/skills/
```

Invoke it explicitly with:

```text
Use $book-to-technical-articles to convert this technical book into technical articles in the requested or inferred language, with source parsing, reference patches, coverage audit, and reader Q&A feedback.
```

## Useful Scripts

```bash
scripts/inspect_pdf.py <book.pdf> --markdown
scripts/extract_pdf_images.py <book.pdf> <outdir> --manifest <json>
scripts/scan_markdown_stats.py <paths...> --markdown
scripts/qa_backwrite_log.py <project-root> --language en --question "..." --answer-summary "..."
scripts/validate_book_materials.py <project-root> --scope project --language auto --markdown
scripts/validate_book_materials.py . --scope skill --markdown
scripts/token_coverage.py --source <source paths...> --target <article paths...> --markdown
```
