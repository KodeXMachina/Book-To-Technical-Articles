# Strict Knowledge Base Mode

Use strict mode when the user requests page-level extraction, strong provenance, interactive Q&A backfill, or a factual knowledge base before article derivation.

## Language

Use the project `Output language` for reader-facing knowledge-base text. Source IDs, code, API names, commands, and quoted source titles stay unchanged. For bilingual projects, keep paired explanations aligned and share the same source IDs.

Use localized uncertainty and update markers:

| Function | Chinese | English |
| --- | --- | --- |
| Uncertainty | `待确认` | `Needs confirmation` |
| Q&A | `Q&A` | `Q&A` |
| Update log | `更新记录` | `Update log` |

Run validation with `validate_book_materials.py --strict --language auto`, or force `--language zh` / `--language en` when needed.

## Additional outputs

```text
knowledge_base/
  00-knowledge-index.md
  01-domain-overview.md
  02-topic-tree.md
  03-code-and-config-index.md
  04-qa-and-update-log.md
```

A single `knowledge_base.md` is acceptable for small sources.

## Source IDs

Use consistent IDs:

| Content | Format |
| --- | --- |
| Text point | `(P3)` |
| Figure | `(P5-Fig2)` |
| Table | `(P6-Table1)` |
| Code | `(P7-Code1)` |
| Cross-page code | `(P5-Code1, P7-Code2)` |

Mark uncertainty with the selected output language marker, for example `（待确认：...）` or `(Needs confirmation: ...)`; do not hide OCR, image, table, or context ambiguity.

## Strict extraction rules

Process pages before topic rewriting. Extract or reference key images, tables, code, and configuration. Images should keep one side under 2000px when generated from page renders. Name images with a stable number and short description.

For code, add function, key statements, inputs/outputs, dependencies, notes, and source IDs. If a source splits code across pages, reconstruct it when possible and list all source IDs. If there are variants, add a comparison table.

## Q&A backfill

When answering later questions, answer from the source parsing layer, knowledge base, and generated articles. If the document does not mention something, say so explicitly and label any extension. After user confirmation, add Q&A and update-log entries in the selected output language.

Only strict mode needs stage labels. Use localized labels when requested; otherwise keep status messages concise.
