# Reader Q&A Feedback Loop

Use this workflow when readers ask questions about generated articles, source chapters, code examples, diagrams, or unclear explanations.

## Goals

- Answer the reader from the book-derived material first.
- Use web sources only as labeled supplements, never as a silent replacement for the book.
- Treat every question as a signal that the current article may have a missing bridge.
- Ask for confirmation before changing articles based on a question.
- Keep Q&A answers in the user's current language unless the project explicitly requires another output language.

## Answering Rules

1. Search local project materials before answering: `markdown_output/`, `course_materials/`, reference patches, audits, and `knowledge_base/` if present.
2. If local material is insufficient, web sources may be used. Prefer official documentation, standards, source repositories, vendor docs, or primary references.
3. Separate evidence types in the answer:
   - **Book/project evidence**: facts from extracted source or generated materials.
   - **Web supplement**: current or external context with URL and source name.
   - **Inference**: reasoning that connects evidence to the reader's question.
4. If the source does not answer the question, say so directly. Do not imply book coverage that does not exist.
5. Avoid long copied excerpts. Summarize and cite.

## Language Rules

- Answer in the reader's current language by default.
- If the project has `Output language: zh`, `en`, or `bilingual`, use that language for article backwrites and persistent logs.
- In bilingual projects, keep paired explanations aligned and cite the same evidence in both languages.
- Use `scripts/qa_backwrite_log.py --language zh` or `--language en` to create localized Q&A log headings.

## Web Source Rules

Use web search when the user asks for current facts, ecosystem status, version behavior, standards, official API details, or external context beyond the book. Cite links in the answer. Mark web-derived claims separately from book-derived claims, especially when a newer web source updates or contradicts the book.

Preferred source order:

1. Official documentation, standards, specifications, source repositories, release notes.
2. Maintainer or vendor technical articles.
3. Reputable educational references.
4. Community posts only when they explain practice clearly and are labeled as community evidence.

## Backwrite Decision

After answering, decide whether the question reveals a reusable reader gap:

| Signal | Backwrite? |
| --- | --- |
| Reader missed a key prerequisite or mental model | Yes |
| Reader misunderstood an article transition | Yes |
| Reader asks for a code-path explanation that should exist | Yes |
| Reader asks for external historical/current context only | Maybe, as a note or reference patch |
| Reader asks a one-off environment/debug question | Usually no |

Before editing articles, ask the user whether to write the question direction back into the article system.

## Organic Backwrite Pattern

Do not paste the raw question and answer into the article. Rewrite the underlying gap into the same article style and selected output language:

- Add a bridging paragraph where the reader likely got lost.
- Add a small judgment table when the answer depends on trade-offs.
- Add a code-path subsection when the gap is execution order or object lifetime.
- Add a misconception section only when it fits the article's tone.
- Add a reference patch when the answer is dense, external, or too detailed for the main flow.

Every applied backwrite should update the index or audit if it changes coverage.

## Suggested Files

```text
course_materials/
  reader_questions/
    question-log.md
    backwrite-candidates.md
    applied-backwrites.md
```

Use `scripts/qa_backwrite_log.py` to append structured entries when the project keeps reader-question records.
