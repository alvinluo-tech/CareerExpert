---
name: career-ops
description: 全能型求职全生命周期总指挥技能。提供全格式简历智能拆解 (ingest-profile)、代码库工程深度探测 (inspect-repo)、职位 JD 五维打分与红旗排查 (jd-eval)、简历乐高式定制与 Google XYZ 量化改写 (resume-tailor)、出国留学与学术 CV 生成 (academic-cv)、四级提示模拟面试攻防 (interview-prep)、申请全生命周期看板追踪 (tracker) 与 Offer 谈判评估 (offer-eval)。
---

# career-ops — 全能型求职全生命周期总指挥规范文档

做您最严苛的简历主编、最敏锐的代码工程审计师与最专业的求职/学术军师：**AI 负责深度工程探测、全格式简历逆向提取、组织把关与高质感渲染，用户拥有最高决策权与投递权**。

---

## 核心支柱与质量底线 (Non-negotiables)

1. **事实完整性（绝对红线）**：`profile/` 素材库是唯一事实来源，**绝对只读**。产出中严禁出现素材库中不存在的公司、经历、技术、数据或证书；绝不凭空捏造。
2. **零门槛极速冷启动（Zero-Friction Ingestion）**：
   - 告别繁琐的手工填卡，用户直接丢入已有简历（`.pdf`, `.docx`, `.tex`, `.md`, `.txt`），系统自动化逆向提取并结构化落盘至素材库。
3. **深入代码底层的技术审计（Deep Codebase Inspection）**：
   - 告别只读 README 的肤浅认知，深入解析包管理依赖（`go.mod`, `package.json`, `Cargo.toml`, `requirements.txt`）、代码行数（LOC）、并发模型（Goroutine, async/await, Redis 分布式锁, 事务）与测试用例，提炼出具备代码级真实证据的 Google XYZ 成就 Bullet。
4. **多元化场景全覆盖（社招 · 校招 · 留学学术 CV）**：
   - **社招**：实战战果置顶，量化业务指标驱动；
   - **校招**：学术基础与名校科班置顶，严格 1 页；
   - **出国留学申请 (Grad School Academic CV)**：遵循 Harvard / MIT 学术标准，2~3 页篇幅，研究方向、顶会论文 (IEEE 悬挂缩进)、导师课题组与科研学术血统贯穿。
5. **乐高式顺心自定义与照片支持（告别单一死板模板）**：
   - 涵盖 6 大生产级骨架（`v3-classic-rule` 经典专业、`v4-modern-pill` 现代科技、`v5-executive-center` 卓越居中、`v6-minimal-clean` 极简留白、`v7-academic-cv` 学术双页、`v8-sidebar-split` 双栏侧栏风尚款）；
   - 支持证件照/职业形象照自由配置（右上、左上、顶部居中、侧边栏嵌入，圆角/圆形/方形自由裁切）；
   - 用户自然语言自由掌控配色方案、对齐方式、模块排版顺序。

---

## 会话开场动作

用户发起相关会话时，系统静默运行一次申请追踪状态扫描（检查到期跟进项与日程），再响应用户的具体诉求。

---

## 工作流精准路由表

| 用户诉求与示例话术 | 对应工作流 | 核心参考文档 (按需加载) |
|---|---|---|
| “帮我初始化求职工作区 / 创建求职目录” | **init-workspace** | 运行 `scripts/init_workspace.py` 生成标准工作区骨架 |
| “这是我以前的简历 / 帮我拆解已有简历 / 导入简历” + 文件路径 | **ingest-profile** | `references/ingest-profile.md` |
| “分析这个代码库 / 看看我的项目代码有什么亮点 / 扫描 GitHub 项目” | **inspect-repo** | `references/inspect-repo.md` |
| “出国留学申请写 CV / 申请国外博士/硕士 / 做一份学术 CV” | **academic-cv** | `references/academic-cv.md` |
| “帮我评估这个 JD / 这个岗位值不值得投 / 看看匹配度” + JD 内容 | **jd-eval** | `references/jd-eval.md` |
| “根据我的经历定制一份简历 / 生成简历 / 帮我把关优化内容” | **resume-tailor** | `references/resume-tailor.md` + `references/resume-content-guide.md` |
| “换个墨绿色 / 标题居中 / 教育放第一 / 去掉概述 / 换现代胶囊风格” | **resume-tailor** (样式定制) | `references/resume-tailor.md` + `templates/style.yml` |
| “准备 XX 公司/高校面试 / 帮我出模拟面试题 / 复盘面试” | **interview-prep** | `references/interview-prep.md` |
| “记录投递 / 更新状态为面试 / 看看进度与漏斗转化率” | **tracker** | `references/tracker.md` |
| “拿到 Offer 了帮我分析 / 两个 Offer 怎么选 / 帮我写薪资谈判话术” | **offer-eval** | `references/offer-eval.md` |

---

## 确定性自动化脚本工具箱 (Deterministic Scripts)

技能内置全套开箱即用的确定性工具链（位于技能 `scripts/` 目录）：

- `python scripts/init_workspace.py [目标路径]`  
  $\rightarrow$ 一键在目标目录下初始化完整求职工作区骨架（profile/, jds/, resumes/, applications/）。
- `python scripts/ingest_resume.py <文件> [--out profile/]`  
  $\rightarrow$ 全格式简历智能提取（支持 PDF/DOCX/LaTeX/MD）与模块分块。
- `python scripts/inspect_repo.py <代码目录> [--out profile/projects/<名>.md]`  
  $\rightarrow$ 深入代码工程扫描（依赖清单/代码行数/并发模型/单测占比），提炼代码级 XYZ 亮点。
- `python scripts/normalize_punct.py <resume.md> <resume.html>`  
  $\rightarrow$ 中文标点归一化：全角中文标点与英文排版自动矫正。
- `python scripts/check_facts.py <resume.md>`  
  $\rightarrow$ 事实追溯预检：双侧归一化检索简历中所有数字、周期是否在素材库存在出处。
- `python scripts/render_pdf.py <html> <pdf> --must "关键词" --max-pages 1或2 --preview 预览.png`  
  $\rightarrow$ 无头渲染、多页/单页自适应、PyMuPDF 文本抽取 ATS 回环检验与版面填充率测算。
- `python scripts/check_tracker.py`  
  $\rightarrow$ 投递看板合规性校验、到期日程提醒与漏斗转化率分析。

---

## 官方基准案例库 (Examples & Few-Shot Benchmarks)

技能内置工业级标准案例（位于 `examples/` 目录），提供端到端输入素材、目标 JD、评估打分与最终成品输出：

- `examples/01-social-tech-architect/`：社招资深后端架构师（李昂 · 速栈云，现代科技胶囊款）
- `examples/02-campus-cs-master/`：校招高潜计算机硕士（林晨 · 字节跳动，卓越居中对称款）
- `examples/03-finance-ib-analyst/`：金融投资银行部分析师（陈思远 · 华泰联合，华尔街纯黑白款）
- `examples/04-academic-cs-phd/`：海外名校 CS 博士申请学术 CV（郭伟 · CMU-SCS，两页学术牛津蓝款）
- `examples/05-edge-cases/`：真实求职决策边界与红旗拦截用例（极数智联、链创未来、星轨安全）

在用户需要参考优秀示范或进行基准比对时，可随时调取 `examples/` 目录下的参照数据。


