# Writing Style

## Language discipline

Write reader-facing material in the selected output language: `zh`, `en`, or `bilingual`. Do not switch languages mid-article except for source terms, API names, code, command output, or quoted source titles. For bilingual output, keep paired sections equivalent in meaning and source coverage.

## Avoid these patterns

- Do not write lesson-plan prose such as “学习目标”, “教学活动”, “本节学习”, “Learning objectives”, or “In this lesson”.
- Do not mechanically translate paragraph by paragraph.
- Do not compress a large technical book into a shallow summary.
- Do not leave supplements detached forever; fold them into the index or reference patch layer.

## Prefer this prose shape

Open with why the engineering problem appears, what breaks if the reader misses it, what model the article builds, and what decision the reader can make after reading.

Concepts should land on boundaries: lifecycle, ownership, synchronization, visibility, error timing, version support, API return semantics, memory location, or performance constraints.

Use localized headings naturally. A Chinese article may use headings such as `核心模型` and `代码路径`; an English article may use headings such as `Core Model` and `Code Path`. Preserve the function, not the exact wording.

## Code explanation checklist

For every core code block, explain:

- where it runs, such as host/device/client/server/build-time;
- where inputs come from;
- where outputs or state changes go;
- what is synchronous/asynchronous;
- where errors surface;
- what parameters must match API, hardware, version, or platform constraints.

In strict mode, add function, key statements, inputs/outputs, dependencies, notes, and source IDs.

## Tables and diagrams

Use tables for decisions, lifecycles, API quick reference, troubleshooting, and comparisons. Use Mermaid only for structure, data flow, lifecycles, dependencies, and state transitions.

## Image handling

Keep key architecture, flow, timeline, performance, and UI/reference images. Check transparency, black backgrounds, cropping, and duplicates. Give each important image a reading note in the selected output language: what it shows, which region matters, how it connects to the model, and how it can be misread.

## Reference handling

Main articles should include only details required for understanding. Put full API families, macros, enums, fields, environment variables, compiler options, limits, version differences, and large tables in supplement sections or reference patches. Large tables may be compressed if the compression rule is stated.
