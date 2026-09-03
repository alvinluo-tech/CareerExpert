#!/usr/bin/env python3
"""中文标点归一化:把 CJK 语境中的半角逗号/分号/冒号/括号转为全角(幂等)。

用法(渲染前对 md/html 各跑一次):
  python <技能目录>/scripts/normalize_punct.py <file.md> [<file.html> ...]

规则(最小干预):
  - **<style>/<script> 块整体跳过**——CSS/JS 出现任何全角字符都是破坏
    (var(--fs） 之类的声明会失效,版式崩坏),这是硬性保护
  - .html 只处理标签之间的文本节点,不碰标签与属性
  - 括号按**配对**转换:仅当括号内容含 CJK 时整对转全角;半开全闭/全开半闭
    的混合对自动修复;纯拉丁内容(如 "var(x)")不动
  - 逗号/分号/冒号仅当紧邻 CJK 一侧时转换
exit 0 恒定;打印每文件替换计数。
"""
import re, sys, argparse
from pathlib import Path

FW_COMMA, FW_SEMI, FW_COLON = "\uFF0C", "\uFF1B", "\uFF1A"
FW_LPAREN, FW_RPAREN = "\uFF08", "\uFF09"
CJK = r"\u4e00-\u9fff"

BLOCK = re.compile(r"(<(style|script)\b[^>]*>.*?</\2\s*>)", re.S | re.I)
TAG = re.compile(r"(<[^>]*>)")
PAIR_PAREN = re.compile(r"\(([^()<>]{0,80}?)\)")
MIXED_OPEN = re.compile(r"\(([^<>(){]*?)\uFF09")   # 半开全闭
MIXED_CLOSE = re.compile(r"\uFF08([^<>(){]*?)\)")  # 全开半闭
RULES = [
    (re.compile(rf"(?<=[{CJK}\uFF08\uFF09、)]),(?=[{CJK}A-Za-z0-9(\uFF08])"), FW_COMMA),
    (re.compile(rf"(?<=[{CJK}、)]);(?=[{CJK}A-Za-z0-9])"), FW_SEMI),
    (re.compile(rf"(?<=[{CJK}]):(?=[A-Za-z0-9])"), FW_COLON),
    (re.compile(rf"(?<=[{CJK}]):(?=[{CJK}])"), FW_COLON),
    (re.compile(rf"(?<=[{CJK}A-Za-z0-9%\uFF09)])\)(?=[、。\uFF0C;:!\?\s]|$)"), FW_RPAREN),
]

def has_cjk(s):
    return re.search(rf"[{CJK}]", s) is not None

def transform_text(t):
    # 括号配对:内容含 CJK 的整对转全角(两轮处理嵌套外的平对)
    for _ in range(2):
        t = PAIR_PAREN.sub(lambda m: FW_LPAREN + m.group(1) + FW_RPAREN
                           if has_cjk(m.group(1)) else m.group(0), t)
        t = MIXED_OPEN.sub(lambda m: FW_LPAREN + m.group(1) + FW_RPAREN
                           if has_cjk(m.group(1)) else m.group(0), t)
        t = MIXED_CLOSE.sub(lambda m: FW_LPAREN + m.group(1) + FW_RPAREN
                            if has_cjk(m.group(1)) else m.group(0), t)
    for rx, full in RULES:
        t = rx.sub(full, t)
    return t

def process(path):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    count = 0
    if p.suffix == ".html":
        blocks = re.findall(BLOCK, s)
        for k, (blk, _tag) in enumerate(blocks):
            s = s.replace(blk, f"\u0001{k}\u0001", 1)
        out = []
        for j, sub in enumerate(TAG.split(s)):
            out.append(sub if j % 2 == 1 else transform_text(sub))
        s = "".join(out)
        for k, (blk, _tag) in enumerate(blocks):
            s = s.replace(f"\u0001{k}\u0001", blk, 1)
    else:
        comments = re.findall(r"<!--.*?-->", s, flags=re.S)
        placeholder = "\u0000{}\u0000"
        for k, c in enumerate(comments):
            s = s.replace(c, placeholder.format(k), 1)
        new = transform_text(s)
        count = sum(1 for a, b in zip(s, new) if a != b)
        s = new
        for k, c in enumerate(comments):
            s = s.replace(placeholder.format(k), c)
    p.write_text(s, encoding="utf-8", newline="\n")
    print(f"OK {p.name}: {count} 处归一化")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="中文标点全角归一化(md/html;style/script 块保护)")
    ap.add_argument("files", nargs="+", help="要处理的 .md/.html 文件")
    args = ap.parse_args()
    for f in args.files:
        process(f)
