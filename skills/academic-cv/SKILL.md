---
name: academic-cv
description: 专注留学生出国申请、海外高校硕博申请 (Ph.D./Master) 学术 CV 生成与排版。遵循 Harvard/MIT 官方规范，严格 2 页布局，强化导师指导、顶会顶刊论文引用 (CVPR/ICLR/ACL)、科研立项与教学助教经历。触发词：出国留学、申请国外大学、CS/理工科/商科申博申硕、做一份学术 CV、学术论文排版、Harvard/MIT CV 规范，或快捷指令 /cv。
---

# academic-cv — 出国留学与海外硕博申请学术 CV 专精技能

> **核心原则：学术纯粹性与国际接轨**！  
> 学术简历（Curriculum Vitae, CV）与工业界求职简历有着本质区别：  
> - **严禁使用** 企业界商业套话（如“商业赋能”、“创造营收”、“ROI”）；  
> - **必须强调** 学术研究潜力、研究兴趣（Research Interests）、指导导师（Advisor）、发表论文（Publications）、顶会顶刊会议等级与引用、科研立项基金、助教经历（Teaching）与国际学术推荐人（References）。

---

## 一、 适用场景与快捷指令

- 用户说：“我要申请美国/欧洲/新加坡的 CS 博士，帮我做一份 CV / 申硕申请材料 / 整理学术论文列表 / 按照 Harvard 格式排版”
- 用户输入 Slash 指令：`/cv` 或 `/academic-cv`

---

## 二、 学术 CV 黄金模块顺序 (Harvard / MIT 标准)

1. **Header (个人学术头部)**：姓名、就读院校、官方 edu 邮箱、个人学术主页、Google Scholar 链接、GitHub；
2. **Research Interests (研究领域与兴趣)**：3~4 个精准方向（如 3D Gaussian Splatting, Distributed Consistency）；
3. **Education (教育背景)**：院校全称、学位、GPA / 排名、指导导师 (Advised by Prof. XXX)；
4. **Publications (发表学术论文与预印本)**：
   - 标注作者顺位（若是共同一作需注明 `*Co-first Author`）；
   - 论文题目、会议/期刊全称、状态（Accepted, Oral Presentation, Under Review）；
5. **Research Experience (核心科研项目经历)**：课题组、主导的研究问题、方法论创新与实验结果；
6. **Honors & Awards (学术荣誉与奖学金)**：国家级/校级奖学金、竞赛奖项与国际荣誉；
7. **Teaching & Mentoring (助教与指导经历)**：课程名称、职责、学期；
8. **Academic Service & References (学术服务与推荐人)**：审稿人经历、3 位海外/国内导师联络信息。

---

## 三、 专属模板与 2 页无头渲染规范

学术 CV 专用模板位于：`templates/resume-template-v7-academic-cv.html`。
- **视觉风格**：牛津深蓝 (`#0f2b48`)、悬挂缩进、Times / Computer Modern 类 LaTeX 排版风格；
- **渲染指令**：
  ```bash
  python scripts/render_pdf.py <html文件> <pdf文件> --must "<候选人英文名>" --max-pages 2 --preview preview.png
  ```
  严格保证内容舒展填满 2 页，无孤行与版面溢出。
