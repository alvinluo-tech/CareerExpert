#!/usr/bin/env python3
"""
append_fact.py — 安全增量素材录入脚本 (CareerExpert Fact Enrichment Helper)

功能：
  当用户在对话交互中提供新的项目、开源链接、作品集、证书或工作战果时，
  本脚本将素材以原子化方式写入 profile/ 事实素材库，严格遵守“事实完整性不可突破”第一红线。

用法：
  python append_fact.py project --title "FastFlow 流式引擎" --url "https://github.com/xxx/fastflow" \
         --role "个人开源作者" --dates "2024.03 ~ 2024.08" \
         --bullets "基于 Go 实现零拷贝环形队列,吞吐达 18.5万 QPS" \
         --profile-dir profile/
"""

import sys
import argparse
from pathlib import Path

def append_project(args):
    profile_dir = Path(args.profile_dir).resolve()
    projects_dir = profile_dir / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)
    
    slug = "".join([c if c.isalnum() else "-" for c in args.title.lower()]).strip("-")
    if not slug:
        slug = "project-custom"
    target_file = projects_dir / f"{slug}.md"
    
    bullets_list = [b.strip() for b in args.bullets.split(",") if b.strip()]
    bullets_md = "\n".join([f"- {b}" for b in bullets_list]) if bullets_list else "- (暂无详细描述)"
    
    content = f"""# {args.title}

- **角色**: {args.role or '核心开发者 / 负责人'}
- **时间**: {args.dates or '2024 ~ 至今'}
- **项目/仓库链接**: {args.url or '无'}
- **演示/在线体验**: {args.demo or '无'}

## 核心技术战果 (STAR / Google XYZ)
{bullets_md}
"""
    target_file.write_text(content, encoding="utf-8")
    print(f"OK 成功将新项目事实写入素材库: {target_file.relative_to(profile_dir.parent) if profile_dir.parent in target_file.parents else target_file}")
    
    # 若提供链接，检查并同步到 basic.md
    basic_file = profile_dir / "basic.md"
    if basic_file.exists() and args.url:
        basic_text = basic_file.read_text(encoding="utf-8")
        if args.url not in basic_text:
            append_text = f"\n- **开源项目/作品集**: [{args.title}]({args.url})"
            basic_file.write_text(basic_text.rstrip() + append_text + "\n", encoding="utf-8")
            print(f"OK 成功将链接同步至候选人基本信息: {basic_file}")

def main():
    parser = argparse.ArgumentParser(description="CareerExpert 增量事实写入辅助工具")
    subparsers = parser.add_subparsers(dest="subcommand", help="素材类型")
    
    p_proj = subparsers.add_parser("project", help="新增项目/作品集素材")
    p_proj.add_argument("--title", required=True, help="项目名称")
    p_proj.add_argument("--url", default="", help="代码仓库或主页链接")
    p_proj.add_argument("--demo", default="", help="在线演示或试用地址")
    p_proj.add_argument("--role", default="", help="角色与职责")
    p_proj.add_argument("--dates", default="", help="起止时间")
    p_proj.add_argument("--bullets", default="", help="战果列表，逗号分隔")
    p_proj.add_argument("--profile-dir", default="profile", help="素材库根目录")
    
    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        return 0
        
    if args.subcommand == "project":
        append_project(args)
    return 0

if __name__ == "__main__":
    sys.exit(main())
