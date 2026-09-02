#!/usr/bin/env python3
"""渲染简历 HTML → PDF 并验证(页数/填充率/关键字段),可附输出预览 PNG。

用法(脚本在技能包内,对任意求职仓库可用):
  python <技能目录>/scripts/render_pdf.py <input.html> <output.pdf> \
      --must "李昂,138,P99" --max-pages 1 --preview preview.png

行为:
  1. 自动探测 Edge/Chrome(Windows/macOS/Linux 常见路径)
  2. 无头渲染 PDF(--no-pdf-header-footer)
  3. 有 PyMuPDF 时验证:页数 ≤ --max-pages;--must 关键词全部可提取
     (ATS 回环;匹配前两侧空白归一化——PDF 提取的换行/空格会把
     "8.5 万"拆成"8.5\\n万",属提取伪影而非 ATS 缺词;
     语义级核对仍由 LLM 对齐校验负责);打印版面填充率(单页 80%~95%)
  4. --preview 输出 PNG 供视觉检查(样式实质变更时必做)
  5. 全部通过 exit 0,否则 exit 1(agent 应据此修复而不是交付)
"""
import argparse, subprocess, sys
from pathlib import Path

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
]

def find_browser():
    for p in BROWSERS:
        if Path(p).exists():
            return p
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("pdf")
    ap.add_argument("--must", default="", help="逗号分隔的必提取关键词")
    ap.add_argument("--max-pages", type=int, default=2)
    ap.add_argument("--preview", default="", help="同时输出首页 PNG 到此路径(视觉检查用)")
    args = ap.parse_args()

    html, pdf = Path(args.html).resolve(), Path(args.pdf).resolve()
    if not html.exists():
        print(f"FAIL: {html} 不存在"); return 1
    browser = find_browser()
    if not browser:
        print("FAIL: 未找到 Edge/Chrome,请手动渲染或安装"); return 1

    subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", html.as_uri()],
                   capture_output=True, timeout=60)
    if not pdf.exists():
        print("FAIL: 渲染后 PDF 未生成"); return 1
    print(f"OK 渲染: {pdf}")

    try:
        import fitz
    except ImportError:
        print("WARN: 未安装 PyMuPDF(pip install pymupdf),跳过内容验证")
        return 0

    doc = fitz.open(pdf)
    text = "".join(page.get_text() for page in doc)
    ok = True
    if len(doc) > args.max_pages:
        print(f"FAIL 页数: {len(doc)} > {args.max_pages}"); ok = False
    else:
        print(f"OK 页数: {len(doc)}")
    norm = "".join(text.split())
    missing = [k for k in args.must.split(",") if k
               and "".join(k.split()) not in norm]
    if missing:
        print(f"FAIL 提取: 缺失关键词 {missing}(ATS 解析风险)"); ok = False
    else:
        n = len([k for k in args.must.split(",") if k])
        print(f"OK 提取: {n} 个关键词全部可提取")
    blocks = doc[0].get_text("blocks")
    fill = max(b[3] for b in blocks) / doc[0].rect.height * 100
    print(f"INFO 填充率: {fill:.0f}%"
          + ("" if 80 <= fill <= 98 or len(doc) > 1 else
             "(单页目标 80%~95%;偏低升 density,偏高减内容;"
             "素材过薄时以事实完整性优先,不得硬凑)"))
    if args.preview:
        pix = doc[0].get_pixmap(dpi=110)
        Path(args.preview).parent.mkdir(parents=True, exist_ok=True)
        pix.save(args.preview)
        print(f"OK 预览: {args.preview}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
