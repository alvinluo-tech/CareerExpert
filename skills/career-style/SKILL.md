---
name: career-style
description: 专注简历前端视觉排版、HTML/CSS 调色换肤、版面边距与字号微调、严格单页/双页高度契合 (85%~95% 填充率) 以及无头渲染 PDF。触发词：换颜色、换胶囊风格、调整边距、单页排不下、调成双页、调整字体大小、微调 CSS、渲染 PDF，或快捷指令 /career-style。
---

# career-style — 简历视觉工程与排版专精技能

> **核心铁律：文字内容绝对锁定 (Content-Lock)**！  
> 本技能专注于简历的前端呈现、排版美学与打印版面契合度。  
> **严禁修改、删减或改写简历中的任何经历文本、事实描述、公司名称或数字**！所有操作仅限于 HTML 结构装配、CSS 属性微调与 PDF 渲染。

---

## 一、 适用场景与快捷指令

- 用户说：“帮我换成墨绿色 / 换成胶囊风格 / 字体调小一点 / 单页超出了帮我压缩进一页 / 换成黑白经典款”
- 用户输入 Slash 指令：`/career-style`

---

## 二、 5 大内建模版骨架与选用指南

模板均位于 `templates/` 目录：

| 模板文件名 | 风格代号 | 视觉特征 | 推荐人群与岗位 |
|---|---|---|---|
| `resume-template-v3-classic-pro.html` | **经典专业款 (Classic)** | 华尔街无衬线纯黑白 / 紧凑单页 / 顶部分割线 | 金融投行、战略咨询、财会风控、传统国央企 |
| `resume-template-v4-modern-pill.html` | **现代科技款 (Modern Pill)** | 墨绿胶囊徽章 / 科技感卡片阴影 / 高级微渐变 | 互联网大厂、后端研发、架构师、全栈工程师 |
| `resume-template-v5-executive-center.html` | **卓越居中款 (Executive Center)** | 皇家深蓝 / 头部居中对称 / 层次分明 | 校招高潜应届生、管培生、产品经理、项目主管 |
| `resume-template-v6-minimal-clean.html` | **极简留白款 (Minimal Clean)** | 大厂极简风 / 呼吸感边距 / 优雅灰色辅助色 | 设计师、前端研发、初创团队、外企远程岗 |
| `resume-template-v7-academic-cv.html` | **学术双页款 (Academic CV)** | 严格 2 页 / 悬挂缩进 / 顶会期刊引用高亮 | 海外高校硕士/博士申请、高校教职、科研学者 |

---

## 三、 排版调优标准化工作流

### 第一步：读取样式配置中心
查阅 `templates/style.yml`，映射用户需求的视觉属性：
- **主题色 (Palette)**：科技墨绿 (`#1b4332`)、皇家深蓝 (`#1d3557`)、华尔街炭黑 (`#111827`)、勃艮第深红 (`#6b1d2f`) 等；
- **版面布局 (Layout)**：头部居中 (Center) vs 左右两列 (Split) vs 经典顶通 (Top)；
- **模块排序 (Sections)**：教育置顶（校招/学术） vs 工作经历置顶（社招研发）。

### 第二步：单页高度严苛微调 (Page-Fitting)
若内容单页溢出（变成 1.1 页）或填充率过低（留白大于 20%），按以下优先级进行 CSS 微调：
1. **行高与段间距**：调整 `.resume-section { margin-bottom: 12px -> 8px }`；
2. **列表条目间距**：调整 `ul li { margin-bottom: 4px -> 2px }`；
3. **正文字号**：调整 `body { font-size: 9.5pt -> 9.0pt }`（最小不得小于 8.5pt）；
4. **页边距**：调整 `@page { margin: 15mm 18mm -> 12mm 14mm }`。

### 第三步：无头渲染与 ATS 真实回环验证
调用确定性脚本完成无头渲染与文本检查：
```bash
python scripts/render_pdf.py <html文件> <pdf文件> --must "<候选人姓名>" --max-pages 1 --preview preview.png
```
- 确认页数严格为 1（或学术款为 2）；
- 确认填充率处于 **85% ~ 95%** 黄金区间；
- 确认 PyMuPDF 抽取的文本无文字倒置或乱码。
