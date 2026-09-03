# examples/ — 官方工业级实操案例库 (Official Exemplars)

本目录依照 **Anthropic 官方 Skills 规范** (`anthropics/skills`) 与开源标杆项目设计，为 `job-finding` 技能提供完整、自包含、可复现的四大代表性场景基准案例（Few-shot Reference Implementations）。

每一个案例均包含该场景下的**完整输入素材 (profile/)、目标职位或录取要求 (jd.md)、AI 评估与匹配度分析报告 (evaluation.md) 以及最终生成的结构化产出包 (output/)**。

---

## 案例矩阵导览

| 案例目录 | 场景领域与类型 | 候选人人设 | 核心亮点与策略 | 产出物清单 |
|---|---|---|---|---|
| **[01-social-tech-architect](01-social-tech-architect/)** | 社招资深后端<br>(social × tech-engineering) | 李昂 (4年经验) | 现代科技胶囊款 (v4) · 墨绿配色 · 2亿级网关重构 · GitHub 开源链接 | `resume.html`<br>`resume.pdf` (1页)<br>`report.md` |
| **[02-campus-cs-master](02-campus-cs-master/)** | 校招高潜应届生<br>(campus × tech-engineering) | 林晨 (浙大硕士) | 卓越居中对称款 (v5) · 皇家深蓝 · GPA 3.85置顶 · 自研 Raft-KV 存储 | `resume.html`<br>`resume.pdf` (1页)<br>`report.md` |
| **[03-finance-ib-analyst](03-finance-ib-analyst/)** | 金融投行分析师<br>(social/campus × finance-ib) | 陈思远 (复旦金融硕) | 经典专业款 (v3) · 华尔街纯黑白 · CPA 5科置顶 · 12.5亿并购量化 | `resume.html`<br>`resume.pdf` (1页)<br>`report.md` |
| **[04-academic-cs-phd](04-academic-cs-phd/)** | 出国留学学术 CV<br>(grad-school × academic) | 郭伟 (清华计算机本科) | 学术双页款 (v7) · 牛津深蓝 · CVPR Oral 一作 · IEEE 悬挂缩进 | `cv.html`<br>`cv.pdf` (2页)<br>`report.md` |
| **[06-creative-product-manager](06-creative-product-manager/)** | 出海产品总监/泛管理<br>(global × product-business) | 苏若涵 (LSE硕士/5年经验) | 双栏侧栏款 (v8) · 宝石蓝 · 侧栏经典证件照 · 4500万$日流水 | `resume.html`<br>`resume.pdf` (1页)<br>`report.md` |
| **[07-ai-agent-architect](07-ai-agent-architect/)** | AI大模型/智能体架构<br>(tech × genai-agent) | 顾远 (UPenn硕/上交ACM) | 极简留白款 (v6) · 石墨碳黑 · 右上角标准证件照 · 12.8k★开源 | `resume.html`<br>`resume.pdf` (1页)<br>`report.md` |
| **[05-edge-cases](05-edge-cases/)** | 真实边界与红旗测试用例 | - | 涵盖用户 override、年限风险预警、炒币/Ghost红旗拦截 | `evaluation.md`<br>决策留痕 |

---

## 一键复现 Prompt 清单

用户在使用本技能时，只需提供类似素材，并使用以下对应的 Prompt 即可获得同等水准的产出：

### 1. 社招资深架构师 (Prompt)
```text
请读取 examples/01-social-tech-architect/profile/ 中的素材，
帮我评估速栈云的这个 Go 后端基础设施 JD (examples/01-social-tech-architect/jd.md)。
合适的话按照现代科技胶囊款 (v4-modern-pill) 为我定制一版简历：
采用科技墨绿配色 (emerald-tech)，重点突出我的统一接入网关重构与分布式调度经历，
技能展示用现代圆角胶囊样式 (pill-badges)，附带上我的开源网关 GitHub 地址，
严格保证 1 页纸，并通过真实文本抽取检验，输出定制报告。
```

### 2. 校招高潜应届生 (Prompt)
```text
请读取 examples/02-campus-cs-master/profile/ 中的素材，
帮我评估字节跳动的后端校招 JD (examples/02-campus-cs-master/jd.md)，
并严格按照 campus 校招策略生成一版简历：
选用卓越居中对称款 (v5-executive-center)，深海蓝色调 (navy-executive)，
教育经历必须置顶第一屏并高亮我的 GPA 3.85 与核心主修课程，去掉概述，
加上我的竞赛荣誉与自研 Raft-KV 存储开源项目（附带 GitHub 链接），严格控制在 1 页纸。
```

### 3. 金融投行分析师 (Prompt)
```text
请读取 examples/03-finance-ib-analyst/profile/ 中的素材，
帮我评估华泰联合证券投行分析师 JD (examples/03-finance-ib-analyst/jd.md)，
并严格遵守金融投行策略包：
选用经典专业款 (v3-classic-rule)，强制执行华尔街纯黑白单页标准 (wallstreet-mono)，
教育经历与 CPA 专业资格置顶，突出 12.5 亿元并购尽调与 DCF 估值模型的硬核财务量化战果，
去掉普通项目区，排版紧凑严谨，输出纯黑白一页纸 PDF 与定制报告。
```

### 4. 出国留学学术 CV (Prompt)
```text
请读取 examples/04-academic-cs-phd/profile/ 中的素材，
我正在申请卡内基梅隆大学 (CMU) 计算机系博士 (Ph.D. in Computer Science)，
请帮我评估 examples/04-academic-cs-phd/jd.md 的申请匹配度，
并严格遵循 Harvard/MIT 学术规范生成一份 2 页的学术 CV (Academic CV)：
选用学术双页款 (v7-academic-cv)，经典学术深蓝 (oxford-blue)，
置顶研究方向 (3D Vision / Neural Rendering)，教育经历高亮 GPA 3.93 与院士导师，
论文模块严格按 IEEE 规范引用并粗体标注我的姓名，高亮 CVPR Oral 与开源代码，
生成标准 2 页学术 PDF 与定制报告。
```

### 5. 出海商业产品总监 · 双栏证件照款 (Prompt)
```text
请读取 examples/06-creative-product-manager/profile/ 中的素材，
帮我评估 TikTok E-Commerce 的海外支付产品专家 JD，
选用双栏侧边栏风尚款 (v8-sidebar-split)，主题配色为商务宝石蓝，
开启照片展示 (photo.show: true)，将我的真实职业证件照置于左侧边栏顶端，
左侧栏集中展示联系方式、技能微胶囊与海外语言资质，右侧主干突出东南亚日均 4500 万美元交易流水与动态路由 12.3% 成功率提升，
严格保持 A4 单页黄金填充率。
```

### 6. AI 大模型系统架构师 · 极简右上角证件照款 (Prompt)
```text
请读取 examples/07-ai-agent-architect/profile/ 中的素材，
帮我评估头部大模型独角兽的资深 AI Agent 架构师 JD，
选用大厂极简纯粹留白款 (v6-minimal-clean)，高级石墨碳黑色调，
在右上角嵌入我的标准 1 寸职业证件照，
突出开源项目 FastAgent (12.8k Stars)、多 Agent 流水线与投机采样推理加速吞吐 3.4 倍战果，
严格保证 A4 单页 88% 黄金填充率。
```

### 7. 用户增量补充项目与在线链接 · 靶向字节跳动中间件 (Prompt)
```text
这是我之前生成的简历 PDF (input/base_resume.pdf)。
最近我业余主导了一个高性能流式数据引擎开源项目 FastFlow：
- GitHub 仓库: https://github.com/leon-tech/fastflow
- 在线演示 Demo: https://fastflow.dev/demo
- 核心指标: 单节点 18.5万 QPS，内存降低 42%，单机支撑 8000+ 虚拟流，获得 1.2k★。
现在我想投递字节跳动基础架构部【高并发流媒体与分布式中间件专家】岗位 (input/target_jd.md)。
请帮我安全录入该项目与链接，重新靶向生成单页 PDF 简历（超链接在 PDF 中可点击），
并输出一份详细的 Before vs After 优化改写报告。
```
