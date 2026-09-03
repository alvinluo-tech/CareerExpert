#!/usr/bin/env python3
"""
ingest_resume.py — 免门槛简历全格式智能摄取解析器

支持格式:
- .pdf (基于 PyMuPDF / fitz 提取文本与版面)
- .docx (基于 Python 原生 zipfile 与 xml.etree 解析，零外部依赖)
- .tex (LaTeX 简历模版，自动剥离命令标签与宏定义，提取核心结构)
- .md / .txt (Markdown 与纯文本直接提取)

用法:
  python ingest_resume.py <文件路径> [--out <输出目录>] [--json]
示例:
  python ingest_resume.py my_resume.pdf --out profile/
"""

import sys
import os
import re
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_from_pdf(path: Path) -> str:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("FAIL: 未找到 fitz (PyMuPDF) 库，无法解析 PDF。请安装: pip install pymupdf")
    
    doc = fitz.open(str(path))
    pages_text = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages_text.append(f"<!-- Page {i+1} -->\n" + text.strip())
    return "\n\n".join(pages_text)

def extract_from_docx(path: Path) -> str:
    """基于 Python 原生 zipfile 提取 docx 中的所有段落文本，零依赖"""
    try:
        with zipfile.ZipFile(str(path)) as z:
            xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            # w:p 是段落, w:t 是文本节点
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            paragraphs = []
            for p in tree.findall(".//w:p", ns):
                texts = [node.text for node in p.findall(".//w:t", ns) if node.text]
                if texts:
                    paragraphs.append("".join(texts))
            return "\n".join(paragraphs)
    except Exception as e:
        sys.exit(f"FAIL: 解析 DOCX 失败: {e}")

def extract_from_latex(path: Path) -> str:
    """剥离 LaTeX 格式标签，保留核心文字内容与结构"""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    # 移除注释
    lines = []
    for line in raw.splitlines():
        line = re.sub(r'(?<!\\)%.*$', '', line).strip()
        if line:
            lines.append(line)
    text = "\n".join(lines)
    
    # 转换常见命令
    text = re.sub(r'\\section\*?\{([^}]+)\}', r'\n\n## \1\n', text)
    text = re.sub(r'\\subsection\*?\{([^}]+)\}', r'\n### \1\n', text)
    text = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'\n#### \1\n', text)
    text = re.sub(r'\\textbf\{([^}]+)\}', r'**\1**', text)
    text = re.sub(r'\\textit\{([^}]+)\}', r'*\1*', text)
    text = re.sub(r'\\href\{[^}]+\}\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\item\s*', r'- ', text)
    
    # 清理多余 LaTeX 环境标签
    text = re.sub(r'\\begin\{[^}]+\}(\[[^\]]*\])?', '', text)
    text = re.sub(r'\\end\{[^}]+\}', '', text)
    text = re.sub(r'\\[a-zA-Z]+\*?(\{.*?\})?', '', text)
    text = re.sub(r'[{}]', '', text)
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def extract_from_text(path: Path) -> str:
    for enc in ["utf-8", "gbk", "utf-16"]:
        try:
            return path.read_text(encoding=enc).strip()
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore").strip()

def split_sections(text: str) -> dict:
    """基于模式匹配对文本进行粗粒度分块"""
    keywords = {
        "education": ["教育背景", "教育经历", "学业", "学历", "Education"],
        "work": ["工作经历", "工作经验", "职业经历", "实习经历", "Experience", "Employment", "Work Experience"],
        "projects": ["项目经历", "核心项目", "科研经历", "项目经验", "Projects", "Research Experience"],
        "skills": ["专业技能", "技能清单", "技术特长", "IT技能", "Skills", "Technical Skills"],
        "publications": ["论文发表", "学术成果", "科研成果", "Publications", "Papers"],
        "awards": ["荣誉奖项", "奖项证书", "竞赛获奖", "Awards", "Honors", "Certifications"]
    }
    
    sections = {"header": "", "education": "", "work": "", "projects": "", "skills": "", "publications": "", "awards": "", "other": ""}
    
    lines = text.splitlines()
    current_sec = "header"
    buffer = []
    
    for line in lines:
        matched_sec = None
        clean_line = line.strip().strip("#").strip(":").strip("：").strip()
        for sec, kws in keywords.items():
            for kw in kws:
                if kw.lower() == clean_line.lower() or (len(clean_line) <= 12 and kw in clean_line):
                    matched_sec = sec
                    break
            if matched_sec:
                break
        
        if matched_sec:
            if buffer:
                sections[current_sec] += "\n".join(buffer) + "\n"
                buffer = []
            current_sec = matched_sec
        else:
            buffer.append(line)
            
    if buffer:
        sections[current_sec] += "\n".join(buffer) + "\n"
        
    return {k: v.strip() for k, v in sections.items() if v.strip()}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
        
    target = Path(sys.argv[1])
    if not target.exists():
        sys.exit(f"FAIL: 文件不存在: {target}")
        
    suffix = target.suffix.lower()
    print(f"INFO 开始解析: {target.name} (格式: {suffix})")
    
    if suffix == ".pdf":
        raw_text = extract_from_pdf(target)
    elif suffix in (".docx", ".doc"):
        if suffix == ".doc":
            sys.exit("FAIL: 暂不支持老旧二进制 .doc 格式，请在 Word 中另存为 .docx 或 .pdf 后重试。")
        raw_text = extract_from_docx(target)
    elif suffix in (".tex", ".latex"):
        raw_text = extract_from_latex(target)
    elif suffix in (".md", ".txt", ".markdown"):
        raw_text = extract_from_text(target)
    else:
        sys.exit(f"FAIL: 不支持的文件格式: {suffix}。支持: .pdf, .docx, .tex, .md, .txt")

    sections = split_sections(raw_text)
    
    # 检查是否传入 --out
    out_dir = None
    if "--out" in sys.argv:
        idx = sys.argv.index("--out")
        if idx + 1 < len(sys.argv):
            out_dir = Path(sys.argv[idx + 1])
            out_dir.mkdir(parents=True, exist_ok=True)
            
    # 检查是否传入 --json
    if "--json" in sys.argv:
        print(json.dumps({"file": str(target), "sections": sections}, ensure_ascii=False, indent=2))
        return 0

    print("=" * 60)
    print(f"OK 成功提取简历文本，共 {len(raw_text)} 字符，识别到以下主要模块:")
    for sec, content in sections.items():
        print(f"  - [{sec}]: 约 {len(content)} 字符")
    print("=" * 60)
    
    if out_dir:
        # 将摄取到的主简历落盘
        master_dest = out_dir / "master-resume-ingested.md"
        master_dest.write_text(raw_text, encoding="utf-8")
        print(f"OK 原文提取内容已保存至: {master_dest}")
        print("提示: AI 将进一步基于分块内容，自动为你在 profile/ 下拆解出具体的经历卡与项目卡！")
    else:
        print("\n--- 提取文本预览 (前 800 字符) ---")
        print(raw_text[:800])
        if len(raw_text) > 800:
            print("\n... [余下内容已省略，使用 --out <目录> 可自动保存]")
            
    return 0

if __name__ == "__main__":
    sys.exit(main())
