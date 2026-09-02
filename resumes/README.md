# resumes/ — 简历版本库

> 由 resume-tailor skill 生成;生成前必须通过对齐校验(skill 第 3 步)。

## 组织方式:按岗位族,不按单个 JD

- `by-family/<族>.md` — 该族的基础版本(源文件,markdown)
- `by-family/<族>--<公司>.md` — 仅当对某公司有实质微调时才另存
- `reports/<公司>-<岗位>-report.md` — 每次生成的报告:选材理由、
  改写清单、gap 清单

## 为什么不每个 JD 一版

版本爆炸是定制简历的第一杀手(Reddit 上 "100+ applications is actual hell"
的根源)。核心要求重叠 ≥70% 的 JD 共用一版,族内微调逐条列出、可回滚。
