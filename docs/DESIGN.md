# 设计决策记录 — 抄了什么,避了什么

> 2026-09-02,基于对四个代表性开源项目的深度调研。
> 调研对象:career-ops(≈70k★)、Resume-Matcher(≈27k★)、
> resume-tailoring-skill(≈723★,Claude skill)、jobsync(自托管追踪器),
> 辅以 huntr/Teal(商业追踪器)和 The Interview Mentor / Liftoff(面试工具)。

## 抄了什么(精华)

| 来源 | 精华 | 落地位置 |
|---|---|---|
| career-ops | HITL 架构边界:AI 只产草稿,系统不代发送/提交/点击 | AGENTS.md §2 |
| career-ops | 事实完整性三件套:源文件只读、不在素材库不得声称、产出独立文件 | AGENTS.md §1, resume-tailor |
| career-ops | 状态机外置 YAML(canonical 状态 + 别名表),防止状态静默漂移 | applications/states.yml |
| career-ops | 红旗/骗局检测独立于匹配分(score-neutral),不污染总分 | jd-eval G 块 |
| career-ops | 评分必须引用证据(简历行 + JD 原文),拒绝黑盒分 | jd-eval, AGENTS.md §4 |
| career-ops | 数据契约:数据层与系统层分离,升级不碰数据 | AGENTS.md §3 |
| career-ops 作者教训 | **去重比打分值钱**:重复检测节省的时间超过任何打分优化 | jd-eval 第 0 步 |
| Resume-Matcher | injectable / non-injectable 关键词二分:不在 master 的绝不注入 | resume-tailor, jd-eval B 块 |
| Resume-Matcher | 交付前对齐校验:diff 产出与 master,自动剥离不可追溯内容 | resume-tailor 第 3 步 |
| Resume-Matcher | 整词匹配防子串误报、日期完整性检查等小技巧 | resume-tailor |
| resume-tailoring-skill | markdown 素材库 + 带 provenance 的结构化经验库(自改进循环) | profile/ 设计 |
| resume-tailoring-skill | 透明匹配档位(DIRECT/TRANSFERABLE/ADJACENT/GAP)+ <60% 不硬填 | resume-tailor |
| resume-tailoring-skill | reframing 带 before/after + 事实性理由 + 用户 Y/N 审批门 | resume-tailor, AGENTS.md |
| resume-tailoring-skill | 成功画像(success profile)作为 JD→简历的中间产物 | jd-eval B/E 块 |
| jobsync | JD 逐字保存(非摘要)+ description completeness 意识 | jds/README |
| jobsync | Interview 作为一等实体(独立目录,含面试官/轮次/复盘) | applications/interviews/ |
| jobsync/huntr/Teal | follow-up 的"下一步+日期"直接放申请行,不建独立任务系统 | tracker.md |
| huntr/Teal | 渠道字段 + 漏斗转化统计(内推 vs 海投差距是最高价值数据) | tracker skill |
| The Interview Mentor | 分阶段模拟(暖场→核心→深挖→收尾)+ 评分卡 rubric | interview-prep |
| The Interview Mentor | 四级提示阶梯(方向→方法→部分解→完整解),学习在挣扎处 | interview-prep |
| STAR 最佳实践 | 8~12 母题按 archetype 组织(非按问题),组件分离,实战记录回填 | profile/star-bank.md |

## 避了什么(糟粕)

| 来源 | 糟粕 | 为什么避 |
|---|---|---|
| career-ops | 模式数量失控(14→37 个模式 × 20 语言) | 单人工具的维护噩梦;4 个 skill 覆盖核心闭环 |
| career-ops | Go TUI 仪表盘 + Web UI | markdown 表格本身就是够用的 UI |
| career-ops | batch 并行架构(conductor + 8 worker + lock file) | 单用户求职用不上;分布式复杂度搬进个人脚本是负资产 |
| career-ops | 9 个 CLI 的 wrapper 层 | 测试矩阵爆炸,同一 skill 表现漂移;依赖 AGENTS.md 约定即可 |
| career-ops(批评文章) | 基于个人画像的静态关键词过滤 | 会静默过滤掉合格职位("差点毁掉我的求职");我们只用红线列表且显式可见 |
| career-ops | 纯 LLM 整体打分、版本间 rubric 漂移 | 打分附维度理由 + 证据引用,弱化精确性承诺 |
| Resume-Matcher | 纯词法打分(无同义/词干/短语,等权) | "manage"≠"management",分数误导;改用透明档位标签 |
| Resume-Matcher | 黑盒 ATS 分数 + README 不写方法论 | 分数必须可审计、方法论写在 skill 里 |
| Resume-Matcher | LLM 当解析器的脆弱管线(重试+日期修复 hack,issue #621) | 素材库直接以 markdown 人工维护,不做 PDF→结构化解析 |
| Resume-Matcher | 双 app 重架构(Next.js + FastAPI + Docker) | 个人工具用 markdown + git 达到同样效果 |
| Resume-Matcher(#571) | 好看但 ATS 读不出的模板 | 产出强制单栏标准结构;PDF 生成后做文本提取验证 |
| jobsync | Activity 时间追踪(含休息/活动类型) | 过度工程,没人坚持用 |
| jobsync | 把跟进塞进独立 Task 模型 | 跟进是申请的属性,分家即死表 |
| 商业工具共识 | AI 代写简历 bullet | 用户实测"华而不实";AI 做批评者/组织者,不做代笔人 |
| liftoff 等 | 静态题库式面试准备 | 从本人素材+目标 JD 生成,个人化才有价值 |

## 我们自己的增量设计

1. **岗位族(job family)作为简历版本单位**:用户原始洞察,落地为
   config.yml 的 job_families + resumes/by-family/。核心要求重叠 ≥70%
   才共用一版,避免版本爆炸与针对性丢失两个极端。
2. **面试深挖 = 简历事实性的压力测试**:interview-prep 对每条 bullet
   做"面试官会怎么挖"自审,与 resume-tailor 的事实完整性规则闭环。
3. **复盘回写环**:模拟面试暴露的薄弱点、真实面试被问住的问题,
   回填素材卡与 star-bank——系统随每次面试变强。
4. **会话开场静默扫描到期跟进**:利用 agent 无需界面交互的优势,
   把"提醒"变成零成本动作(商业工具要靠推送通知,我们靠会话入口)。

## 未纳入(有意)

- 自动投递/表单填写:封号与信誉风险(招聘方对 AI 海投反弹明显),且国内
  渠道(Boss直聘/内推)是对话式流程,自动化价值低。保持人工投递。
- 公司 career page 扫描爬虫(career-ops scan / jobsync crawler):
  维护成本高,国内渠道不适用。需要时手动收集 JD 即可。
- 求职信 cover letter 独立 skill:并入 resume-tailor 产出可选项,
  国内场景使用率低。

## 追加(2026-09-02 demo 后):简历样式层的实现决策

- **路线**:markdown(事实源)→ HTML/CSS 模板(呈现)→ 无头 Edge/Chrome 渲染 PDF。
  这是 career-ops 验证过的路线,不引入任何应用代码,渲染是两条 shell 命令。
- **模板约束**(吸收 Resume-Matcher issue #571 教训):单栏、语义标签、
  无表格/文本框/图标、系统字体;颜色仅用于节标题,正文保持可解析纯文本。
- **验证闭环**:PyMuPDF 检查页数与文本提取 + pandoc docx 回环 + 视觉验收。
  模板好不好以"解析回环能提取关键字段"为准,不以好看为准。
- docx 仅按需生成(部分国内网申要求 Word 格式);内推/邮件投递默认 PDF。

## 追加(2026-09-02):样式升级机制 —— 模板变体 + 设计变量

- v1 经典版(下划线节标题)→ v2 现代版(大姓名区/tagline/左侧色条/日期右对齐)。
  同一套 {{TOKEN}},换模板零成本;两版都通过"提取回环 + 视觉验收"双门槛。
- 更优样式不靠每次手改 CSS,靠三层杠杆,从便宜到贵:
  ① :root 设计变量(--accent 主色/--fs 字号/--lh 行距/--sec-gap 节间距)→ 秒级换风格
  ② 版面填充率量化(最后文本块底部/页高,目标 80%~95%)→ 用数据决定是否调参
  ③ 新建模板变体(如英文版/双栏头版)→ 必须重新过提取+视觉双验证
- 日期右对齐用 float 实现:不改文本流顺序,解析顺序仍是"公司|职位|日期",ATS 安全。

## 追加(2026-09-02):主流简历设计调研 → v3 模板

调研范围:Novoresume/Zety/Microsoft Word 官方指南、Yale OCS、ResumeOptimizerPro、
Nelson Connects(欧美);超级简历 WonderCV/五百丁/锤子简历/Canva(国内)。

### 主流设计规律(欧美与国内共识)

1. **单栏 + 逆时序**是绝对主流,ATS 场景下无争议;国内平台模板亦绝大多数单栏。
2. **节标题必须与正文强视觉区隔**:主流手法是"标题 + 全宽分隔线"或色块条;
   超级简历/五百丁模板几乎清一色全宽线。→ v2 左色条被用户否("不规整")与此吻合,
   v3 回归全宽线并保留 v2 其余优点。
3. **标准节名**(工作经历/项目经历/技能/教育经历)优于创意命名,利于 ATS 与 HR 扫读。
4. **字号梯度**:正文 10.5~12pt,节标题更大/加粗;全库只用一到两种字体。
5. **日期格式全库一致**,右对齐是常见高阶手法(扫读时间线)。
6. **边距 0.5~1 inch,行距 1.0~1.15(英文);中文模板行距常在 1.3~1.5**。
7. **单一主色**只用于标题与线条,正文保持黑/深灰;避免多色。
8. **规避项共识**:表格/文本框/图形/照片(除非确定无 ATS);
   国内"风格化模板"(锤子/五百丁个性化款)适合设计岗,技术岗仍以简洁规整为主。

### v3「主流规整版」= v1 的全宽分隔线 + v2 的优点

- 恢复节标题全宽分隔线(细线 1pt,--rule 色),标题保留主色加粗字距
- 保留:大姓名区 + tagline + 主色粗线收尾、日期右对齐、技能行分类加粗、
  设计变量集中 :root、填充率指标(实测 90%,验收 pass 零 issue)
- v3 成为默认模板;v1/v2 保留为备选(同一套 TOKEN,切换零成本)

来源:novoresume.com/career-blog/resume-fonts · zety.com/blog/ats-resume ·
word.cloud.microsoft/create/en/blog/best-resume-fonts ·
ocs.yale.edu/resources/resume-formatting ·
nelsonconnects.com/learning-center/the-six-best-modern-resume-template-resources ·
wondercv.com · 500d.me · zhihu.com/p/506079500

## 追加(2026-09-02):内容质量体系 + 多领域策略 + 样式自定义

### 调研结论(信源分级见 docs/RESUME-CONTENT-GUIDE.md)

1. **内容质量有权威标准,已采纳为门禁**:Google XYZ 公式(Laszlo Bock,官方)、
   HBS PAR 结构与动作动词表(高校官方)、MIT/Yale 职业服务格式规范。
   商业博客(Novoresume/Zety)只作交叉验证不单独采信。
2. **分领域:确有必要,实现为策略包而非系统分叉**。差异实质:量化对象不同
   (金融=钱/工程=技术效率/HR=人效)、模块权重不同(工程必有技能区、
   金融教育前置且一页铁律+黑白、HR 职能广度+证书)、语言风格不同。
   共性(事实完整性/XYZ/对齐校验)不分领域。
3. **校招 vs 社招:确有必要**。校招=教育前置第一屏+潜力信号+实习/课程项目补位;
   社招=工作经历前置+量化业绩为王。来自 Moka/牛客/超级简历等国内招聘实践信源。

### 样式自定义设计(schema 驱动,不写渲染引擎)

- `templates/style.yml` 是唯一样式入口:template/colors/header.align/
  sections(顺序+增删)/dates.align/density/page/language
- 实现机制:agent 填充 HTML 时按 schema 组装——模块顺序=块顺序、
  居中=header class、配色/密度=:root CSS 变量、删模块=不填该块。
  零代码引擎,三套模板通用。
- 已实测:自然语言 4 项要求(青色/居中/模块重排/加密)
  → 一次渲染全部生效,提取回环 OK,视觉验收 pass(customization 4/4)。
- 冲突规则:策略包强制样式(金融黑白)> 用户样式偏好,生成时显式提示。

## 追加(2026-09-02):按 skill-creator 规范收敛为单一技能

- 4 个独立 skill(jd-eval/resume-tailor/interview-prep/tracker)收敛为
  **1 个 `job-finding` 技能**:`SKILL.md` 只留触发描述、核心原则与路由表
  (66 行),工作流细节全部移入 `references/` 按需加载(progressive disclosure)。
- 收敛动机:描述即触发信号,4 个技能对"简历/面试/投递"类话术会互相竞争触发;
  单入口 + 内部路由消除歧义,规则更新只动一个目录。
- references/ 中的文档已剥离独立技能时期的 frontmatter,标注"由 SKILL.md 按需加载"。

## 追加(2026-09-02):补充 scripts 层 — 判断与机制的分工

用户质疑"纯 markdown skill 太简单"。分析判据:脚本承载确定性机制,
prompt 承载判断力(skill-creator:"每次测试都重复手写的辅助脚本应固化进 scripts/")。
demo 期间确实反复手写三类确定性步骤,固化为:

- scripts/render_pdf.py — 浏览器探测(跨平台)+ 渲染 + 页数/关键词提取/填充率验证,
  exit code 即交付门禁
- scripts/check_tracker.py — tracker 状态机/日期/引用校验 + 到期扫描 + 渠道漏斗
  (首次运行即抓到 tracker 引用路径缩写的真实数据 bug,验证了价值)
- scripts/check_facts.py — 事实追溯预检(双侧空白归一化匹配),负向测试通过
  (编造数字被拦截);明确定位为启发式第一道网,语义校验仍归 LLM 流程

不脚本化的部分及理由:评分/选材/改写/STAR 映射是判断型工作;
HTML 按 style.yml 组装需要灵活性,脚本化会退回固定模板。
AGENTS.md 反过度工程条款相应澄清:机制型脚本在"被重复手写"时应该固化。
