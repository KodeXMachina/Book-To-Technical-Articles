# Validation

Run validation after every generation or substantial revision. Use `validate_book_materials.py --scope project --language auto` for generated book projects and `--scope skill` for this repository.

## Structural checks

- Expected Markdown files exist.
- Output language is recorded in the plan or clearly inferable from existing materials.
- Index links resolve.
- Every article has a consistent skeleton in the selected output language.
- Reference patches are linked from the reading path.
- Audit and checklist files exist.
- Reader-question logs exist when Q&A backfill or article backwrites were performed.

## Markdown health checks

- Code fences are balanced.
- Mermaid fences use `mermaid` info string.
- Image links exist.
- Tables are readable.
- Old template residue is absent outside fenced code examples. The validator checks Chinese and English residues such as `本段主旨`, `原文核对`, `中文教材正文`, `讲解：`, `Section summary`, `Source check`, `Generated article body`, `Explanation:`, and `<details>`.
- Use `--exclude` for archived source playbooks or reference files that intentionally quote forbidden examples.

## Coverage checks

- Included source chapters have mappings.
- Key source images are counted and explained.
- Key source code is migrated or explained.
- API/token scan weak coverage is recorded.
- P0 gaps are closed or documented as blockers.
- Reader-question backwrites cite the local evidence and any web supplements used.

## Reader Q&A checks

For answered reader questions, confirm the answer separates book/project evidence, web supplements, and inference. For accepted backwrites, confirm the raw Q&A was not pasted into the article and the explanation was integrated as a bridge, table, code path, misconception note, or reference patch in the project's selected output language.

## Readability spot checks

Sample at least one article per module. Confirm the opening is problem-driven, not a definition dump; the article explains code; tables/diagrams help judgment; and the article can be understood without the source PDF.

## Strict-mode additional checks

Run strict checks with `--language auto`, `--language zh`, or `--language en` as appropriate. The validator accepts Chinese markers such as `待确认` and `更新记录`, and English markers such as `Needs confirmation` and `Update log`. Confirm code snippets have function, key statements, inputs/outputs, dependencies, and source IDs.
