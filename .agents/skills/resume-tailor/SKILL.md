---
name: resume-tailor
description: 基于素材事实库为特定 JD 或岗位族生成定制简历,含内容质量门禁、领域/招聘类型策略包与可自定义样式。当用户要求"定制简历/生成简历/更新简历版本/改简历样式"时使用。依赖 jd-eval 的评估结果或用户直接给的 JD。
---

# 简历定制

## 核心原则(违反即失败)

1. `profile/` 是唯一事实来源,**只读**。产出中任何经历、数字、技能、时间
   必须能追溯到具体素材卡/master-resume。
2. 关键词二分:injectable 才能进简历;non-injectable 三选一(留空 /
   求职信解释 / 提示用户补素材),绝不编造。
3. 一切措辞改写(reframing)先展示 before/after + 一句事实性理由,
   用户 Y/N 确认后才落稿。
4. `profile/master-resume.md` 永不被覆写;产出只写 `resumes/`。

## 流程

### 1. 确定策略(生成前必做)

确定 `domain`(领域)与 `recruiting_type`(campus/social/internship):
- 从 JD 明显可推断的直接采用并告知用户;推断不了就问一句,
  同时给出默认建议(如"看 JD 像社招技术岗,按 social + tech-engineering 处理?")。
- 按 `.agents/skills/resume-tailor/strategy-packs.md` 应用对应策略包:
  模块取舍、排序、量化对象、篇幅、语言风格。
- 未收录领域按 generic-business 起步并告知用户,邀请其补充领域要求。

### 2. 准备
读 `config.yml`(目标、红线、岗位族)、相关 JD 评估报告(没有就先跑 jd-eval)、
`profile/` 全部相关素材卡、该族现有版本(如有)、`templates/style.yml`(样式)。

### 3. 组装(内容质量门禁)

- 选材:top 3~4 相关项目/经历,按 JD 相关性排序(理由写进报告)。
- **每条 bullet 过 XYZ 检查**(依据 docs/RESUME-CONTENT-GUIDE.md,信源 Google/HBS):
  强动作动词开头 + 职责范围 + 量化结果;无数字时用规模/范围量化。
  未通过的 bullet 要么改写(走 reframing 审批),要么降权排后。
- **反模式扫描**:职责型语句("负责…")、弱开头("参与/协助"单独开头)、
  空话形容词、无结果动作 —— 发现即改写或删除。
- 关键词:injectable 覆盖 JD 核心词(具体工具/语言/方法论名显性出现);
  non-injectable 不硬填,进 gap 清单。
- 每条 bullet 对照 JD 打匹配档位:DIRECT/TRANSFERABLE/ADJACENT/GAP
  (透明标签,GAP 标记不硬填)。
- 篇幅按策略包(领域×招聘类型)控制;ATS 安全结构:单栏、标准节名、
  无表格/图标/文本框。

### 4. 样式(用户可自定义,不限于固定模板)

读 `templates/style.yml`。用户可直接用自然语言要求,映射到 schema:
- "换个青色/绿色" → colors.accent
- "标题居中" → header.align: center
- "去掉项目经历 / 概述不要" → sections 删行
- "技能放到项目前面 / 教育放最后" → sections 排序
- "紧凑点/松一点" → density: compact|regular|airy
- "日期跟在标题后面" → dates.align: inline
冲突处理:策略包有强制样式的(如金融=黑白单页)优先,并告知用户冲突。
用户的临时要求可不回写 style.yml;明确说"以后都这样"才回写。
没有独立模板可选时,在 v3 骨架上按 schema 调整即可,不必新建模板文件。

### 5. 对齐校验(交付前必做)
逐条 diff 产出与 `profile/` 素材:
- 不可追溯的技能/公司/数字 → 删除并报告
- 时态/月份丢失等常见解析损伤 → 检查
- 报告 injectable 关键词覆盖率与 non-injectable gap 清单
- XYZ 抽查:随机 3 条 bullet 检查动词开头/量化/结果

### 6. 产出(写入 `resumes/`)
- `resumes/by-family/<族>.md` — 族基础版(源文件,markdown)
- `resumes/by-family/<族>--<公司>.md` — 若有微调,存微调版
- `resumes/reports/<公司>-<岗位>-report.md` — 生成报告:策略(域/类型)、
  选材理由、改写清单、gap 清单、bullet 质量抽查结果、简历版本号
- **样式输出管线**(用户要 PDF/DOCX 时;markdown 永远是事实源):
  1. 复制所选模板到 `resumes/by-family/<版本>.html`,按 style.yml 填充:
     模块按 sections 顺序组装、header 按 align 加样式、
     colors/density 写入 :root CSS 变量
  2. 无头渲染 PDF(命令见模板文件头注释,Edge/Chrome 均可)
  3. 验证(必做):PyMuPDF 检查页数(≤策略包篇幅)、姓名/联系方式/量化数字
     可提取;版面填充率 80%~95%(偏低调 density);首次用模板渲染 PNG 视觉检查
  4. 需要可编辑版时用 pandoc 转 docx 并回环验证
  5. 中文排版:CJK 之间用全角标点

### 7. 收尾
更新 `applications/tracker.md` 对应行:简历版本列、状态 ready、
下一步"待用户确认投递"。
