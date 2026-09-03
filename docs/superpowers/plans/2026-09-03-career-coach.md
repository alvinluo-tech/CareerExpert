# career-coach (简历通盘掌握与答辩军师) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建专属的 `career-coach` 技能及其确定性渲染脚本，为求职者生成包含经历软肋诊断、底层原理补课、高段位思考模型与连环追问解析的精美自包含 HTML 备考通透手册，并自动在浏览器中唤醒查看。

**Architecture:** 
采用纯静态、零外部依赖架构。由 `skills/career-coach/SKILL.md` 定义主动追问与代码库审查协议；`templates/guide-template.html` 承载自包含的现代双色响应式排版与高亮卡片；`scripts/render_guide.py` 负责将结构化分析数据拼装渲染为 HTML 并通过 Python `webbrowser` 原生调用默认浏览器打开；全面接入 `install.ps1` 与自动化测试套件。

**Tech Stack:** 
Python 3.10+ (内置 `webbrowser`, `argparse`, `json`, `html`), Semantic HTML5 + Vanilla CSS3 (自包含无外部 CDN).

---

### Task 1: 构建精美自包含 HTML 模板 (`guide-template.html`)

**Files:**
- Create: `skills/career-coach/templates/guide-template.html`

- [ ] **Step 1: 编写自包含现代设计系统 HTML 模板**
包含四维核心模块占位符、渐变顶栏、高危软肋排雷卡片、技术底座清单、高段位思维导图与连环追问折叠卡片，支持免外部 CDN 独立渲染。

- [ ] **Step 2: 验证模板语法与占位符完整性**
确保 `{{TITLE}}`, `{{CANDIDATE_NAME}}`, `{{TARGET_ROLE}}`, `{{VULNERABILITIES}}`, `{{TECHNICAL_GROUNDING}}`, `{{MENTAL_MODELS}}`, `{{DEEP_DIVE_QA}}` 等插值变量清晰规范。

- [ ] **Step 3: 提交代码**
```bash
git add skills/career-coach/templates/guide-template.html
git commit -m "feat(coach): add self-contained guide-template.html"
```

---

### Task 2: 编写确定性组装与自动唤醒脚本 (`scripts/render_guide.py`)

**Files:**
- Create: `skills/career-coach/scripts/render_guide.py`
- Create: `tests/test_render_guide.py`

- [ ] **Step 1: 编写失败的单元测试**
```python
def test_render_guide_output():
    # 验证传入测试 json 数据时能正常输出完整 html 并不报错
```

- [ ] **Step 2: 运行测试验证失败**
Run: `python tests/test_render_guide.py`
Expected: FAIL (脚本尚未创建)

- [ ] **Step 3: 实现 `render_guide.py`**
支持读取 JSON/Markdown 数据、填充模板、保存到目标路径、支持 `--open` 参数唤起浏览器、支持 `--help` 退出。

- [ ] **Step 4: 运行测试验证通过**
Run: `python tests/test_render_guide.py`
Expected: PASS

- [ ] **Step 5: 提交代码**
```bash
git add skills/career-coach/scripts/render_guide.py tests/test_render_guide.py
git commit -m "feat(coach): implement render_guide.py with auto-browser launch"
```

---

### Task 3: 编写 `career-coach` 技能指令主文档 (`SKILL.md`)

**Files:**
- Create: `skills/career-coach/SKILL.md`

- [ ] **Step 1: 编写技能协议规范**
定义 `/career-coach` 触发词、简历初检逻辑、代码库主动追问话术、结合 `inspect_repo.py` 扫描架构模式、四维手册生成规范与事实守卫红线。

- [ ] **Step 2: 校验前置元信息与命名规范**
确保符合 AI Agent Skill YAML Frontmatter 规范与工作区标准。

- [ ] **Step 3: 提交代码**
```bash
git add skills/career-coach/SKILL.md
git commit -m "feat(coach): add career-coach SKILL.md specification"
```

---

### Task 4: 联动 `career-interview` 与跨技能生态整合

**Files:**
- Modify: `skills/career-interview/SKILL.md`
- Modify: `install.ps1`
- Modify: `README.md`

- [ ] **Step 1: 更新 `career-interview` 引入 coach 备战引导**
在面试开场前增加友好提示：若未生成通透手册，建议运行 `/career-coach` 提前武装思路。

- [ ] **Step 2: 更新 `install.ps1` 注册第 6 大技能**
将 `career-coach` 加入安装清单，支持一键部署到 Claude Code、Codex、Antigravity 全局。

- [ ] **Step 3: 更新 `README.md` 技能矩阵表**
加入 `career-coach` 说明与使用示例。

- [ ] **Step 4: 提交代码**
```bash
git add skills/career-interview/SKILL.md install.ps1 README.md
git commit -m "feat(coach): integrate career-coach into installer and interview skill"
```

---

### Task 5: 真实实战基准案例与自动化回归测试

**Files:**
- Create: `skills/career-coach/examples/01-fastflow-middleware-guide/`
- Modify: `tests/test_e2e_scenarios.py`

- [ ] **Step 1: 搭建基准测试案例 01**
以李昂 FastFlow 流式引擎 + 字节跳动中间件专家为例，生成一份真实的 `fastflow-mastery-guide.html`。

- [ ] **Step 2: 在 `tests/test_e2e_scenarios.py` 中增加 Test 11**
验证从简历提取到 coach 手册渲染及 HTML 关键标签存在性的完整闭环。

- [ ] **Step 3: 运行完整自动化测试套件**
Run: `python tests/test_e2e_scenarios.py`
Expected: 11 / 11 PASSED (100% 成功)

- [ ] **Step 4: 提交并推送到 GitHub 远端**
```bash
git add -A
git commit -m "feat: complete career-coach skill with benchmark case and e2e test"
git push origin main
```
