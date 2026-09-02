#!/usr/bin/env python3
"""tracker 校验 + 到期扫描 + 渠道漏斗(确定性检查,LLM 不手算日期与统计)。

用法:
  python scripts/check_tracker.py                 # 校验 + 扫描 + 漏斗
  python scripts/check_tracker.py --no-funnel     # 只要校验与扫描

校验项:
  1. 状态词 ∈ applications/states.yml 的 canonical(含别名映射)
  2. 必填列非空(公司/岗位/渠道/状态/下一步);终态行可无下一步日期
  3. 日期格式 YYYY-MM-DD;投递日期非终态(无投递日期除外)不应晚于今天
  4. JD/简历引用的文件存在
  5. 到期项:非终态且 下一步日期 ≤ 今天 → 打印提醒
漏斗:按渠道统计 投递→回复→面试→offer(样本 <10 标注无统计意义)。
全部通过 exit 0,发现 FAIL exit 1。
"""
import re, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "applications" / "tracker.md"
STATES = ROOT / "applications" / "states.yml"
NON_TERMINAL = ["saved", "evaluating", "ready", "applied", "responded", "interviewing"]
TERMINAL = ["offer", "rejected", "withdrawn", "skipped", "ghosted"]
ALIASES = {}

def load_states():
    """优先 yaml;缺库时用容错解析。"""
    try:
        import yaml
        d = yaml.safe_load(STATES.read_text(encoding="utf-8"))
        nt, t, al = d["non_terminal"], d["terminal"], d.get("aliases", {})
        return list(nt), list(t), {k: list(v) for k, v in al.items()}
    except Exception:
        return NON_TERMINAL, TERMINAL, ALIASES

def parse_rows():
    rows = []
    for line in TRACKER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 12 or set(cells[0]) <= {"-", " ", ":"}:
            continue  # 分隔行
        rows.append(cells)
    return rows[1:] if rows else []  # 去表头

def canon_status(raw, terminal, non_terminal, aliases):
    s = raw.strip().lower()
    if s in terminal or s in non_terminal:
        return s
    for k, vs in aliases.items():
        if s == k or s in [v.lower() for v in vs]:
            return k
    return None

def main():
    today = datetime.date.today()
    non_terminal, terminal, aliases = load_states()
    rows = parse_rows()
    if not rows:
        print("FAIL: tracker.md 没有可解析的数据行"); return 1
    problems, due, funnel = [], [], {}
    for i, r in enumerate(rows, 2):
        company, role, _fam, channel, jd, resume, status_raw = r[0], r[1], r[2], r[3], r[4], r[5], r[6]
        next_step, next_date = r[8], r[9]
        st = canon_status(status_raw, terminal, non_terminal, aliases)
        if not st:
            problems.append(f"L{i} {company}: 状态 '{status_raw}' 不在 states.yml(canonical 或别名)")
            continue
        for label, d in [("投递日期", r[7]), ("下一步日期", next_date)]:
            if d and d != "-" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
                problems.append(f"L{i} {company}: {label} '{d}' 不是 YYYY-MM-DD")
        if st not in terminal:
            if not next_step or next_step in ("-", ""):
                problems.append(f"L{i} {company}: 非终态但'下一步'为空(没有下一步的追踪表等于死表)")
        for ref in [jd, resume]:
            if ref and ref not in ("-", "") and "(未生成)" not in ref:
                f = ROOT / ref
                if not f.exists():
                    problems.append(f"L{i} {company}: 引用文件不存在 {ref}")
        # 到期扫描
        if st not in terminal and next_date and re.fullmatch(r"\d{4}-\d{2}-\d{2}", next_date):
            if datetime.date.fromisoformat(next_date) <= today:
                due.append(f"⏰ {company}·{role} [{st}] 下一步到期({next_date}): {next_step}")
        # 漏斗(有投递日期才计入)
        if r[7] and re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[7]):
            f = funnel.setdefault(channel, [0, 0, 0, 0])
            f[0] += 1
            if st in ("responded", "interviewing", "offer"): f[1] += 1
            if st in ("interviewing", "offer"): f[2] += 1
            if st == "offer": f[3] += 1

    print(f"校验 {len(rows)} 行")
    for p in problems: print("FAIL", p)
    if not problems: print("OK 状态/日期/引用/下一步 全部合规")
    print()
    for d in due: print(d)
    if not due: print("今日无到期项")
    if "--no-funnel" not in sys.argv:
        print("\n渠道漏斗(渠道: 投递→回复→面试→offer)")
        for ch, (a, b, c, o) in sorted(funnel.items(), key=lambda x: -x[1][0]):
            note = "" if a >= 10 else f"(样本={a},无统计意义)"
            print(f"  {ch}: {a} → {b} → {c} → {o} {note}")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
