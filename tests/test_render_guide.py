#!/usr/bin/env python3
"""
test_render_guide.py — 单元测试：render_guide.py 渲染与模板拼装测试
"""

import sys
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "career-coach" / "scripts" / "render_guide.py"

def test_render_guide():
    data = {
        "title": "李昂 — FastFlow 核心掌握手册",
        "candidate_name": "李昂",
        "target_role": "字节跳动·中间件专家",
        "gen_date": "2026-09-03",
        "stats_summary": "3项漏洞排查 · 3套思考模型 · 5组追问",
        "vulnerabilities": [
            {
                "title": "单节点 18.5万 QPS 指标真实性考验",
                "quote": "单节点压测极限吞吐达 18.5万 QPS",
                "subtext": "考官必问机器规格、消息大小与压测工具，空跑无意义。"
            }
        ],
        "technical_grounding": [
            {
                "title": "无锁队列 Cache Line 对齐",
                "content": "避免 CPU 伪共享 (False Sharing)，使用 64 字节 padding。",
                "bullets": ["对齐生产消费指针", "避免 CPU 缓存失效跨核同步"]
            }
        ],
        "mental_models": [
            {
                "title": "STAR-T 高段位答辩模型",
                "steps": [
                    {"name": "定边界", "desc": "主动讲清机器规格与 Payload"},
                    {"name": "说权衡", "desc": "解释为何不直接用现有开源库"},
                    {"name": "提局限", "desc": "指出当前瓶颈与下一步演进路线"}
                ]
            }
        ],
        "deep_dive_qa": [
            {
                "question": "Q1: 18.5万 QPS 压测时的 CPU 瓶颈在哪？如何排查？",
                "intent": "考察真实动手压测与性能调优工具链掌握度",
                "answer": "使用 pprof 采样发现 Channel 锁竞争，改用无锁 CAS 后解除锁等待..."
            }
        ]
    }
    
    test_json = ROOT / ".test_guide_input.json"
    test_out = ROOT / ".test_guide_output.html"
    test_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    try:
        res = subprocess.run([
            sys.executable, str(SCRIPT), str(test_json), "--out", str(test_out)
        ], capture_output=True, text=True, encoding="utf-8")
        assert res.returncode == 0, f"render_guide failed: {res.stderr}\n{res.stdout}"
        assert test_out.exists(), "Output HTML was not created"
        content = test_out.read_text(encoding="utf-8")
        assert "李昂" in content
        assert "18.5万 QPS" in content
        assert "STAR-T 高段位答辩模型" in content
        print("OK test_render_guide PASSED")
    finally:
        if test_json.exists():
            test_json.unlink()
        if test_out.exists():
            test_out.unlink()

if __name__ == "__main__":
    test_render_guide()
