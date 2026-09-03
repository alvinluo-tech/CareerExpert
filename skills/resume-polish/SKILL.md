---
name: resume-polish
description: 专注简历经历深度润色、Google XYZ / HBS PAR 战果量化改写、动词增强、ATS 关键词自然注入、真实代码证据提炼以及事实追溯预检。样式绝对锁定：绝不修改 HTML/CSS 结构与配色。触发词：优化简历内容、润色 Bullet、改写为 Google XYZ、提取强动词、核对数据真实性、ATS 关键词注入，或快捷指令 /polish。
---

# resume-polish — 简历内容精修与战果量化主编技能

> **核心铁律 1：排版样式绝对锁定 (Style-Lock)**！  
> 本技能专注于简历的文字表述深度与业务说服力，**严禁修改 HTML/CSS 布局、颜色或标签结构**。  
> **核心铁律 2：事实完整性不可突破**！  
> 绝对禁止捏造不存在的公司、工作周期、未掌握的技术或伪造数字指标。所有改写必须基于原始素材库或代码库真实证据。

---

## 一、 适用场景与快捷指令

- 用户说：“帮我润色这段项目经历 / 改写成 Google XYZ 格式 / 强化动词 / 看看这段话怎么写更有说服力 / 提取代码库亮点写进简历”
- 用户输入 Slash 指令：`/polish` 或 `/polish-bullet`

---

## 二、 核心公式：Google XYZ 与 HBS PAR

每个经历 Bullet 必须满足严格的产出公式：

### 1. Google XYZ 经典公式
$$\text{Accomplished [X]} \quad \text{as measured by [Y]} \quad \text{by doing [Z]}$$
- **X (战果动作)**：明确达成的核心成果（避免“参与了XX系统开发”这种弱动词，使用“主导重构”、“独立研发”、“突破解决”）；
- **Y (量化指标)**：严谨的度量标准（吞吐量 TPS、P99 延迟、错误率、成本节约、并发人数、代码行数）；
- **Z (工程手段)**：具体的技术与架构手段（如：基于 Go Channel 流水线并发编排、集成 LSM-Tree 存储分层压实）。

### 2. 弱动词替换金标准
- ❌ 负责 / 参与 / 协助 / 完成了...
- ✅ **主导研发** (Spearheaded / Architected)
- ✅ **性能攻坚** (Optimized / Accelerated)
- ✅ **故障止血** (Mitigated / Diagnosed)
- ✅ **架构重构** (Refactored / Decoupled)

---

## 三、 工作流与改写留痕规范

1. **输入分析**：读取候选人原始经历或通过 `python scripts/inspect_repo.py <代码路径>` 提取真实代码证据；
2. **改写对齐**：对照目标岗位关键词，将原始表达提炼重组为 3~4 条 Google XYZ Bullet；
3. **输出改写留痕报告**：
   每条改写必须输出 Before / After / 改写理由：
   ```markdown
   - [Before 原句]: 参与了公司消息网关的重构，提升了性能。
   - [After 改写]: 主导基于 Go 协程池与内存复用重构消息网关，将高并发下 P99 延迟由 120ms 降至 18ms，平稳支撑 2 亿次日调用。
   - [改写理由]: 注入量化指标 (120ms -> 18ms, 2亿次) 与架构手段 (协程池/内存复用)，符合社招技术评审标准。
   ```
4. **事实追溯第一道机械预检**：
   运行自动化核对脚本：
   ```bash
   python scripts/check_facts.py <改写后的简历.md>
   ```
   拦截任何未在素材库中的捏造时间、公司或数字。
