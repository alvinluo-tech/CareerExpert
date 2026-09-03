#!/usr/bin/env python3
"""
render_guide.py — 《简历通盘掌握与答辩全景指导手册》确定性渲染脚本 (深度升级版)

功能：
  读取结构化深度分析数据 (JSON)，结合自包含现代技术工作台设计系统，
  编译生成包含架构拓扑、底层源码、数学算账、STAR-T 思考模型与红绿榜攻防的
  极其丰富详尽的高质感单文件 HTML 备战手册。

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
        return "<p style='color:#64748b;'>暂无显著高危软肋，经历表述较为扎实。</p>"
    items = []
    for v in vulns:
        title = html.escape(v.get("title", "重点排雷项"))
        quote = html.escape(v.get("quote", ""))
        severity = html.escape(v.get("severity", "高危审问"))
        subtext = html.escape(v.get("subtext", ""))
        mitigation = html.escape(v.get("mitigation", "答题时务必主动定场景，不可含糊。"))
        items.append(f"""
        <div class="trap-card">
          <div class="trap-top">
            <span class="trap-severity">{severity}</span>
            <h3>{title}</h3>
          </div>
          <div class="trap-quote">“{quote}”</div>
          <div class="subtext-block">
            <p><b>🕵️ 考官真实审查视角与潜台词：</b>{subtext}</p>
            <p style="margin-top: 8px; color: #1e3a8a;"><b>🛡️ 军师避坑防守指引：</b>{mitigation}</p>
          </div>
        </div>
        """)
    return "\n".join(items)

def render_architecture(arch):
    if not arch:
        return "<p style='color:#64748b;'>暂无专用架构拓扑定义。</p>"
    overview = html.escape(arch.get("overview", "系统全局架构拓扑"))
    diagram_ascii = html.escape(arch.get("diagram", ""))
    flow_steps = arch.get("flow_steps", [])
    
    flow_html = []
    for step in flow_steps:
        s_name = html.escape(step.get("name", ""))
        s_desc = html.escape(step.get("desc", ""))
        flow_html.append(f"""
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 12px 14px; margin-bottom: 8px;">
          <strong style="color: #38bdf8;">{s_name}</strong>：<span style="color: #cbd5e1; font-size: 13px;">{s_desc}</span>
        </div>
        """)
    flow_combined = "\n".join(flow_html)
    
    return f"""
    <div style="margin-bottom: 18px; font-size: 13.5px; line-height: 1.6; color: #334155;">
      {overview}
    </div>
    <div class="architecture-diagram">
      <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; margin-bottom: 8px; letter-spacing: 1px;">
        ASCII 数据流转与架构白板拓扑
      </div>
      <pre style="margin: 0; font-family: ui-monospace, monospace; color: #38bdf8; font-size: 12.5px; line-height: 1.4;">{diagram_ascii}</pre>
    </div>
    <div style="margin-top: 16px;">
      <h4 style="font-size: 13.5px; margin-bottom: 10px; color: #0f172a;">全链路核心数据流动分解：</h4>
      {flow_combined}
    </div>
    """

def render_code_grounding(code_items):
    if not code_items:
        return "<p style='color:#64748b;'>暂无源码级实现分析。</p>"
    items = []
    for item in code_items:
        title = html.escape(item.get("title", "核心源码机制"))
        lang = html.escape(item.get("language", "go"))
        snippet = html.escape(item.get("snippet", ""))
        explanation = html.escape(item.get("explanation", ""))
        takeaways = item.get("takeaways", [])
        takeaways_html = "".join([f"<li>{html.escape(t)}</li>" for t in takeaways])
        
        items.append(f"""
        <div class="code-section">
          <div class="code-title">
            <span style="background: #0f172a; color: #fff; font-size: 11px; padding: 2px 6px; border-radius: 4px;">{lang}</span>
            {title}
          </div>
          <pre class="code-container"><code>{snippet}</code></pre>
          <div class="code-explain">
            <p><strong>底层原理解析：</strong>{explanation}</p>
            <ul style="margin-top: 8px; padding-left: 20px; font-size: 12.5px;">
              {takeaways_html}
            </ul>
          </div>
        </div>
        """)
    return "\n".join(items)

def render_math(math_items):
    if not math_items:
        return "<p style='color:#64748b;'>暂无数学算账推导数据。</p>"
    items = []
    for m in math_items:
        title = html.escape(m.get("title", "算账推导"))
        formula = html.escape(m.get("formula", ""))
        breakdown = html.escape(m.get("breakdown", ""))
        conclusion = html.escape(m.get("conclusion", ""))
        items.append(f"""
        <div class="math-card">
          <h4 style="font-size: 14px; color: #0369a1; margin-bottom: 8px;">{title}</h4>
          <div class="math-formula">{formula}</div>
          <div class="math-details">
            <p><strong>数值拆解：</strong>{breakdown}</p>
            <p style="margin-top: 6px; color: #0f172a;"><strong>💡 考官答辩结语：</strong>{conclusion}</p>
          </div>
        </div>
        """)
    return "\n".join(items)

def render_models(models):
    if not models:
        return "<p style='color:#64748b;'>遵循标准结构即可。</p>"
    items = []
    for m in models:
        title = html.escape(m.get("title", "高段位思维模型"))
        tagline = html.escape(m.get("tagline", ""))
        steps = m.get("steps", [])
        steps_html = []
        for s in steps:
            s_name = html.escape(s.get("name", ""))
            s_desc = html.escape(s.get("desc", ""))
            steps_html.append(f"""
            <div class="start-box">
              <div class="step-tag">{s_name}</div>
              <p>{s_desc}</p>
            </div>
            """)
        steps_combined = "".join(steps_html)
        items.append(f"""
        <div style="margin-bottom: 24px;">
          <h3 style="font-size: 15px; color: #1e1b4b; margin-bottom: 4px;">{title}</h3>
          <p style="font-size: 12.5px; color: #64748b; margin-bottom: 12px;">{tagline}</p>
          <div class="start-model-grid">
            {steps_combined}
          </div>
        </div>
        """)
    return "\n".join(items)

def render_qa(qa_list):
    if not qa_list:
        return "<p style='color:#64748b;'>暂无问答攻防演练。</p>"
    items = []
    for i, qa in enumerate(qa_list, 1):
        q = html.escape(qa.get("question", ""))
        intent = html.escape(qa.get("intent", ""))
        red_flag = html.escape(qa.get("red_flag", ""))
        green_flag = html.escape(qa.get("green_flag", ""))
        script = qa.get("master_script", "")
        
        items.append(f"""
        <div class="dialogue-card">
          <div class="dialogue-q">
            <span class="badge">Round {i:02d}</span>
            <span>{q}</span>
          </div>
          <div class="dialogue-body">
            <div class="dialogue-intent">
              <strong>🎯 考官考察真实意图：</strong>{intent}
            </div>
            <div class="comparison-grid">
              <div class="flag-box red">
                <h5>❌ 常见翻车外行回答 (扣分/质疑)</h5>
                <p>{red_flag}</p>
              </div>
              <div class="flag-box green">
                <h5>✅ 资深架构师破局思路 (加分/大将之风)</h5>
                <p>{green_flag}</p>
              </div>
            </div>
            <div class="master-script">
              <div style="font-size: 11px; text-transform: uppercase; color: #0284c7; font-weight: 800; letter-spacing: 1px; margin-bottom: 6px;">
                🎙️ 推荐满分答辩范本
              </div>
              <div>{script}</div>
            </div>
          </div>
        </div>
        """)
    return "\n".join(items)

def build_guide_html(data, template_path=TEMPLATE_PATH):
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found at: {template_path}")
    template = template_path.read_text(encoding="utf-8")
    
    title = html.escape(data.get("title", "简历通盘掌握与答辩全景指导手册"))
    cand = html.escape(data.get("candidate_name", "求职者"))
    role = html.escape(data.get("target_role", "目标岗位"))
    proj = html.escape(data.get("project_name", "标杆项目"))
    date_str = html.escape(data.get("gen_date", "2026-09-03"))
    
    metrics = data.get("key_metrics", [
        {"val": "18.5万 QPS", "lbl": "单机实测极限吞吐"},
        {"val": "4.2 ms", "lbl": "P99 核心延迟"},
        {"val": "42%", "lbl": "内存开销下降"},
        {"val": "100%", "lbl": "代码事实可追溯"}
    ])
    
    rendered = template.replace("{{TITLE}}", title)
    rendered = rendered.replace("{{CANDIDATE_NAME}}", cand)
    rendered = rendered.replace("{{TARGET_ROLE}}", role)
    rendered = rendered.replace("{{PROJECT_NAME}}", proj)
    rendered = rendered.replace("{{GEN_DATE}}", date_str)
    
    for idx in range(1, 5):
        m = metrics[idx-1] if len(metrics) >= idx else {"val": "-", "lbl": "-"}
        rendered = rendered.replace(f"{{{{METRIC_{idx}_VAL}}}}", html.escape(m.get("val", "")))
        rendered = rendered.replace(f"{{{{METRIC_{idx}_LBL}}}}", html.escape(m.get("lbl", "")))
        
    rendered = rendered.replace("{{VULNERABILITIES}}", render_vulnerabilities(data.get("vulnerabilities", [])))
    rendered = rendered.replace("{{ARCHITECTURE_SECTION}}", render_architecture(data.get("architecture", {})))
    rendered = rendered.replace("{{CODE_GROUNDING_SECTION}}", render_code_grounding(data.get("code_grounding", [])))
    rendered = rendered.replace("{{MATH_METRICS_SECTION}}", render_math(data.get("math_metrics", [])))
    rendered = rendered.replace("{{MENTAL_MODELS_SECTION}}", render_models(data.get("mental_models", [])))
    rendered = rendered.replace("{{DEEP_DIVE_QA_SECTION}}", render_qa(data.get("deep_dive_qa", [])))
    
    return rendered

def main():
    parser = argparse.ArgumentParser(description="CareerExpert — 简历通盘掌握手册深度编译与唤醒工具")
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
    
    print(f"OK 成功编译高质感全景复习手册: {out_path}")
    
    if args.open:
        print(f"INFO 正在自动唤醒浏览器打开: {out_path.as_uri()}")
        webbrowser.open(out_path.as_uri())
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
