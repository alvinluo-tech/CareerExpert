#!/usr/bin/env python3
"""中文标点归一化:把 CJK 语境中的半角逗号/分号/冒号/括号转为全角(幂等)。

用法(渲染前对 md/html 各跑一次):
  python <技能目录>/scripts/normalize_punct.py <file.md> [<file.html> ...]

规则(最小干预,避免误伤代码与标签):
  - 仅当标点紧邻 CJK/顿号/右括号一侧时转换,拉丁语境("pandas, numpy")不动
  - .html 只处理标签之间的文本节点,不碰标签与属性
  - .md 先剥 HTML 注释块再处理
exit 0 恒定;打印每文件替换计数。
"""
import re, sys
from pathlib import Path

FW_COMMA, FW_SEMI, FW_COLON, FW_LPAREN, FW_RPAREN = (
    "\uFF0C", "\uFF1B", "\uFF1A", "\uFF08", "\uFF09")  # 全角标点,用码点避免源文件字符歧义

RULES = [
    (re.compile(r"(?<=[\u4e00-\u9fff\u3001)])\,(?=[\u4e00-\u9fffA-Za-z0-9(])"), FW_COMMA),
    (re.compile(r"(?<=[\u4e00-\u9fff\u3001)]);(?=[\u4e00-\u9fffA-Za-z0-9])"), FW_SEMI),
    (re.compile(r"(?<=[\u4e00-\u9fff]):(?=[A-Za-z0-9])"), FW_COLON),
    (re.compile(r"(?<=[\u4e00-\u9fff])\((?=[\u4e00-\u9fffA-Za-z0-9])"), FW_LPAREN),
    (re.compile(r"(?<=[A-Za-z0-9%)])\((?=[\u4e00-\u9fff])"), FW_LPAREN),
    (re.compile(r"(?<=[\u4e00-\u9fffA-Za-z0-9%)])\)(?=[\u4e00-\u9fff\uFF0C\u3002\uFF1B\uFF1A])"), FW_RPAREN),
]

def transform_text(t):
    for rx, full in RULES:
        t = rx.sub(full, t)
    return t

def process(path):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    count = 0
    if p.suffix == ".html":
        out = []
        for i, seg in enumerate(re.split(r"(<[^>]*>)", s)):  # 奇数段是标签,原样保留
            if i % 2 == 1:
                out.append(seg)
            else:
                new = transform_text(seg)
                count += sum(1 for a, b in zip(seg, new) if a != b)
                out.append(new)
        s = "".join(out)
    else:
        s2 = re.sub(r"<!--.*?-->", lambda m: m.group(0), s, flags=re.S)  # 注释保留原样
        new = transform_text(s2)
        count = sum(1 for a, b in zip(s, new) if a != b)
        s = new
    p.write_text(s, encoding="utf-8", newline="\n")
    print(f"OK {p.name}: {count} 处归一化")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    for f in sys.argv[1:]:
        process(f)
