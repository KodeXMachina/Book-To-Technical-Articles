# Playbook for Turning Books into Technical Articles

[Chinese](full-playbook.zh-cn.md) | [English](full-playbook.en.md)

> This is the English version of the original long playbook. The active language-neutral rules are maintained in the split references such as `output-contract.md`, `workflow.md`, `writing-style.md`, and `validation.md`.

This playbook came from a complete CUDA Programming Guide article-system conversion. It is not a book-specific table of contents. It is a reusable method for turning a technical book from PDF, figures, code, and chapter structure into materials that people can read and auditors can compare back to the source.

Core goal: **do not mechanically convert a book into Markdown; rewrite it into technical materials that help readers build models, write code, look up details, and verify source coverage.**

## 1. What the Final Deliverable Should Look Like

A complete book analysis result should include at least four layers:

| Layer | Output | Purpose |
| --- | --- | --- |
| Source parsing layer | `markdown_output/chapters/*.md`, images, code blocks | Preserve source structure for verification; readability is secondary. |
| Reader path layer | `course_materials/v3/<module>/<article>.md` | Help readers genuinely understand the material; this layer carries the article experience. |
| Reference supplement layer | reference patches or appendix articles | Carry APIs, macros, enums, limits, tables, and weak-coverage details. |
| Audit layer | `source_coverage_audit.md` | Record coverage differences against source chapters, figures, code, and tokens. |

Do not merge these layers into one file. The source parsing layer should be faithful; the reader path should be readable; the reference layer should be complete enough to look things up; the audit layer should be honest.

If a book needs stronger page-level provenance, figure/code extraction, Q&A backfill, and later blog derivation, use **Strict Knowledge Base Mode** in section 7. It strengthens the default flow but does not replace the main system of readable technical articles, reference patches, and coverage audits.

## 2. Core Judgments

### 2.1 Do Not Write Lesson Plans

Do not write articles as lesson plans with learning objectives, teaching activities, or exercises. Readers open an article to understand a technical problem, not to see how a teacher would teach it.

Better openings answer:

- Why this problem appears in real engineering work.
- What wrong code or bad decision appears if the reader misses it.
- What model the article will build.
- What engineering judgment the reader can make after reading.

### 2.2 Do Not Translate Mechanically

Do not translate a PDF paragraph by paragraph, and do not scatter source paragraphs into translated bullet lists. Mechanical translation gives an illusion of coverage, but the reading experience is poor and it does not help readers build higher-level structure.

A better approach:

- Preserve source concepts and terminology.
- Reorder explanations along the reader's understanding path.
- Add context, motivation, misconceptions, and engineering judgment.
- Put dense API details into a reference section or reference patch instead of the main narrative.

### 2.3 Do Not Only Summarize

A 600-page technical book cannot be compressed into a few thousand lines of summary. Summaries are good for quick orientation, not mastery. Main articles must be sufficiently developed, and reference patches must cover details.

Reasonable structure:

- Split by topic into modules.
- Split each module into multiple articles.
- Let each article revolve around an engineering problem.
- Generate reference patches for dense chapters.

### 2.4 Do Not Let Supplements Remain Detached Forever

Temporary supplements are useful during drafting, but the final reading path should not depend on a permanent two-track structure.

Better final state:

- Main articles carry the reading experience.
- Reference patches are linked from the index as lookup entries.
- The audit report clearly says which content is covered by the main path and which by patches.

## 3. Recommended Workflow

### Phase 1: Build the Source Parsing Layer

The goal is to convert the PDF into verifiable Markdown, not to write articles immediately.

Expected outputs:

- Chapter-split Markdown.
- Image asset directory.
- Code blocks preserved where possible.
- Tables preserved where possible.
- Traceable chapter numbers, page numbers, and titles.
- In strict mode, an extra page-level knowledge base with source IDs for key facts.

Notes:

- Check extracted images for transparency, black backgrounds, bad cropping, and duplicates.
- Image filenames should be stable and ideally include chapter/page information.
- Source front matter, copyright, trademarks, and index-like sections can be excluded when appropriate.
- In strict mode, use consistent source IDs: text `(P3)`, figure `(P5-Fig2)`, table `(P6-Table1)`, code `(P7-Code1)`.
- If OCR, figures, tables, or context are ambiguous, mark the uncertainty instead of guessing.
- When extracting images, keep one side under `2000px`; scale DPI to actual content to avoid oversized files.
- In strict mode, name images as `number_short-description.png`, derive the description from caption/context, sanitize it, and keep it under 40 characters.
- If a figure or table cannot be parsed reliably, keep the image link and mark that human completion is needed.

### Phase 2: Plan Top-Level Modules

Do not rush into writing. Read the table of contents, chapters, and density first, then propose a module plan.

Module principles:

| Principle | Meaning |
| --- | --- |
| Follow the reader's understanding path | Do not mechanically copy source chapters. |
| Group by engineering topic | Merge related chapters into topic modules. |
| Split dense topics | API, language, numeric, and interop chapters often need multiple articles. |
| Keep mapping traceable | Every module should list source chapters. |
| Avoid fixed-count thinking | Six courses may be too coarse; twelve modules may still be insufficient. |

The plan should include:

- Module title.
- Corresponding source chapters.
- Why the module is split this way.
- What problem each module solves.
- Planned article list.
- Sections excluded from the main path.

### Phase 3: Generate the First Reader-Facing Article Pass

The first pass should prioritize readability over reference completeness.

Suggested article skeleton:

```markdown
# Open with an engineering problem

## 1. Why this problem appears

## 2. Core model

## 3. Main explanation

## 4. Code path

## 5. Engineering judgment table

## 6. Source coverage supplement

## 7. Capability after reading
```

Guidance:

- Use Mermaid or tables for the core model where helpful.
- The code path should explain inputs, outputs, execution side, synchronization boundary, and error boundary.
- The engineering judgment table answers when to use or not use an approach.
- The source coverage supplement carries APIs, macros, limits, figures, and chapter gaps.

### Phase 4: Audit Source Coverage

After the first article pass, check against the source. Do not rely on impressions.

Audit targets:

| Target | Check |
| --- | --- |
| Chapters | Did every included source chapter enter the reading path? |
| Figures | Are source figures included and explained? |
| Code | Is key code migrated, rewritten, or explained? |
| API/token | Are functions, macros, enums, environment variables, and compiler options retained? |
| Tables | Are large tables preserved, compressed with explanation, or explicitly excluded? |
| High-risk chapters | Pay special attention to APIs, interop, language extensions, numeric functions, and system chapters. |

Coverage states:

| State | Meaning |
| --- | --- |
| Strong | Main explanation is sufficient and key details are preserved. |
| Medium | The topic is explained, but APIs or tables are incomplete. |
| Weak | The concept is mentioned but lacks supporting detail. |
| Missing | The content cannot be found in the reading path. |
| Excluded | Front matter, copyright, trademarks, or low-value material intentionally excluded. |

### Phase 5: Generate Reference Patches

Do not rewrite the main path after an audit. For weak or missing content, generate targeted reference patches.

A reference patch:

- Does not carry the main narrative.
- Is not a random list.
- Is written as a technical article plus itemized supplements.
- Compresses APIs, macros, enums, environment variables, limits, figures, and tables into an organized lookup surface.

Each reference patch should include:

- Corresponding article and source chapters.
- Why a separate patch exists.
- Explanation ordered by source order or engineering logic.
- Itemized supplements for weak/missing points.
- Quick reference tables for APIs, macros, env vars, and compiler options.
- Notes for source code, figures, and tables.
- Capability gained after reading.

### Phase 6: Update Index and Audit Conclusion

After patches are generated, update the global index and audit report.

The index should show:

- Main article path.
- Reference patch path.
- What each patch supplements.
- Recommended reading order.

The audit should update:

- File counts, line counts, code block counts, figure coverage, and table row counts.
- Remaining gaps.
- Closed gaps.
- Differences intentionally not replicated.

## 4. Technical Article Writing Style

### 4.1 Write for Engineering Readers

Readers are not memorizing definitions. They need to understand problems, write code, debug issues, and make trade-offs.

Good phrasing:

- "What engineering problem does this mechanism solve?"
- "What boundary appears if you do not use it?"
- "How does it differ from neighboring mechanisms?"
- "Where is the synchronization point in the code?"
- "This API returning does not mean the work has completed."
- "This configuration is a hint, not a hard guarantee."

Avoid:

- "In this lesson..."
- "Learning objective..."
- "Section summary..."
- "Source check..."
- "The following introduces several knowledge points..."

### 4.2 Open with a Real Problem

Do not start with encyclopedia definitions. Start from a real scenario.

Bad:

```text
CUDA Stream is an asynchronous execution mechanism in CUDA.
```

Better:

```text
After writing the first kernel, you soon hit a problem: the CPU has submitted work, the GPU has not finished it yet, and the next batch of data is ready. The value of streams is that they express which work must stay ordered and which work can overlap.
```

### 4.3 Concepts Should Land on Boundaries

Concepts in technical books are usually not isolated facts. They are boundaries:

| Concept | Boundary to explain |
| --- | --- |
| Stream | host return, GPU execution, same-stream ordering, cross-stream non-ordering |
| Event | record point, wait point, timing boundary |
| Unified Memory | unified address, migration, prefetch, advice, consistency |
| Graph | definition, instantiation, update, launch, capture restrictions |
| Atomic | operation, memory order, thread scope |
| Shared memory | visibility, lifetime, bank conflicts |
| Driver API | context, module, function, launch, version boundary |

### 4.4 Explain Code Execution Paths

Code cannot merely be pasted. Each core code block should explain:

- Whether it runs on host or device.
- Where inputs come from.
- Where outputs are written.
- Which APIs are asynchronous.
- Which call provides the synchronization boundary.
- Where errors may surface.
- Which parameters must match hardware capabilities.

In strict knowledge-base mode, each code snippet should also include:

| Field | Meaning |
| --- | --- |
| Function | What problem the code solves. |
| Key statements | Explain key statements, API calls, and parameters. |
| Inputs/outputs | Input data, output data, state changes. |
| API/library dependencies | Functions, libraries, macros, compiler options. |
| Source | Use `(P7-Code1)` or multiple source IDs. |

If the source splits one code path into declaration, initialization, implementation, and invocation, reconstruct the complete code and list all sources. If the source compares pre/post optimization, alternate implementations, or API paths, create a code comparison table with differences, trade-offs, performance traits, and use cases.

### 4.5 Tables Should Serve Judgment

Tables are not decoration. They help readers make decisions.

Recommended table types:

| Type | Purpose |
| --- | --- |
| Decision table | When to use A/B/C. |
| Lifecycle table | Create, use, sync, destroy. |
| API quick reference | Functions, macros, enums, fields. |
| Troubleshooting table | Symptom, possible cause, checkpoint. |
| Comparison table | Runtime vs Driver, IPC vs VMM, pageable vs pinned. |

### 4.6 Mermaid Should Express Structure

Mermaid is useful for:

- Platform stacks.
- Data flow.
- Lifecycles.
- stream/event dependencies.
- memory migration.
- graph instantiation and update.
- VMM reserve-map-access-release.

Do not draw diagrams for decoration. A diagram must answer a structural question.

## 5. Image Handling Rules

Source images should not merely be pasted. Each meaningful image needs a reading note.

Image principles:

| Principle | Meaning |
| --- | --- |
| Keep key figures | Architecture diagrams, flows, timelines, and performance diagrams should not be lost. |
| Stable links | Use relative paths, not temporary paths. |
| Explain images | Tell readers what to inspect, not just translated captions. |
| Check black backgrounds/cropping | PDF extraction may produce transparency or black-background problems. |
| Exclude meaningless images | Logos, covers, and copyright images can stay out of articles. |

A reading note should explain:

- What structure the image shows.
- Which arrow or region matters most.
- How it connects to the article's model.
- How it can be misread.

## 6. API/Reference Content Handling

Reference-heavy content can destroy readability. Put only the essentials in the main article, then centralize details in supplements.

### 6.1 Keep Only Understanding-Critical Items in the Main Path

For CUDA Graphs, the main article needs to explain:

- Why Graph exists.
- The difference between capture and explicit graph construction.
- The relationship between instantiate and launch.
- Why update has restrictions.

It should not list every node API in the main narrative.

### 6.2 List Families in the Supplement Section

In a source coverage supplement or reference patch, list families as fully as appropriate:

- API families.
- Macros.
- Enums.
- Struct fields.
- Environment variables.
- Compiler options.
- Limits.
- Version differences.

### 6.3 Large Tables Can Be Compressed, But Say So

Tables such as compute capability, math functions, C++ proposals, or DXGI formats do not always need item-by-item replication.

Reasonable handling:

- Use compressed tables for common items.
- Classify full-family items by category.
- If not replicating the full table, explicitly say the lookup method is retained while the original table is not copied item by item.
- Fully cover high-risk P0 areas when possible.

## 7. Strict Knowledge Base Mode

Strict knowledge-base mode is for tasks where the user explicitly needs page-level extraction, strong provenance, interactive Q&A backfill, or a structured knowledge base before article/blog derivation. It is heavier than the default flow but reduces omissions.

It does not replace the default flow. The default flow remains: source parsing preserves facts, the reader path provides readability, reference patches provide lookup detail, and the audit compares against the source. Strict mode adds finer constraints to extraction and later interaction.

### 7.1 When to Use It

| Scenario | Recommendation |
| --- | --- |
| Standard technical book for month-long study | Not required; default v3 article flow is usually better. |
| High API/reference density needing item-level gap checks | Recommended. |
| The user will frequently ask follow-up questions | Recommended. |
| Short document requiring a complete knowledge base | Recommended. |
| User only wants one readable article | Do not enable full strict mode; borrow only blog derivation rules. |

### 7.2 Strict Knowledge Base Outputs

Generate an additional knowledge-base Markdown file. Recommended sections:

| Section | Content |
| --- | --- |
| Domain overview | Core problem, application scenarios, overall reader model. |
| Topic hierarchy | Tree from domain to topics, subtopics, and specific points. |
| Code/config summary | Code snippets, configurations, commands, and APIs grouped by function. |
| Figure/table index | Figures, tables, flowcharts, architecture diagrams, and sources. |
| Unclear points | All uncertainty markers collected together. |
| Q&A | Confirmed Q&A backfill. |
| Update log | Summary of each knowledge-base change. |

A knowledge base is not a blog and not the final article. It is a factual warehouse emphasizing completeness, searchability, and traceability. Main articles and blogs can later be derived from it.

### 7.3 Page-Level Extraction and Source IDs

In strict mode, process pages before topic rewriting. Do not drop details just because later articles will rewrite them.

Source ID format:

| Content type | Format | Example |
| --- | --- | --- |
| Text point | `(Ppage)` | `(P3)` |
| Figure | `(Ppage-FigN)` | `(P5-Fig2)` |
| Table | `(Ppage-TableN)` | `(P6-Table1)` |
| Code | `(Ppage-CodeN)` | `(P7-Code1)` |
| Cross-page content | Multiple IDs | `(P5-Code1, P7-Code2)` |

If content is fuzzy, OCR is unreliable, or a figure/table cannot be interpreted automatically, preserve uncertainty, for example: `(Needs confirmation: the dashed arrow may indicate an asynchronous dependency, but the source caption does not say so.)`

### 7.4 Figures, Tables, and Flowcharts

Image extraction rules:

- Keep each image dimension under `2000px`.
- Scale DPI according to actual content to avoid blank margins and huge files.
- Use globally increasing numbers and short descriptions, such as `01_thread-hierarchy.png`.
- Prefer captions for descriptions; otherwise use nearby context; sanitize filenames and keep descriptions under 40 characters.
- Every figure used in articles or the knowledge base needs a reading note.

Table rules:

- Convert parseable tables into Markdown tables.
- Compress very large tables only with a clear compression principle.
- If a table image cannot be parsed reliably, keep the original image and mark it for human completion.

Flowchart and architecture diagram rules:

- Keep the image when the original structure is clear and add a reading note.
- Use Mermaid when it better expresses the logic.
- Mermaid should express structure, data flow, lifecycle, or dependency, not decoration.

### 7.5 Code Analysis and Code Comparisons

In strict mode, describe code snippets with fixed fields:

| Field | Content |
| --- | --- |
| Code snippet | Function name and source. |
| Function | What task the code completes. |
| Key statements | Explain statements, APIs, parameters, and boundaries. |
| Inputs/outputs | Inputs, outputs, state changes, sync result. |
| API/library dependencies | Functions, macros, libraries, compiler options, runtime environment. |
| Notes | Error boundaries, performance boundaries, version or platform limits. |

If a source splits one code example, reconstruct the complete code and list all source IDs. Do not preserve only one part because the example crosses pages.

If the source includes code comparisons, generate a comparison table:

| Comparison item | Version A | Version B |
| --- | --- | --- |
| Implementation | Describe path | Describe path |
| Key APIs | List APIs | List APIs |
| Performance traits | Throughput, latency, memory, sync differences | Throughput, latency, memory, sync differences |
| Use case | Suitable conditions | Suitable conditions |
| Risk | Possible failure points | Possible failure points |

### 7.6 Interactive Knowledge Completion

When the user asks follow-up questions in strict mode:

- Answer from the source parsing layer, knowledge base, and generated articles first.
- If the document does not mention the point, say so explicitly and propose a supplement.
- You may add simple examples, pseudocode, Mermaid, or comparison tables, but label source content and extended explanation separately.
- After user confirmation, backfill the conclusion into the relevant knowledge-base section.
- Add a `Q&A` block that records representative questions, question source, answer summary, and backfill location.
- Add an entry to the update log whenever the knowledge base changes.

Status labels such as "Phase 1: knowledge extraction in progress" apply only to strict interactive knowledge-base mode, not to every book-processing task.

### 7.7 Blog or Single-Article Derivation

A blog-style output is a derived artifact, not a replacement for the default v3 technical article system. It is useful after the knowledge base and main articles are stable, as a lighter entry point for readers.

Derivation rules:

- Title should convey a problem or benefit.
- Opening should say which knowledge base or book the article is derived from.
- Language can be more accessible, but technical accuracy must remain.
- Strongly related extended knowledge is allowed, but should stay under 20% of total length.
- Extended content must be marked clearly.
- Preserve core references such as section IDs or source IDs.
- The ending should summarize and avoid introducing many new concepts.

Blog shape:

| Section | Content |
| --- | --- |
| Guide | What problem this article solves and where it comes from. |
| Why the technology is needed | Open with an engineering scenario. |
| Core concept explanation | Use analogy, diagrams, and tables to reduce friction. |
| Practical example | Minimal code or flow. |
| Advanced points | Pitfalls, performance, versions, platforms. |
| Summary | Return to the key model and practical judgment. |

### 7.8 Batch Delivery Rules

Do not treat "stop after 20 pages" as a default rule. Default to completing an end-to-end pass when safe.

Split only when:

- The user explicitly requests chapter/page batches.
- One context cannot safely hold the full output.
- PDF extraction quality is poor and needs human confirmation.
- Strict mode has many uncertainty markers and continuing would amplify errors.

When batching, state completed range, uncertainty points, and next batch, but do not interrupt unnecessarily.

## 8. Coverage Priority

Handle audit gaps as P0/P1/P2.

| Priority | Definition | Handling |
| --- | --- | --- |
| P0 | Affects core knowledge integrity or engineering usability. | Must become an article or reference patch. |
| P1 | Does not affect the main path, but affects lookup/debugging. | Should be added to a reference patch. |
| P2 | Local source example symbols, platform helpers, low-value table rows. | Record in audit; do not force main-text coverage. |

P0 often includes:

- Language extensions and atomic memory model.
- Floating-point and numeric functions.
- Graph node/update/capture limits.
- Unified Memory advice/prefetch/range attributes.
- Driver JIT/link/module/entry point.
- VMM/IPC/interop system boundaries.
- Key source figures and key code paths.

## 9. Validation Checklist

Validate after every generation pass.

### 9.1 Files and Structure

- Markdown file count matches expectations.
- Global index links to all articles.
- Every article has a consistent skeleton.
- Reference patches are linked into the reading path.

### 9.2 Markdown Health

- Code fences are closed.
- Mermaid blocks use a fenced code block with `mermaid` info string.
- Image links exist.
- Tables are readable.
- No stale template residue remains.

Example stale template residue:

```text
Section summary
Source check
Generated article body
Explanation:
<details>
```

### 9.3 Coverage

- Included source chapters all have mappings.
- Source figure coverage is counted clearly.
- Key source code paths are migrated or explained.
- Weak coverage after API/token scanning is recorded.
- P0 gaps are closed.

### 9.4 Readability Spot Check

Sample at least one article per module and check:

- The opening reads like a technical article.
- It is not a pile of facts.
- It provides engineering judgment.
- It explains code.
- It uses figures or tables where helpful.
- It can be understood without the source PDF.

Additional strict-mode checks:

- The knowledge base contains `Q&A` and update-log sections.
- Search confirms key rules or real content, such as `P5-Fig2`, uncertainty markers, `Q&A`, update log, `2000px`, code comparison, and extension labels.
- Code snippets include function, key statements, inputs/outputs, API/library dependencies, and source IDs.
- Split code has been reconstructed, or the reason it cannot be reconstructed is stated.

## 10. File Naming Suggestions

Recommended directory structure:

```text
<Book Name>/
  original.pdf
  pdf_to_markdown_plan.md
  markdown_output/
    chapters/
    assets/images/
  course_materials/
    00-course-plan.md
    source_coverage_checklist.md
    v3_source_coverage_audit.md
    v3/
      00-index.md
      01-module-name/
        01-article-name.md
        02-article-name.md
      02-module-name/
        ...
```

Naming rules:

- Modules use two-digit numbering.
- Articles use two-digit numbering.
- Filenames use English phrases to avoid tooling issues with non-English paths.
- Titles may use the selected output language.
- Audit files stay separate.
- Do not delete intermediate versions unless traceability is no longer needed.

In strict knowledge-base mode, add:

```text
  knowledge_base/
    00-knowledge-index.md
    01-domain-overview.md
    02-topic-tree.md
    03-code-and-config-index.md
    04-qa-and-update-log.md
```

`knowledge_base/` is optional. Small projects may use a single `knowledge_base.md` instead.

## 11. Definition of Done

A book-derived technical article system is complete only when it has:

- Source parsing layer.
- Top-level course/module plan.
- Readable main articles.
- Reference patches or equivalent supplement sections.
- Global index.
- Coverage audit report.
- Key figures included or excluded with reasons.
- P0 gaps closed.
- Markdown structure, code fences, and image links validated.
- A reading path for sequential reading and reference patches for detail lookup.

When strict knowledge-base mode is enabled, also require:

- Page-level source IDs.
- Unified numbering for key figures, tables, and code.
- Fuzzy content collected into unclear-points sections.
- Confirmed Q&A backfilled into `Q&A` and relevant sections.
- Update log tracks each knowledge-base change.
- Blogs or single articles remain derived artifacts, not replacements for main articles and reference patches.

## 12. Execution Order for a New Book

For the next technical book, proceed in this order:

1. Parse the PDF and generate chapter Markdown, images, and code blocks.
2. Scan the table of contents and content density.
3. Write `pdf_to_markdown_plan.md` or an equivalent parsing plan.
4. Write `00-course-plan.md` and decide modules and reading path.
5. Generate first-pass main articles.
6. Manually spot-check readability and remove lesson-plan/mechanical tone.
7. Write `source_coverage_audit.md`.
8. Generate reference patches for P0/P1 gaps.
9. Update the global index.
10. Run validation scripts.
11. Update final audit status.

If strict knowledge-base mode is enabled, insert after step 1:

- Generate a knowledge base for the document.
- Establish page-level source IDs.
- Summarize code/configuration, figures/tables, and unclear points.
- Backfill `Q&A` and update logs after later user-confirmed answers.

## 13. Most Important Quality Standards

Final materials must satisfy three goals:

| Standard | Meaning |
| --- | --- |
| Readable | Feels like carefully written technical articles, not automatic summaries. |
| Findable | APIs, macros, figures, code, and limits can be found through the index or supplements. |
| Traceable | Content maps back to source chapters, figures, code, and tokens for coverage checks. |

If the three conflict, prioritize:

1. Keep main articles readable.
2. Let reference patches preserve details.
3. Let the audit report record differences.

Do not destroy the reading experience to look complete, and do not hide coverage gaps to make the article feel lighter.
