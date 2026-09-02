---
name: job-finding
description: 求职全流程工作流:JD 评估打分、按岗位族定制简历(内容质量门禁 + 领域策略包 + 样式自定义)、面试准备与模拟、申请追踪与渠道漏斗。凡是用户提供职位 JD、要求评估岗位值不值得投、定制或修改简历、调整简历样式配色、准备面试、模拟面试、记录投递、查看求职进度、统计面试转化,或在一个 job_finding 求职仓库里发起任何相关请求时都应使用本技能——即使用户没有明确说"求职"两个字。
---

# job-finding — AI 原生求职工作流

把 AI CLI 变成求职流水线:**AI 分析与组织,用户决策与投递**。
本技能运行在一个"求职仓库"里(数据层:profile 素材库 / jds / resumes /
applications;系统层:本技能与 docs)。先看仓库是否已初始化(见下),
再按用户意图路由到对应工作流。

## 第 0 步:确认仓库就绪

检查仓库根是否有 `profile/`、`jds/`、`applications/`、`config.yml`。
**分发契约**:本技能自带完整系统层(templates/ 与 scripts/ 都在技能目录内,
含 style.yml 样式入口),仓库里只放数据层。数据层缺失时按以下骨架创建
(空目录 + 一行用途说明的 README),并提示用户先填充 `profile/master-resume.md`
与项目卡——素材库是唯一事实来源:

```
profile/            master-resume.md(主简历)+ projects/(项目卡)+ work/(经历卡)+ star-bank.md
jds/                JD 逐字存档,文件名 YYYY-MM-DD-<公司>-<岗位>.md + evaluations/(评估报告)
resumes/            by-family/(岗位族版本)+ reports/(生成报告)
applications/       tracker.md(追踪表)+ interviews/ + reports/
                    states.yml(状态机):首次创建时从本技能 templates/states.yml 复制
config.yml          岗位族/红线/跟进节奏/渠道
```
仓库根若有 `AGENTS.md`,它的规则(事实完整性、HITL、数据契约)优先级最高。

## 核心原则(所有工作流通用,违者即失败)

1. **事实完整性**:`profile/` 只读;产出中不得出现素材库中不存在的
   经历/数字/技能;JD 关键词二分 injectable / non-injectable,后者绝不编造。
2. **人在回路**:一切产出是草稿;不代用户发送/提交/投递;每份简历投出前
   必须用户确认。用户离线但明确预授权("直接出一版")时:落稿为草稿、
   before/after 改写全量留痕于生成报告并标注"待追认"、状态停在 ready;
   绝不因预授权而代投或越过事实完整性。
3. **可审计**:评分必须引用证据(简历行 + JD 原文);红旗独立于匹配分,
   永不掺入总分。
4. **反过度工程**:能用 markdown + 现有模板解决的,不写代码不加脚本。

## 会话开场动作

用户在本仓库发起任何求职相关对话时,先静默执行 tracker 工作流的
"到期项扫描"(follow-up 提醒、面试日程),再响应用户请求。

## 工作流路由

| 用户意图(示例话术) | 工作流 | 先读 |
|---|---|---|
| "评估这个 JD / 值不值得投" + 贴出职位描述 | jd-eval | references/jd-eval.md |
| "定制简历 / 更新简历版本 / 生成简历" | resume-tailor | references/resume-tailor.md |
| "换个颜色 / 居中 / 去掉某模块 / 校招版" | resume-tailor(样式节) | references/resume-tailor.md + references/strategy-packs.md |
| "准备 XX 公司面试 / 模拟面试" | interview-prep | references/interview-prep.md |
| "记录一下 / 更新状态 / 看进度 / 该跟进谁 / 统计转化" | tracker | references/tracker.md |

一个请求常跨工作流(如"评估这个 JD,合适就出简历"):按顺序串联,
每步产物落盘后再进下一步。

## 各工作流一句话约束

- **jd-eval**:先去重(最值钱的一步),JD 逐字存档,五维评分必须引用证据,
  红旗单列;投不投永远用户决定。
- **resume-tailor**:先定策略(domain × recruiting_type,见 strategy-packs),
  每条 bullet 过 XYZ 门禁,岗位族决定版本(重叠 ≥70% 共用一版),
  样式按 `templates/style.yml` schema 由用户自然语言驱动,
  交付前对齐校验 + PDF 提取回环验证(命令见模板头注释)。
- **interview-prep**:故事映射不新编;模拟面试用四级提示阶梯;
  结束必给评分卡;薄弱点回填素材库——每次面试让系统变强。
- **tracker**:状态词只能用 `applications/states.yml` 的 canonical 值;
  每行必须有"下一步";渠道漏斗是唯一必做统计;
  跟进草稿永远标注"请确认后自行发送"。

## 确定性脚本(scripts/,判断交给模型,机制交给脚本)

以下步骤**必须用脚本**而不是手写临时命令——它们是精确性要求高、
每次手写都会重新发明轮子的确定性检查。脚本都在**技能目录的 scripts/ 下**
(对任意求职仓库可用;脚本自动向上定位仓库根):

- `<技能目录>/scripts/render_pdf.py <html> <pdf> --must "关键词,..." --max-pages 1 --preview 预览.png`
  → 渲染 PDF + 页数/关键词提取/填充率验证 + 视觉检查用 PNG,exit 1 不达标不交付
- `<技能目录>/scripts/check_tracker.py` → tracker 校验 + 到期扫描 + 渠道漏斗
  + 投递节奏(会话开场扫描和一切统计请求都跑它;空表是合法 WARN 不是 FAIL)
- `<技能目录>/scripts/check_facts.py <resume.md>` → 事实追溯预检(自动剥除
  HTML 注释元数据);启发式第一道网,语义级对齐校验仍须 LLM 流程
- `<技能目录>/scripts/normalize_punct.py <产出.md> <产出.html>` → 中文全角标点
  归一化(渲染前必跑,幂等)
- docx 导出仍用 pandoc(低频,不设脚本)
