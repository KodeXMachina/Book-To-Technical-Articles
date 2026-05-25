# Output Contract

## Output language

Every project should record one output language decision before article generation:

```text
Output language: zh | en | bilingual
```

Use this value for article titles, headings, image notes, Q&A logs, index text, and reference patches. `markdown_output/` remains source-oriented and does not need to be translated unless the user asks.

## Project layers

| Layer | Typical path | Purpose |
| --- | --- | --- |
| Source parsing | `markdown_output/chapters/*.md`, `assets/images/`, `work/*.json` | Preserve source structure and facts for audit; readability is secondary. |
| Reader path | `course_materials/v1/` or `course_materials/v3/` | Technical articles in the selected output language. |
| Reference patch | articles under the relevant module or `reference-patches/` | Dense APIs, macros, enums, tables, images, limits, weak coverage supplements. |
| Audit | `source_coverage_audit.md`, `source_coverage_checklist.md` | Honest source-to-output coverage record. |
| Reader feedback | `course_materials/reader_questions/*.md` | Optional after reader questions: evidence, backwrite candidates, and applied explanation improvements. |

## Recommended project tree

```text
<Book Name>/
  original.pdf
  pdf_to_markdown_plan.md
  markdown_output/
    README.md
    toc.json
    chapters/
    assets/images/
    work/
      document_meta.json
      outline.json
      section_map.json
      image_manifest.json
      validation_report.md
  course_materials/
    README.md
    00-course-plan.md
    source_coverage_checklist.md
    source_coverage_audit.md
    validation_report.md
    reader_questions/
      question-log.md
      backwrite-candidates.md
      applied-backwrites.md
    v1/
      00-index.md
      01-module-name/
        README.md
        01-article-name.md
```

Use English slugs for directories and filenames. Titles inside Markdown should use the selected output language. Use two-digit module and article numbers. Keep intermediate manifests when they support reruns or audit.

## Reader Q&A records

Reader-question records are optional until the first reader question appears. When used, keep them separate from the article path:

- `question-log.md`: raw reader question, local evidence, optional web sources, answer summary, and unresolved points.
- `backwrite-candidates.md`: questions that reveal reusable explanation gaps and suggested article targets.
- `applied-backwrites.md`: confirmed article edits, changed files, rationale, and whether audit/index updates were needed.

Web sources are allowed for current or external context, but each source must be named and linked. Never let a web source silently override the book; note the difference when book material is outdated or incomplete.

## Article skeleton

Use headings in the selected output language. Preserve these functions even if wording changes:

| Function | Chinese example | English example |
| --- | --- | --- |
| Problem opening | 这个问题为什么会出现 | Why This Problem Appears |
| Core model | 核心模型 | Core Model |
| Main explanation | 主线讲解 | Main Explanation |
| Code path | 代码路径 | Code Path |
| Engineering judgment | 工程判断表 | Engineering Judgment |
| Source supplement | 原书覆盖补全区 | Source Coverage Supplement |
| Reader capability | 读完应该形成的能力 | Capability After Reading |

Example shape:

```markdown
# Problem-driven title in the selected language

> Source map: Chapter X, Section Y

## 1. Problem opening
## 2. Core model
## 3. Main explanation
## 4. Code path
## 5. Engineering judgment
## 6. Source coverage supplement
## 7. Capability after reading
```

The exact headings can be adapted, but preserve the functions: problem, model, explanation, code path, engineering judgment, source supplement, and reader capability.

## Definition of Done

- Output language is recorded or clearly inferable from the project.
- Source parsing layer exists and is traceable.
- Course/module plan exists before or with articles.
- Reader-facing articles exist and are indexed.
- Reference patches or equivalent supplement sections cover dense details.
- Coverage audit exists and distinguishes strong, medium, weak, missing, and excluded content.
- Reader Q&A logs exist when questions were answered or used for article backwrites.
- Key images are included or excluded with a reason.
- P0 gaps are closed or explicitly called out as blockers.
- Markdown structure, code fences, image links, and index links validate.
