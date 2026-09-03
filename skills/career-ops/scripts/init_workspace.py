#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_workspace.py — 一键初始化求职工作区骨架
用法:
    python scripts/init_workspace.py [目标路径]
    若未指定路径，默认在当前工作目录下初始化。
"""

import os
import sys
import shutil
from pathlib import Path

def init_workspace(target_dir: str = "."):
    dest = Path(target_dir).resolve()
    skill_root = Path(__file__).resolve().parent.parent

    print(f"[*] 正在为求职工作区创建骨架: {dest}")

    # 1. 创建核心目录树
    directories = [
        dest / "profile" / "projects",
        dest / "profile" / "work",
        dest / "jds",
        dest / "resumes" / "base",
        dest / "resumes" / "tailored",
        dest / "applications" / "interviews",
        dest / "applications" / "decisions",
        dest / "applications" / "reports",
    ]

    for d in directories:
        d.mkdir(parents=True, exist_ok=True)
        # 添加 .gitkeep 保持空目录追踪
        gitkeep = d / ".gitkeep"
        if not gitkeep.exists() and not any(d.iterdir()):
            gitkeep.write_text("# keep empty folder\n", encoding="utf-8")

    # 2. 复制模板文件
    templates_dir = skill_root / "templates"
    ws_templates = templates_dir / "workspace"

    copy_tasks = [
        (ws_templates / "profile" / "master-resume.template.md", dest / "profile" / "master-resume.md"),
        (ws_templates / "profile" / "star-bank.template.md", dest / "profile" / "star-bank.md"),
        (ws_templates / "profile" / "projects" / "_template.md", dest / "profile" / "projects" / "_template.md"),
        (ws_templates / "profile" / "work" / "_template.md", dest / "profile" / "work" / "_template.md"),
        (templates_dir / "tracker.template.md", dest / "applications" / "tracker.md"),
        (templates_dir / "states.yml", dest / "applications" / "states.yml"),
        (ws_templates / "config.yml.example", dest / "config.yml.example"),
        (ws_templates / "config.yml.example", dest / "config.yml"),
    ]

    for src, dst in copy_tasks:
        if src.exists() and not dst.exists():
            shutil.copyfile(src, dst)
            print(f"  [+] 创建: {dst.relative_to(dest)}")

    # 3. 辅助 README 说明
    jds_readme = dest / "jds" / "README.md"
    if not jds_readme.exists():
        jds_readme.write_text(
            "# jds/ — 目标职位 JD 库\n\n"
            "将目标职位的 JD 原文逐字保存于此目录（或让 AI 自动录入）。\n"
            "建议命名格式: `YYYY-MM-DD-<公司>-<岗位>.md`\n",
            encoding="utf-8"
        )

    resumes_readme = dest / "resumes" / "README.md"
    if not resumes_readme.exists():
        resumes_readme.write_text(
            "# resumes/ — 简历交付包库\n\n"
            "- `base/`: 各岗位族基准版简历\n"
            "- `tailored/<公司>/`: 针对具体公司的定制独立交付包（含 HTML、PDF、改写报告）\n",
            encoding="utf-8"
        )

    # 4. 完成提示
    print("\n" + "=" * 55)
    print("  ✨ 求职工作区初始化成功！")
    print("  推荐下一步操作：")
    print("  1. 导入已有简历：")
    print(f"     python {skill_root / 'scripts' / 'ingest_resume.py'} <你的简历.pdf/.docx/.tex>")
    print("  2. 深入扫描你的本地/GitHub代码项目：")
    print(f"     python {skill_root / 'scripts' / 'inspect_repo.py'} <你的代码路径>")
    print("  3. 评估职位 JD 并定制简历：")
    print("     把 JD 发给 AI，即可自动评估打分并生成针对性高质感简历！")
    print("=" * 55)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    init_workspace(target)
