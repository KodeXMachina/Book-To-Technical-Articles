---
name: book-to-technical-articles
description: Use when Codex is asked to turn technical books, PDFs, extracted Markdown, or long documentation into traceable technical article systems; choose an output language from context or confirmation; audit or validate book-derived materials; answer reader questions with cited evidence; or improve articles from reader confusion.
---

# Book to Technical Articles

Use this skill to turn a technical book or long technical document into an article system that readers can follow and auditors can trace back to the source. Do not mechanically translate the book. Preserve a source parsing layer, write reader-facing articles in the selected output language, add reference patches for dense details, answer reader questions from traceable evidence, and produce an honest coverage audit.

## Choose the Output Language

Decide the output language before planning articles:

1. Use the language explicitly requested by the user: `zh`, `en`, or `bilingual`.
2. If the project already has `Output language:` in `pdf_to_markdown_plan.md` or `course_materials/00-course-plan.md`, keep it.
3. If existing articles already establish a dominant language, continue that language.
4. If no project signal exists, infer from the current user request.
5. If the target language is still ambiguous, ask a short confirmation question before writing reader-facing materials.

For bilingual output, keep source mapping and filenames shared. Write article titles, headings, captions, Q&A logs, and reader-facing explanations in both languages only where the user requests bilingual delivery; otherwise use one selected language consistently.

## Choose the Mode

- Use the default article-system mode for most technical books: source Markdown, course plan, articles, reference patches, audit, validation.
- Use strict knowledge-base mode when the user asks for page-by-page extraction, strong provenance, Q&A backfill, or future interactive querying. Read `references/strict-knowledge-base-mode.md` before writing outputs.
- Use reader Q&A feedback mode when readers ask about unclear points, source facts, generated articles, or how to improve an explanation. Read `references/reader-qa-feedback-loop.md` before answering or backwriting.
- Use blog/single-article derivation only after a source layer or knowledge base exists, or when the user explicitly asks for a lightweight article.
- Split delivery only when the user asks for batches, context cannot safely hold the task, PDF extraction quality is poor, or strict mode has many uncertain items.

## Default Output Contract

Create or update a project with four core layers and an optional reader-feedback layer:

```text
<Book Name>/
  pdf_to_markdown_plan.md          # include Output language: zh | en | bilingual
  markdown_output/
    README.md
    chapters/
    assets/images/
    work/validation_report.md
  course_materials/
    00-course-plan.md              # include Output language
    reader_questions/              # optional after first reader question
    source_coverage_checklist.md
    source_coverage_audit.md
    validation_report.md
    v1/ or v3/
      00-index.md
      01-module-name/
        01-article-name.md
```

Keep layers separate: `markdown_output` is factual and traceable; `course_materials` is readable in the selected output language; reference patches are for dense API/table/detail coverage; audit files are for coverage truth. Read `references/output-contract.md` for naming and Definition of Done.

## Workflow

1. Inspect the source: identify PDFs, existing Markdown, assets, outlines, page count, images, code fonts, and prior project conventions.
2. Decide and record `Output language` before article planning.
3. Build the source parsing layer before writing articles. Preserve chapter/page boundaries, code blocks, tables when possible, stable image links, and extraction manifests.
4. Write `pdf_to_markdown_plan.md` or an equivalent parsing plan that records tool choices, split strategy, source ranges, output language, and known extraction risks.
5. Plan modules before writing articles. Group by reader understanding path and engineering topics, not by blindly copying the original table of contents.
6. Generate reader-facing technical articles in the selected language. Each article should answer an engineering problem, explain the model, explain code execution paths, include judgment tables, and include a source coverage supplement section.
7. Audit coverage after the first article pass. Check chapters, images, code, API/token names, tables, and high-risk reference sections.
8. Add reference patches for weak or missing P0/P1 coverage. Do not bloat the main narrative with API catalogs.
9. For reader questions, answer in the user's current language unless the project requires another language; use web sources only as labeled supplements with URLs; then ask before writing the question direction back into articles.
10. Update index, checklist, audit conclusion, validation report, and reader-question logs when relevant. Do not claim coverage without evidence.

Read `references/workflow.md` for phase-level details and `references/coverage-audit.md` for audit and patch rules.

## Writing Rules

- Start from real engineering problems, not lesson-plan phrases such as “本节学习” or “Learning objectives”.
- Reorganize source knowledge into an understanding path; do not produce paragraph-by-paragraph translation.
- Explain code by execution side, inputs, outputs, sync/error boundary, dependencies, and hardware/API constraints where relevant.
- Use Mermaid only for structure, lifecycle, dependency, or data flow.
- Give every important source image a reading note in the selected output language; exclude decorative/legal images when appropriate.
- Keep main articles readable; move exhaustive APIs, macros, enums, environment variables, limitations, and large tables into supplement sections or reference patches.

Read `references/writing-style.md` for detailed article, image, code, table, Mermaid, and reference handling rules.

## Bundled Scripts

Use scripts when they fit the project instead of rewriting one-off checks:

- `scripts/inspect_pdf.py <book.pdf> --markdown`: inspect page count, metadata, outline, fonts, image refs, and likely OCR needs before conversion.
- `scripts/extract_pdf_images.py <book.pdf> <outdir> --manifest <json>`: render placed PDF image regions to white-background PNG files and write an image manifest.
- `scripts/scan_markdown_stats.py <paths...> --markdown`: count Markdown files, lines, code fences, Mermaid blocks, images, links, and table-like lines.
- `scripts/validate_book_materials.py <project-root> --scope project --language auto --markdown`: check generated book layers, code fence balance, image/Markdown links, stale template residue, reader-question logs, and optional strict-mode markers.
- `scripts/validate_book_materials.py <skill-root> --scope skill --markdown`: check this skill repository without requiring generated book layers.
- `scripts/token_coverage.py --source <source paths...> --target <article paths...> --markdown`: compare API-like tokens by token kind and source location to find possible weak coverage.
- `scripts/qa_backwrite_log.py <project-root> --language zh --question "..." --answer-summary "..."`: append a structured reader question and backwrite candidate record.

Scripts are intentionally generic. Patch or replace them with project-specific converters when the PDF structure demands it. Use `--exclude` on validation and `--ignore-file` on token coverage to reduce known project-specific noise.

## Reference Navigation

- Read `references/output-contract.md` and `references/workflow.md` by default for full book conversion.
- Read `references/writing-style.md` before generating or revising article prose.
- Read `references/coverage-audit.md` before writing audits or reference patches.
- Read `references/reader-qa-feedback-loop.md` before answering reader questions, using web supplements, or backwriting unclear points into articles.
- Read `references/strict-knowledge-base-mode.md` only when strict mode is selected.
- Read `references/validation.md` before final checks.
- Read `references/full-playbook.zh-cn.md` for the Chinese original playbook, or `references/full-playbook.en.md` for the English version, only when the long historical playbook is needed.

## Completion Standard

A task is done only when readers can follow the generated index, key details can be found in reference patches or supplement sections, reader questions are answered with labeled evidence, and the audit honestly maps source chapters/images/code/tokens to generated materials. If readability, reference completeness, and auditability conflict, keep the main articles readable, put details in reference patches, and record remaining gaps in the audit.
