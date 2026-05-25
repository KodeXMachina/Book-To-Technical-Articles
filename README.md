# Book to Technical Articles Skill

[中文](README.md) | [English](README.en.md)

> 将技术书籍、PDF、已抽取 Markdown 或长篇技术文档，转化为可阅读、可审计、可持续修订的技术文章体系。输出语言可以是中文、英文或双语，由用户指定、项目上下文推断，或在不明确时由 AI 询问确认。

## 这个 Skill 解决什么问题

很多技术书籍不适合直接翻译或简单总结。直接翻译会保留原书顺序，但不一定符合读者的理解路径；简单总结又容易丢掉代码、图表、API、表格和限制条件。

这个 skill 的目标是建立一套分层产物：先保留可追溯的原始解析层，再写面向读者的技术文章，最后用补丁、审计和读者问答反馈不断补齐理解缺口。

## 语言支持

支持三种输出语言模式：

- `zh`：中文技术文章和读者问答日志。
- `en`：英文技术文章和读者问答日志。
- `bilingual`：中英文双语输出，要求两种语言的解释、证据和覆盖范围保持一致。

语言选择顺序：

1. 用户明确指定时，使用用户指定语言。
2. 项目已有 `Output language:` 时，沿用项目设置。
3. 已有文章存在明显主语言时，沿用现有语言。
4. 否则根据当前对话语言推断。
5. 仍不明确时，AI 应先询问确认。

## 适用场景

- 把一本技术书或官方文档整理成中文、英文或双语课程/文章系统。
- 从 PDF 中抽取章节、图片、代码和表格，并保留审计依据。
- 将原书知识重新组织成工程问题驱动的文章，而不是逐段翻译。
- 检查文章是否遗漏关键 API、代码路径、图表或高密度参考内容。
- 回答读者对文章或原书内容的疑问，并把高价值问题反写回文章。
- 为后续 GitHub 仓库、课程材料或知识库沉淀一个可复用流程。

## 核心产物结构

```text
<Book Name>/
  pdf_to_markdown_plan.md          # 包含 Output language: zh | en | bilingual
  markdown_output/                 # 原书解析层，强调事实和可追溯
    README.md
    chapters/
    assets/images/
    work/
  course_materials/                # 面向读者的文章层
    00-course-plan.md              # 包含 Output language
    source_coverage_checklist.md
    source_coverage_audit.md
    validation_report.md
    reader_questions/              # 读者提问后才需要
      question-log.md
      backwrite-candidates.md
      applied-backwrites.md
    v1/ 或 v3/
      00-index.md
      01-module-name/
        01-article-name.md
```

核心原则是分层：

- `markdown_output/` 保存原书解析结果，方便追溯和审计。
- `course_materials/` 保存读者真正阅读的文章。
- reference patches 用于补齐 API、宏、枚举、表格、限制条件等密集内容。
- coverage audit 记录哪些内容覆盖充分，哪些内容弱覆盖、缺失或有意排除。
- reader Q&A feedback 把读者问题转化为文章改进线索。

## 工作流

1. 确定并记录 `Output language`。
2. 检查原始资料：PDF 页数、目录、图片、字体、代码块、OCR 风险和已有 Markdown。
3. 建立 `markdown_output/`，先保证事实层可追溯。
4. 写 `pdf_to_markdown_plan.md`，记录抽取工具、拆分策略、输出语言、风险和来源范围。
5. 规划文章模块，按读者理解路径组织，而不是照搬目录。
6. 按选定语言写技术文章：问题开场、模型解释、代码路径、判断表、来源覆盖补全区。
7. 做覆盖审计：章节、图片、代码、API/token、表格、高风险参考内容。
8. 对弱覆盖内容补 reference patches。
9. 对读者问题进行问答：先查本地材料，必要时参考网络并标注来源。
10. 经用户确认后，把高价值读者问题有机反写进文章。

## 读者问答反馈闭环

读者问题很重要，因为它说明文章某处可能没有讲透。这个 skill 不建议把“问题 + 答案”直接贴进文章，而是把问题背后的理解缺口改写成文章里的自然内容：

- 增加过渡段。
- 增加代码路径解释。
- 增加判断表。
- 增加误解说明。
- 增加 reference patch。

回答读者问题时，可以参考网络，但必须标注来源，并且要区分：

- 书内/项目证据：来自原书解析层、生成文章、补丁或审计。
- 网络补充：来自官方文档、标准、源码仓库、release notes 等外部来源。
- 推导解释：AI 根据证据做出的连接和解释。

## 仓库结构

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

## 安装方式

将仓库复制或软链接到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R book-to-technical-articles ~/.codex/skills/
```

之后可以显式调用：

```text
Use $book-to-technical-articles to convert this technical book into technical articles in the requested or inferred language, with source parsing, reference patches, coverage audit, and reader Q&A feedback.
```

## 常用脚本

```bash
scripts/inspect_pdf.py <book.pdf> --markdown
scripts/extract_pdf_images.py <book.pdf> <outdir> --manifest <json>
scripts/scan_markdown_stats.py <paths...> --markdown
scripts/qa_backwrite_log.py <project-root> --language zh --question "..." --answer-summary "..."
scripts/validate_book_materials.py <project-root> --scope project --language auto --markdown
scripts/validate_book_materials.py . --scope skill --markdown
scripts/token_coverage.py --source <source paths...> --target <article paths...> --markdown
```
