#!/usr/bin/env python3
"""
render_guide.py — 《简历通盘掌握与答辩全景指导手册》确定性渲染脚本

功能：
  读取结构化分析数据 (JSON 或 Markdown)，结合自包含现代设计模板，
  编译生成高质感单文件 HTML 手册，并支持自动调用系统默认浏览器唤醒查看。

用法：
  python render_guide.py <input.json> [--out applications/coach/guide.html] [--open]
"""

import sys
import json
import argparse
import html
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "guide-template.html"

def render_vulnerabilities(vulns):
    if not vulns:
        return "<p style='color:#64748b;'>暂无显著高危软肋，经历较为扎实。</p>"
    items = []
    for v in vulns:
        title = html.escape(v.get("title", "重点审查项"))
        quote = html.escape(v.get("quote", ""))
        subtext = html.escape(v.get("subtext", ""))
        items.append(f"""
        <div class="vulnerability-card">
          <h4>{title}</h4>
          <div class="quote">“{quote}”</div>
          <div class="subtext"><b>考官审查视角与深挖意图：</b>{subtext}</div>
        </div>
        """)
    return "\n".join(items)

def render_grounding(items):
    if not items:
        return "<p style='color:#64748b;'>暂无特定底层原理补课需求。</p>"
    res = []
    for g in items:
        title = html.escape(g.get("title", "底层原理"))
        content = html.escape(g.get("content", ""))
        bullets = g.get("bullets", [])
        bullets_html = "".join([f"<li>{html.escape(b)}</li>" for b in bullets])
        res.append(f"""
        <div class="grounding-item">
          <h4>{title}</h4>
          <p>{content}</p>
          <ul>{bullets_html}</ul>
        </div>
        """)
    return "\n".join(res)

def render_models(models):
    if not models:
        return "<p style='color:#64748b;'>遵循标准 STAR 结构答辩即可。</p>"
    res = []
    for m in models:
        title = html.escape(m.get("title", "思考模型"))
        steps = m.get("steps", [])
        steps_html = []
        for s in steps:
            s_name = html.escape(s.get("name", ""))
            s_desc = html.escape(s.get("desc", ""))
            steps_html.append(f"""
            <div class="step-box">
              <b>{s_name}</b>
              <span>{s_desc}</span>
            </div>
            """)
        steps_combined = "".join(steps_html)
        res.append(f"""
        <div class="model-card">
          <h4>{title}</h4>
          <div class="model-steps">{steps_combined}</div>
        </div>
        """)
    return "\n".join(res)

def render_qa(qa_list):
    if not qa_list:
        return "<p style='color:#64748b;'>暂无预设攻防题组。</p>"
    res = []
    for qa in qa_list:
        q = html.escape(qa.get("question", ""))
        intent = html.escape(qa.get("intent", ""))
        ans = html.escape(qa.get("answer", ""))
        res.append(f"""
        <div class="qa-card">
          <div class="qa-header">{q}</div>
          <div class="qa-body">
            <div class="qa-intent">💡 <b>考察维度与意图</b>：{intent}</div>
            <div class="qa-answer">
              <b>答辩逻辑与核心要点参考</b>：<br>
              {ans}
            </div>
          </div>
        </div>
        """)
    return "\n".join(res)

def build_guide_html(data, template_path=TEMPLATE_PATH):
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found at: {template_path}")
    template = template_path.read_text(encoding="utf-8")
    
    title = html.escape(data.get("title", "简历通盘掌握与答辩全景指导手册"))
    cand = html.escape(data.get("candidate_name", "求职者"))
    role = html.escape(data.get("target_role", "通用目标岗位"))
    date_str = html.escape(data.get("gen_date", "2026-09-03"))
    summary = html.escape(data.get("stats_summary", "全景经历与代码深度诊断"))
    
    vulns_html = render_vulnerabilities(data.get("vulnerabilities", []))
    grounding_html = render_grounding(data.get("technical_grounding", []))
    models_html = render_models(data.get("mental_models", []))
    qa_html = render_qa(data.get("deep_dive_qa", []))
    
    rendered = template.replace("{{TITLE}}", title)
    rendered = rendered.replace("{{CANDIDATE_NAME}}", cand)
    rendered = rendered.replace("{{TARGET_ROLE}}", role)
    rendered = rendered.replace("{{GEN_DATE}}", date_str)
    rendered = rendered.replace("{{STATS_SUMMARY}}", summary)
    rendered = rendered.replace("{{VULNERABILITIES}}", vulns_html)
    rendered = rendered.replace("{{TECHNICAL_GROUNDING}}", grounding_html)
    rendered = rendered.replace("{{MENTAL_MODELS}}", models_html)
    rendered = rendered.replace("{{DEEP_DIVE_QA}}", qa_html)
    
    return rendered

def main():
    parser = argparse.ArgumentParser(description="CareerExpert — 简历通盘掌握手册编译与唤醒工具")
    parser.add_argument("input_data", help="JSON 格式分析数据路径")
    parser.add_argument("--out", default="mastery-guide.html", help="输出 HTML 文件路径")
    parser.add_argument("--template", default=str(TEMPLATE_PATH), help="指定 HTML 模板路径")
    parser.add_argument("--open", action="store_true", help="生成后自动调用系统浏览器打开")
    
    args = parser.parse_args()
    
    input_path = Path(args.input_data).resolve()
    if not input_path.exists():
        print(f"ERROR: 找不到输入数据文件: {input_path}", file=sys.stderr)
        return 1
        
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: 解析 JSON 失败: {e}", file=sys.stderr)
        return 1
        
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    html_content = build_guide_html(data, Path(args.template).resolve())
    out_path.write_text(html_content, encoding="utf-8")
    
    print(f"OK 成功编译精美复习手册: {out_path}")
    
    if args.open:
        print(f"INFO 正在自动唤醒浏览器打开: {out_path.as_uri()}")
        webbrowser.open(out_path.as_uri())
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
