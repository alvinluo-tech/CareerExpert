#!/usr/bin/env python3
"""事实追溯预检:简历里的数字/日期是否都能在 profile/ 素材库找到出处。

用法:
  python scripts/check_facts.py <resume.md> [--profile-dir profile]

机制:提取简历中的量化数字(带单位或百分比)、年份区间、公司名,
逐个在 profile/ 下做文本检索;找不到出处的列出清单。
注意:这是**启发式第一道网**,不是证明——措辞改写导致的语义不匹配
(数字对但事实错了)仍需 LLM 按对齐校验流程逐条核对。
exit 0 = 全部可追溯;exit 1 = 有不可追溯项(agent 须处理后再交付)。
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def extract_claims(text):
    lines = text.splitlines()
    claims = set()
    for ln in lines:
        if re.match(r"#|>\s*|联系方式|姓名|状态|日期", ln):
            continue  # 跳过标题/注释头/联系行(手机号等不追索)
        for m in re.finditer(r"\d[\d,.]*\s*(?:万|亿|%|ms|k|K|人日|events/s|倍|年|个|次|人|天|分钟)?", ln):
            tok = re.sub(r"\s+", "", m.group(0)).rstrip(",")
            if len(tok) >= 2 and not re.fullmatch(r"[01]|\d{4}(?!\.|-)", tok):
                claims.add(tok)
        for m in re.finditer(r"\d{4}\.\d{2}\s*~\s*\S+", ln):
            claims.add(re.sub(r"\s+", "", m.group(0)))
    return sorted(claims)

def main():
    ap = sys.argv[1:]
    if not ap:
        print(__doc__); return 1
    resume = Path(ap[0])
    prof = Path(ap[ap.index("--profile-dir") + 1]) if "--profile-dir" in ap else ROOT / "profile"
    corpus = "\n".join(p.read_text(encoding="utf-8", errors="ignore")
                       for p in prof.rglob("*.md"))
    corpus_flat = re.sub(r"\s+", "", corpus)  # 双侧空白归一化:"8.5 万"与"8.5万"等价
    missing = []
    for c in extract_claims(resume.read_text(encoding="utf-8")):
        if c not in corpus_flat:
            missing.append(c)
    if missing:
        print(f"FAIL {len(missing)} 项在 profile/ 中无出处(须改写、补素材或删除):")
        for m in missing: print("  -", m)
        return 1
    print("OK 所有量化数字/日期区间均可在 profile/ 素材库中追溯")
    return 0

if __name__ == "__main__":
    sys.exit(main())
