# 简历定制

> 本文件是 job-finding 技能的参考文档,由 SKILL.md 按需加载;路径均相对仓库根。

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
- 按本技能 `references/strategy-packs.md` 应用对应策略包(先读它):
  模块取舍、排序、量化对象、篇幅、语言风格。
- 未收录领域按 generic-business 起步并告知用户,邀请其补充领域要求。

### 2. 准备
读 `config.yml`(目标、红线、岗位族)、相关 JD 评估报告(没有就先跑 jd-eval)、
`profile/` 全部相关素材卡、该族现有版本(如有)、**技能目录下** `templates/style.yml`(样式)。

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
- **素材过薄时**(如应届只有一段实习):填充率让位于事实完整性——
  绝不为凑版面夸大或硬凑 bullet,宁可页尾留白,skill 会如实报告填充率。
- header 的 tagline(岗位定位行)属于 header 不属于概述模块:
  用户"去掉概述"时 tagline 仍保留(它承担岗位定位职能)。

### 4. 样式(用户可自定义,不限于固定模板)

读**技能目录下** `templates/style.yml`。用户可直接用自然语言要求,映射到 schema:
- "换个青色/绿色" → colors.accent
- "标题居中" → header.align: center
- "去掉项目经历 / 概述不要" → sections 删行
- "技能放到项目前面 / 教育放最后" → sections 排序
- "紧凑点/松一点" → density: compact|regular|airy
- "日期跟在标题后面" → dates.align: inline
冲突处理:策略包有强制样式的(如金融=黑白单页)优先,并告知用户冲突。
用户的临时要求可不回写 style.yml;明确说"以后都这样"才回写。
用户给的颜色只有色名(如"深绿色")时,自选一个稳妥色值并在报告中标注"可换"。
没有独立模板可选时,在 v3 骨架上按 schema 调整即可,不必新建模板文件。

### 5. 对齐校验(交付前必做)
逐条 diff 产出与 `profile/` 素材:
- 不可追溯的技能/公司/数字 → 删除并报告
- 时态/月份丢失等常见解析损伤 → 检查
- 报告 injectable 关键词覆盖率与 non-injectable gap 清单
- 先跑 `<技能目录>/scripts/check_facts.py <产出.md>`(确定性预检,数字/日期出处;
  脚本自动剥除 HTML 注释元数据),再做语义级核对
- XYZ 抽查:随机 3 条 bullet 检查动词开头/量化/结果

### 6. 产出(写入 `resumes/`)
- `resumes/by-family/<族>.md` — 族基础版(源文件,markdown)
- `resumes/by-family/<族>--<公司>.md` — 若有微调,存微调版
- `resumes/reports/<公司>-<岗位>-report.md` — 生成报告:策略(域/类型)、
  选材理由、改写清单、gap 清单、bullet 质量抽查结果、简历版本号
- **样式输出管线**(用户要 PDF/DOCX 时;markdown 永远是事实源):
  1. 复制**技能目录** `templates/` 所选模板到 `resumes/by-family/<版本>.html`,
     按 style.yml 填充:模块按 sections 顺序组装、header 按 align 加样式、
     colors/density 写入 :root CSS 变量
  2. `<技能目录>/scripts/normalize_punct.py <产出.md> <产出.html>`
     (全角标点归一化,幂等)
  3. `<技能目录>/scripts/render_pdf.py <html> <pdf> --must "姓名,手机尾号,核心数字" --max-pages <策略包篇幅> --preview <预览.png>`
     一条命令完成渲染+验证+预览;exit 1 必须修复后重跑
  4. 样式实质变更(新模板/换色/换布局)时看一眼 PNG 做视觉检查;
     同款样式复用可跳过
  5. 需要可编辑版时用 pandoc 转 docx 并回环验证

### 7. 收尾
更新 `applications/tracker.md` 对应行:简历版本列、状态 ready、
下一步"待用户确认投递"。