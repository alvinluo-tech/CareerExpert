#!/usr/bin/env python3
"""tracker 校验 + 到期扫描 + 渠道漏斗 + 投递节奏(确定性检查,日期与统计不心算)。

用法(脚本在技能包内;仓库根 = 从当前目录向上找到 applications/tracker.md 的位置):
  python <技能目录>/scripts/check_tracker.py
  python scripts/check_tracker.py --no-funnel      # 只要校验与扫描

校验项:
  1. 状态词 ∈ applications/states.yml 的 canonical(含别名映射)
  2. 必填列非空(公司/岗位/渠道/状态/下一步);终态行可无下一步
  3. 日期格式 YYYY-MM-DD
  4. JD/简历引用的文件存在
  5. 到期项:非终态且 下一步日期 ≤ 今天 → 打印提醒
输出:渠道漏斗(投递→回复→面试→offer)+ 投递节奏(近 4 周自然周)。
空 tracker 是合法状态(新仓库):WARN 不 FAIL。
全部通过 exit 0,发现 FAIL exit 1。
"""
import re, sys, datetime
from pathlib import Path

NON_TERMINAL = ["saved", "evaluating", "ready", "applied", "responded", "interviewing"]
TERMINAL = ["offer", "rejected", "withdrawn", "skipped", "ghosted"]

def find_repo_root():
    """从当前目录向上找 applications/tracker.md;找不到再从脚本位置向上找。"""
    for start in [Path.cwd(), Path(__file__).resolve()]:
        d = start
        for _ in range(6):
            if (d / "applications" / "tracker.md").exists():
                return d
            d = d.parent
    return None

def load_states(root):
    try:
        import yaml
        d = yaml.safe_load((root / "applications" / "states.yml").read_text(encoding="utf-8"))
        return list(d["non_terminal"]), list(d["terminal"]), {k: list(v) for k, v in d.get("aliases", {}).items()}
    except Exception:
        return NON_TERMINAL, TERMINAL, {}

def canon_status(raw, terminal, non_terminal, aliases):
    s = raw.strip().lower()
    if s in terminal or s in non_terminal:
        return s
    for k, vs in aliases.items():
        if s == k or s in [v.lower() for v in vs]:
            return k
    return None

def main():
    root = find_repo_root()
    if not root:
        print("FAIL: 未找到求职仓库(向上查找 applications/tracker.md 失败);请在仓库内运行"); return 1
    tracker = root / "applications" / "tracker.md"
    today = datetime.date.today()
    non_terminal, terminal, aliases = load_states(root)
    rows = []
    for lineno, line in enumerate(tracker.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 12 or set(cells[0]) <= {"-", " ", ":"}:
            continue
        rows.append((lineno, cells))
    if rows:
        rows = rows[1:]  # 首个表行是表头
    if not rows:
        print(f"WARN {tracker} 为空表(新仓库合法状态,投出第一份申请后此警告消失)")
        return 0
    problems, due, funnel, weeks = [], [], {}, {}
    for lineno, r in rows:
        i = lineno  # 报告里的行号 = tracker.md 真实行号
        company, role, _fam, channel, jd, resume, status_raw = r[0], r[1], r[2], r[3], r[4], r[5], r[6]
        next_step, next_date = r[8], r[9]
        st = canon_status(status_raw, terminal, non_terminal, aliases)
        if not st:
            problems.append(f"L{i} {company}: 状态 '{status_raw}' 不在 states.yml(canonical 或别名)")
            continue
        for label, d in [("投递日期", r[7]), ("下一步日期", next_date)]:
            if d and d != "-" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
                problems.append(f"L{i} {company}: {label} '{d}' 不是 YYYY-MM-DD")
        if st not in terminal and (not next_step or next_step in ("-", "")):
            problems.append(f"L{i} {company}: 非终态但'下一步'为空(没有下一步的追踪表等于死表)")
        for ref in [jd, resume]:
            if ref and ref not in ("-", "") and "(未生成)" not in ref:
                if not (root / ref).exists():
                    problems.append(f"L{i} {company}: 引用文件不存在 {ref}")
        if st not in terminal and next_date and re.fullmatch(r"\d{4}-\d{2}-\d{2}", next_date):
            if datetime.date.fromisoformat(next_date) <= today:
                due.append(f"⏰ {company}·{role} [{st}] 下一步到期({next_date}): {next_step}")
        if r[7] and re.fullmatch(r"\d{4}-\d{2}-\d{2}", r[7]):
            f = funnel.setdefault(channel, [0, 0, 0, 0])
            f[0] += 1
            if st in ("responded", "interviewing", "offer"): f[1] += 1
            if st in ("interviewing", "offer"): f[2] += 1
            if st == "offer": f[3] += 1
            d0 = datetime.date.fromisoformat(r[7])
            wk = d0 - datetime.timedelta(days=d0.weekday())  # 自然周(周一起)
            weeks[wk] = weeks.get(wk, 0) + 1

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
        print("\n投递节奏(近 4 周自然周,只陈述不评判)")
        total = 0
        for k in sorted(weeks, reverse=True)[:4]:
            total += weeks[k]
            print(f"  {k} 周: {weeks[k]} 份")
        if not weeks: print("  无投递记录")
        else: print(f"  近期合计: {total} 份")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
