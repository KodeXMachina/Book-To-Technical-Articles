# Coverage Audit and Reference Patches

## Audit dimensions

| Dimension | Check |
| --- | --- |
| Chapters | Every included source chapter maps to a reader article or patch. |
| Images | Key images are referenced and explained; excluded images have reasons. |
| Code | Key code paths are migrated, rewritten, or explained. |
| API/token | Functions, macros, enums, environment variables, flags, and types are retained or logged as weak coverage. |
| Tables | Large tables are preserved, compressed with rules, or intentionally not replicated. |
| High-risk sections | Language extensions, numerical behavior, API references, interop, memory/system boundaries, and platform restrictions get extra checks. |

## Coverage status

| Status | Meaning |
| --- | --- |
| Strong | Main article explains the topic and key details are preserved. |
| Medium | Topic is understandable, but API/table/detail coverage is incomplete. |
| Weak | Concept is mentioned without enough detail for use or audit. |
| Missing | No generated reading path covers the source item. |
| Excluded | Front matter, copyright, trademarks, decorative images, or low-value material intentionally omitted. |

## Priority

| Priority | Meaning | Action |
| --- | --- | --- |
| P0 | Affects core knowledge completeness or engineering usability. | Must write article or reference patch. |
| P1 | Does not block the main path but matters for lookup/debugging. | Add to reference patch when feasible. |
| P2 | Local helper symbols, low-value rows, obvious examples. | Record in audit if useful; do not force into prose. |

## Reference patch structure

Each patch should include source article/chapter mapping, why it exists, ordered explanation, weak/missing补全, API/token quick tables, source code/image/table notes, and capability gained. Add patches to the total index and update audit counts.
