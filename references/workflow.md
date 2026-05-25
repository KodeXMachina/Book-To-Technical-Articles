# Workflow

## Phase 0: Decide output language

Resolve `Output language` before writing reader-facing materials. Use the user's explicit request first, then existing project metadata, then the dominant language of existing articles, then the current conversation language. Ask a short confirmation question if the language is still ambiguous.

Record the decision in `pdf_to_markdown_plan.md` or `course_materials/00-course-plan.md`:

```text
Output language: zh | en | bilingual
```

## Phase 1: Build source parsing layer

Inspect the PDF or source docs first. Record page count, metadata, outline entries, image count, code-font clues, OCR needs, and available local tooling. For PDFs, start with `scripts/inspect_pdf.py`; when source images matter, use `scripts/extract_pdf_images.py` or a project-specific extractor. Then generate chapter Markdown, image assets, code blocks, tables where possible, and manifests.

Do not start with course articles. The source layer is the audit base.

## Phase 2: Plan modules

Read the table of contents and density. Group by reader understanding path and engineering topic. Do not mechanically mirror the original chapters when a better learning path exists. The plan should include module title, source chapter mapping, rationale, problem solved, article list, excluded sections, and output language.

## Phase 3: Write first article pass

Prioritize readability and mental models in the selected output language. Use problem-driven openings, Mermaid/table models where helpful, code-path explanations, and engineering judgment tables. Keep API catalogs out of the main narrative unless essential.

## Phase 4: Audit source coverage

After writing, compare generated materials against the source parsing layer. Check chapter mapping, images, key code, table treatment, API/token retention, and high-risk reference sections. Do not rely on memory or impressions.

## Phase 5: Add reference patches

For weak or missing coverage, add targeted reference patches. Keep them article-like, not random lists. Include source mapping, why the patch exists, ordered details, weak/missing supplements, API/token tables, source code/image/table notes, and capability gained.

## Phase 6: Update index and audit

Add patches to the reading path. Update counts for files, lines, code blocks, images, tables, and remaining gaps. Mark intentional non-replication clearly.

## Phase 7: Reader Q&A feedback loop

When readers ask questions, search local project materials first: source Markdown, generated articles, reference patches, coverage audit, and strict knowledge base when present. If local evidence is insufficient or the question needs current context, use web sources as supplements and cite their URLs. Label book/project evidence, web supplements, and inference separately.

Answer in the reader's current language unless the project has an explicit output-language constraint. Backwrite accepted improvements in the project's selected output language. For bilingual projects, keep paired explanations aligned rather than letting one language drift.

After answering, judge whether the question reveals an article gap. If it does, ask the user before backwriting. Backwrite the underlying explanation gap organically: add a bridge, table, code-path explanation, misconception note, or reference patch instead of copying the raw Q&A. Keep logs under `course_materials/reader_questions/` when the project tracks reader feedback.

## Batch rules

Do not stop every fixed number of pages. Split only when the user asks, context is unsafe, extraction quality needs confirmation, or strict mode uncertainty would compound errors.
