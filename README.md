# job_finding — AI 原生求职工作流

不做应用,不写代码。整个系统 = **这个 git 仓库(数据层)+ 4 个 skills(规则层)**,
由任意 AI 编程 CLI(ZCode / Claude Code / …)驱动运行。

设计来源:对 [career-ops](https://github.com/santifer/career-ops)、
[Resume-Matcher](https://github.com/srbhr/resume-matcher)、
[resume-tailoring-skill](https://github.com/varunr89/resume-tailoring-skill)、
[jobsync](https://github.com/Gsync/jobsync) 等开源项目"取其精华、去其糟粕"的
深度分析,决策记录见 `docs/DESIGN.md`。

## 目录结构

```
job_finding/
├── AGENTS.md            # agent 操作规范(最重要,所有 agent 必读)
├── config.yml           # 个人配置:岗位族、红线、跟进节奏(隐私,不入库)
├── .agents/skills/job-finding/    # 唯一技能:SKILL.md 路由 + references/ 按需加载
│   ├── SKILL.md                   #   触发描述、核心原则、工作流路由
│   └── references/                #   jd-eval / resume-tailor / interview-prep
│                                   #   / tracker / strategy-packs
├── profile/             # 素材事实库(唯一事实来源,只读原则)
│   ├── master-resume.md       # 主简历(从现有简历迁移)
│   ├── projects/              # 项目卡,一项目一文件
│   ├── work/                  # 工作经历卡
│   └── star-bank.md           # STAR 故事库(8~12 个母题)
├── templates/
│   └── resume-template.html   # ATS 安全简历样式模板(单栏,Edge/Chrome 渲染 PDF)
├── jds/                 # JD 逐字原文 + evaluations/ 评估报告
├── resumes/             # 按岗位族组织的简历版本 + 生成报告
├── applications/
│   ├── tracker.md       # 申请追踪表(单一事实源)
│   ├── states.yml       # 状态机定义
│   ├── interviews/      # 面试准备文档与复盘
│   └── reports/         # 周报:到期跟进扫描 + 渠道漏斗统计
└── docs/DESIGN.md       # 设计决策:抄了什么,避了什么
```

## 1 个 skill,4 个工作流

`job-finding` 是唯一技能入口(agent 按用户意图自动触发),内部路由到 4 个工作流:

| 工作流 | 触发场景 | 一句话职责 |
|---|---|---|
| jd-eval | 丢一段 JD 过来 | 去重 → 评估打分(证据可审计)→ 决定投递策略 |
| resume-tailor | 定制/更新简历/改样式 | 策略包选材、XYZ 内容门禁、岗位族共用版本、样式自定义 |
| interview-prep | 准备/模拟面试 | JD→故事映射、模拟面试官深挖、评分卡、复盘回写 |
| tracker | 记录/看进度 | 到期跟进提醒、状态机维护、渠道漏斗统计 |

## 典型工作流

```
收集 JD → jd-eval(存档+评估+打分)
        → resume-tailor(按岗位族定制,人工确认)
        → [人工投递] → tracker(记录)
        → 收到面试 → interview-prep(准备→模拟→复盘回写素材库)
        → 结果 → tracker(复盘归因) → 漏斗统计调整策略
```

## 开始使用(首次填充)

1. 把现有简历内容迁入 `profile/master-resume.md`(不分岗位的完整版)
2. 按 `profile/projects/_template.md` 为主要项目建卡(先 2~3 个重要的)
3. 填写 `config.yml`(岗位族、红线、跟进节奏)
4. 往 `profile/star-bank.md` 写 8~12 个 STAR 母题故事
5. 丢第一个 JD 进来,启动工作流

## 隐私

`.gitignore` 已把个人数据排除在外。若要备份,推送到**私有** remote,
绝不推公开仓库(简历含真实联系方式)。
