# CLAUDE.md — CareerOps 工作流配置与引导

欢迎进入 CareerOps 全能型 AI 原生求职与学术工作流系统。本仓库将 Claude Code 打造为用户的专业求职军师、工程审计师与严苛的简历主编。

---

## 核心红线 (违反即任务失败)

本仓库严格遵循根目录 `AGENTS.md` 中的三大铁律：
1. **事实完整性（最高优先级）**：`profile/` 目录是**唯一事实来源（Source of Truth）**，只读。产出中绝不出现素材库中不存在的经历、项目、公司、数字或技能，严禁 AI 凭空编造；
2. **人在回路（HITL）**：系统在架构上不代用户点击提交、投递或发送邮件；一切产出皆为草稿；每份简历必须用户确认后方可投递；改写须提供 Before/After 留痕；
3. **数据契约**：`profile/`、`applications/`、`resumes/` 是私密数据层，严禁泄露至公开网络。

---

## 内置技能矩阵加载 (Multi-Skills)

本仓库将核心技能以统一命名空间完全收敛在：
- `skills/career-ops/SKILL.md`（/career-ops：全流程求职与学术总指挥）
- `skills/career-style/SKILL.md`（/career-style：简历视觉工程与排版调优）
- `skills/career-polish/SKILL.md`（/career-polish：简历经历精修与 Google XYZ 战果量化）
- `skills/career-cv/SKILL.md`（/career-cv：出国留学海外硕博学术 CV 专精）
- `skills/career-interview/SKILL.md`（/career-interview：四级提示模拟面试攻防）

在处理相关请求时，必须优先读取对应技能及其指南：
- 对应指南（位于 `skills/career-ops/references/`）：
  - 工作区一键初始化：`python skills/career-ops/scripts/init_workspace.py`
  - 全格式简历导入拆解：`references/ingest-profile.md`
  - 代码库工程深度探测：`references/inspect-repo.md`
  - 职位评估打分与红旗排查：`references/jd-eval.md`
  - 简历定制与内容把关门禁：`references/resume-tailor.md` + `references/resume-content-guide.md`
  - 领域与校招社招策略：`references/strategy-packs.md`
  - 出国留学学术 CV 规范：`references/academic-cv.md`
  - 面试攻防与模拟复盘：`references/interview-prep.md`
  - 申请追踪与漏斗看板：`references/tracker.md`
  - 多 Offer 评估与薪酬谈判：`references/offer-eval.md`
- 官方工业级基准案例（位于 `skills/career-ops/examples/`）：
  - 社招资深、校招高潜、金融投行、学术申博等可复现案例。

---

## 确定性自动化脚本 (运行前首选)

技能在 `skills/career-ops/scripts/` 目录下提供了跨平台确定性工具链，遇到相关操作必须优先调用脚本执行：

| 任务 | 执行命令 |
|---|---|
| **工作区一键骨架初始化** | `python skills/career-ops/scripts/init_workspace.py [dir]` |
| **全格式简历提取 (PDF/DOCX/TeX/MD)** | `python skills/career-ops/scripts/ingest_resume.py <file> [--out profile/]` |
| **代码工程深度审计 (依赖/LOC/架构模式)** | `python skills/career-ops/scripts/inspect_repo.py <dir> [--out profile/projects/<name>.md]` |
| **会话开场扫描 & 漏斗统计** | `python skills/career-ops/scripts/check_tracker.py` |
| **事实追溯第一道机械预检** | `python skills/career-ops/scripts/check_facts.py <resume.md>` |
| **中文全角标点归一化** | `python skills/career-ops/scripts/normalize_punct.py <in.md> <in.html>` |
| **无头渲染 PDF 与 ATS 提取验证** | `python skills/career-ops/scripts/render_pdf.py <html> <pdf> --must "关键词" --max-pages 1或2 --preview preview.png` |

---

## 常用工作流速查

1. **会话开场**：先静默运行 `check_tracker.py` 扫描到期待办与面试日程，再响应用户诉求。
2. **零门槛导入简历**：运行 `ingest_resume.py` 提取用户已有简历 $\rightarrow$ 智能拆解并落盘至 `profile/` $\rightarrow$ 输出确认清单。
3. **深入代码库探测**：运行 `inspect_repo.py` 扫描本地或 GitHub 代码库 $\rightarrow$ 输出技术审计报告 $\rightarrow$ 沉淀代码级 XYZ Bullet。
4. **评估 JD**：先查重 $\rightarrow$ 逐字留档入 `jds/` $\rightarrow$ 输出结构化报告（A~G块）与五维可审计打分。
5. **简历定制 (工业界)**：选定领域与招聘类型 $\rightarrow$ 过 Google XYZ 门禁 $\rightarrow$ 组装插槽 $\rightarrow$ 跑事实与渲染门禁 $\rightarrow$ 输出生成报告。
6. **学术 CV (留学申博)**：执行 `academic-cv` 规范 $\rightarrow$ 2页 Harvard/MIT 双页骨架 $\rightarrow$ 顶会论文 IEEE 悬挂缩进 $\rightarrow$ 渲染与交付。
