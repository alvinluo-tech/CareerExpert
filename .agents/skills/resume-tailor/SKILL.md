---
name: resume-tailor
description: 基于素材事实库为特定 JD 或岗位族生成定制简历,严格保证事实完整性。当用户要求"定制简历/生成简历/更新简历版本"时使用。依赖 jd-eval 的评估结果或用户直接给的 JD。
---

# 简历定制

## 核心原则(违反即失败)

1. `profile/` 是唯一事实来源,**只读**。产出中任何经历、数字、技能、时间
   必须能追溯到具体素材卡/master-resume。
2. 关键词二分:injectable 才能进简历;non-injectable 三选一(留空 /
   求职信解释 / 提示用户补素材),绝不编造。
3. 一切措辞改写(reframing)先展示 before/after + 一句事实性理由,
   用户 Y/N 确认后才落稿。批量改写时汇总展示,但用户有权整批否决。
4. `profile/master-resume.md` 永不被覆写;产出只写 `resumes/`。

## 分组策略(岗位族 = 简历版本单位)

先查 `config.yml` 的 job_families:
- JD 属于现有族 → **在族版本基础上微调**(关键词措辞、bullet 排序、
  侧重点),不整版重写。微调项逐条列出。
- JD 不属于任何现有族 → 先问用户:新建族,还是归入相近族?
  盲目每 JD 一版会导致版本爆炸;盲目共用一版会丢失针对性。
  判断依据:两个 JD 的核心要求重叠 ≥70% 才值得共用一版。

## 流程

### 1. 准备
读 `config.yml`(目标、红线)、相关 JD 评估报告(没有就先跑 jd-eval)、
`profile/` 全部相关素材卡、该族现有版本(如有)。

### 2. 组装
- 选材:top 3~4 相关项目/经历,按该 JD 相关性排序(相关性理由写进报告)。
- 每条 bullet 对照 JD 打匹配档位:
  DIRECT(90+)/TRANSFERABLE(75+)/ADJACENT(60+)/GAP(标记,不硬填)。
  档位是透明标签不是黑盒分数,允许不精确,不允许假装精确。
- 保留 ATS 安全结构:单栏、标准节标题、无表格/图标/文本框。

### 3. 对齐校验(交付前必做)
逐条 diff 产出与 `profile/` 素材:
- 不可追溯的技能/公司/数字 → 删除并报告
- 时态/月份丢失等常见解析损伤 → 检查
- 报告 injectable 关键词覆盖率与 non-injectable gap 清单

### 4. 产出(写入 `resumes/`)
- `resumes/by-family/<族>.md` — 族基础版(源文件,markdown)
- `resumes/by-family/<族>--<公司>.md` — 若有微调,存微调版
- `resumes/reports/<公司>-<岗位>-report.md` — 生成报告:选材理由、
  改写清单(含已确认的 reframings)、gap 清单、简历版本号(回填 tracker)
- PDF/DOCX 只在用户要求时生成(用 document skills),生成后提醒用户
  目测排版 + 用文本提取验证可解析性(防"好看但 ATS 读不出")

### 5. 收尾
更新 `applications/tracker.md` 对应行:简历版本列、状态 ready、
下一步"待用户确认投递"。
