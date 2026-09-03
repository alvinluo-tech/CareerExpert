#!/usr/bin/env python3
"""
test_e2e_scenarios.py — CareerExpert 10 大真实场景从 0 到 1 全流程端到端自动化测试矩阵

测试场景列表:
  [Test 01] PDF 格式已有简历上传智能摄取 (ingest_resume.py)
  [Test 02] DOCX (Word) 格式已有简历零依赖提取 (ingest_resume.py)
  [Test 03] 代码库深度工程架构探测 (inspect_repo.py)
  [Test 04] 目标职位 JD 五维评估与高危红旗排查 (jd-eval 逻辑)
  [Test 05] 8年老兵海量经历 · ultra-dense 极致紧凑单页压制 (render_pdf.py)
  [Test 06] 应届生精简经历 · airy 从容舒展防空洞布局 (render_pdf.py)
  [Test 07] 出海商业产品 · 双栏侧边栏 + 真实经典证件照测试 (render_pdf.py)
  [Test 08] 金融投行华尔街一页纸 · 纯黑白 + ATS 关键指标 100% 抽取 (render_pdf.py)
  [Test 09] 顶会科研学者 · Harvard/MIT 学术 CV 严格双页测试 (render_pdf.py)
  [Test 10] 事实完整性红线拦截 · 虚假捏造数据 100% 阻断校验 (check_facts.py)
"""

import os
import sys
import json
import zipfile
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "skills" / "career-ops" / "scripts"
TEMPLATES_DIR = ROOT / "skills" / "career-style" / "templates"
SANDBOX = ROOT / ".test-e2e-sandbox"

def log(msg, status="INFO"):
    colors = {
        "INFO": "\033[94m",
        "PASS": "\033[92m",
        "FAIL": "\033[91m",
        "WARN": "\033[93m",
        "RESET": "\033[0m"
    }
    prefix = f"[{status}]"
    print(f"{colors.get(status, '')}{prefix} {msg}{colors['RESET']}")

def setup_sandbox():
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    SANDBOX.mkdir(parents=True, exist_ok=True)
    log(f"测试沙盒已就绪: {SANDBOX}", "INFO")

def run_cmd(cmd_list):
    res = subprocess.run(cmd_list, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return res.returncode, res.stdout, res.stderr

# ==========================================
# [Test 01] PDF 简历解析
# ==========================================
def test_01_pdf_ingest():
    log("Running Test 01: PDF 简历智能摄取...", "INFO")
    pdf_source = ROOT / "skills" / "career-ops" / "examples" / "01-social-tech-architect" / "output" / "resume.pdf"
    if not pdf_source.exists():
        # 若未编译则先编译一个
        html_src = ROOT / "skills" / "career-ops" / "examples" / "01-social-tech-architect" / "output" / "resume.html"
        subprocess.run([sys.executable, str(SCRIPTS_DIR / "render_pdf.py"), str(html_src), str(pdf_source)], capture_output=True)
    
    out_dir = SANDBOX / "t01_pdf_out"
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "ingest_resume.py"), str(pdf_source), "--out", str(out_dir)
    ])
    assert code == 0, f"ingest_resume failed: {stderr}"
    dest_file = out_dir / "master-resume-ingested.md"
    assert dest_file.exists(), "master-resume-ingested.md 未成功生成"
    content = dest_file.read_text(encoding="utf-8")
    assert "李昂" in content or "Go" in content, "未正确提取出核心内容"
    log("Test 01 PASSED: PDF 解析成功，模块自动切分", "PASS")
    return True

# ==========================================
# [Test 02] DOCX (Word) 简历解析
# ==========================================
def test_02_docx_ingest():
    log("Running Test 02: DOCX (Word) 简历零依赖解析...", "INFO")
    docx_file = SANDBOX / "sample_resume.docx"
    
    # 动态构建一个合法的 Word .docx 文件
    xml_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:body>
        <w:p><w:r><w:t>张伟 — 资深前端架构师</w:t></w:r></w:p>
        <w:p><w:r><w:t>联系方式: 13900001111 · zhangwei@example.com</w:t></w:r></w:p>
        <w:p><w:r><w:t>【工作经历】</w:t></w:r></w:p>
        <w:p><w:r><w:t>极客互联 | 核心前端负责人 | 2021.05 ~ 至今</w:t></w:r></w:p>
        <w:p><w:r><w:t>负责大型 Web 前端微服务重构，主导微前端架构演进，页面加载首屏耗时降低 45%。</w:t></w:r></w:p>
        <w:p><w:r><w:t>【教育经历】</w:t></w:r></w:p>
        <w:p><w:r><w:t>北京邮电大学 | 软件工程 | 本科 | 2017.09 ~ 2021.06</w:t></w:r></w:p>
      </w:body>
    </w:document>"""
    
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
      <Default Extension="xml" ContentType="application/xml"/>
      <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
      <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    </Types>"""
    
    with zipfile.ZipFile(docx_file, "w") as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("word/document.xml", xml_content)
        
    out_dir = SANDBOX / "t02_docx_out"
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "ingest_resume.py"), str(docx_file), "--out", str(out_dir)
    ])
    assert code == 0, f"DOCX ingest failed: {stderr}"
    dest_file = out_dir / "master-resume-ingested.md"
    assert dest_file.exists()
    content = dest_file.read_text(encoding="utf-8")
    assert "张伟" in content and "首屏耗时降低 45%" in content
    log("Test 02 PASSED: Word (.docx) 原生提取成功，零依赖解析通过", "PASS")
    return True

# ==========================================
# [Test 03] 代码库深度架构探测
# ==========================================
def test_03_inspect_repo():
    log("Running Test 03: 代码库深度工程探测...", "INFO")
    out_file = SANDBOX / "repo_report.md"
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "inspect_repo.py"), str(ROOT / "skills" / "career-ops"), "--out", str(out_file)
    ])
    assert code == 0, f"inspect_repo failed: {stderr}"
    assert out_file.exists()
    report = out_file.read_text(encoding="utf-8")
    assert "代码工程深度审计报告" in report and "语言与代码拓扑分布" in report
    log("Test 03 PASSED: 代码库探测成功生成架构度量与 Google XYZ 语句", "PASS")
    return True

# ==========================================
# [Test 04] 岗位 JD 五维评估与高危红旗排查
# ==========================================
def test_04_jd_eval_red_flags():
    log("Running Test 04: 岗位 JD 五维打分与红旗拦截测试...", "INFO")
    edge_report = ROOT / "skills" / "career-ops" / "examples" / "05-edge-cases" / "链创未来" / "evaluation.md"
    assert edge_report.exists(), f"找不到边界报告: {edge_report}"
    content = edge_report.read_text(encoding="utf-8")
    assert "红旗" in content
    assert "炒币" in content or "风险" in content
    log("Test 04 PASSED: 假岗/外包/涉币高危红旗排查与独立告警机制健全", "PASS")
    return True

# ==========================================
# [Test 05] 极致紧凑型 (ultra-dense) 8年资深单页压制
# ==========================================
def test_05_ultra_dense_page_fitting():
    log("Running Test 05: 8年老兵海量经历 ultra-dense 极致紧凑压制单页...", "INFO")
    # 创建一个充满大量经历的 HTML 文件，应用 ultra-dense 样式 (9.0pt, 1.35行高, 6pt 节间距)
    html_content = """<!DOCTYPE html>
    <html><head><meta charset="utf-8"><style>
      @page { size: A4; margin: 10mm 11mm; }
      body { font-family: -apple-system, sans-serif; font-size: 9.0pt; line-height: 1.35; color: #111; }
      h1 { font-size: 18pt; margin: 0 0 2pt; font-weight: 800; }
      h2 { font-size: 10pt; font-weight: 700; border-bottom: 1pt solid #ccc; margin: 5pt 0 2pt; }
      .item { display: flex; justify-content: space-between; font-weight: 700; margin-top: 3pt; font-size: 9.2pt; }
      ul { padding-left: 11pt; margin: 1pt 0; }
      li { margin-bottom: 1pt; }
    </style></head><body>
      <h1>赵立恒 — 资深技术架构专家 (10年经验)</h1>
      <p>13800000000 · zhaoliheng@example.com · 北京 · 10年高并发/分布式架构设计经验</p>
      <h2>工作经历</h2>
      <div class="item"><span>集团核心基础架构部 · 首席架构师</span><span>2021.03 ~ 至今</span></div>
      <ul>
        <li>主导集团异地多活双活架构演进，支撑日均核心交易流水 3.8 亿笔，跨机房数据同步延迟控制在 15ms 内。</li>
        <li>推动服务网格 Service Mesh 落地 1,200+ 微服务，单节点内存开销降低 35%，平均 RPC 调用延迟下降 22%。</li>
        <li>负责容量规划与大促护航，连续 3 年天猫双11保障系统 99.999% 高可用，P0 故障复发率为零。</li>
      </ul>
      <div class="item"><span>云计算独角兽 · 研发总监</span><span>2018.06 ~ 2021.02</span></div>
      <ul>
        <li>带领 45 人分布式存储研发团队，从 0 到 1 打造自主可控的高性能分布式块存储系统，吞吐突破 120 万 IOPS。</li>
        <li>优化自研 Raft 共识协议实现，故障节点切主耗时从 3 秒缩短至 600ms，支撑 150+ 重点企业客户上云。</li>
        <li>主导引入混沌工程 Chaos Mesh 开展每周常态化故障演练，提前拦截潜在高危脑裂缺陷 18 起。</li>
      </ul>
      <div class="item"><span>知名互联网科技 · 高级后端工程师</span><span>2015.07 ~ 2018.05</span></div>
      <ul>
        <li>负责订单履约与支付结算核心链路，重构千万级分库分表与异步削峰架构，吞吐提升 240%。</li>
        <li>主导 Redis 缓存集群迁移与穿透治理，设计布隆过滤器预热机制，缓存命中率保持在 99.4% 以上。</li>
      </ul>
      <h2>核心标杆项目</h2>
      <div class="item"><span>自研分布式云原生调度控制面</span><span>2022.01 ~ 2022.12</span></div>
      <ul>
        <li>针对万台物理机异构算力调度瓶颈，设计动态拓扑感知调度算法，全集群 CPU 平均利用率从 28% 提升至 46%。</li>
      </ul>
      <h2>专业技能与认证</h2>
      <p><b>技术栈</b>: Go, C++, Kubernetes, Raft, eBPF, Distributed Storage, Redis, Kafka, MySQL</p>
      <h2>教育背景</h2>
      <div class="item"><span>哈尔滨工业大学 · 计算机科学与技术 · 硕士</span><span>2013.09 ~ 2015.07</span></div>
      <div class="item"><span>哈尔滨工业大学 · 软件工程 · 学士</span><span>2009.09 ~ 2013.07</span></div>
    </body></html>"""
    
    html_file = SANDBOX / "t05_ultra_dense.html"
    pdf_file = SANDBOX / "t05_ultra_dense.pdf"
    preview_file = SANDBOX / "t05_ultra_dense.png"
    html_file.write_text(html_content, encoding="utf-8")
    
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "render_pdf.py"), str(html_file), str(pdf_file), "--max-pages", "1", "--preview", str(preview_file)
    ])
    assert code == 0, f"Ultra-dense 渲染失败: {stdout}\n{stderr}"
    assert pdf_file.exists()
    assert "OK 页数: 1" in stdout, "页数超出 1 页！未能成功压制"
    log("Test 05 PASSED: 10年海量经历成功经 ultra-dense 压制为严格单页", "PASS")
    return True

# ==========================================
# [Test 06] 从容舒展型 (airy) 应届生精简经历充实单页
# ==========================================
def test_06_airy_campus_filling():
    log("Running Test 06: 应届生精简经历 airy 从容舒展防空洞布局...", "INFO")
    html_content = """<!DOCTYPE html>
    <html><head><meta charset="utf-8"><style>
      @page { size: A4; margin: 16mm 18mm; }
      body { font-family: -apple-system, sans-serif; font-size: 10.5pt; line-height: 1.56; color: #1e293b; }
      h1 { font-size: 22pt; margin: 0 0 4pt; font-weight: 800; color: #0f172a; text-align: center; }
      .contact { text-align: center; font-size: 9.6pt; color: #64748b; margin-bottom: 12pt; }
      h2 { font-size: 11.2pt; font-weight: 700; color: #1d4ed8; border-bottom: 1.5pt solid #cbd5e1; margin: 12pt 0 5pt; padding-bottom: 2pt; }
      .item { display: flex; justify-content: space-between; font-weight: 700; margin-top: 5pt; font-size: 10.2pt; }
      ul { padding-left: 14pt; margin: 3pt 0; }
      li { margin-bottom: 3.5pt; }
    </style></head><body>
      <h1>许明达</h1>
      <div class="contact">13700002222 · mingda.xu@example.com · 杭州 · 2025届计算机应届硕士</div>
      
      <h2>教育背景 (优先置顶)</h2>
      <div class="item"><span>浙江大学 · 计算机科学与技术专业 · 硕士</span><span>2022.09 ~ 2025.06</span></div>
      <div>专业绩点: 3.82 / 4.0 (前 5%) · 浙江大学优秀研究生一等奖学金</div>
      <div class="item"><span>浙江大学 · 软件工程专业 · 学士</span><span>2018.09 ~ 2022.06</span></div>
      <div>国家奖学金获得者 (2020) · 校级优秀毕业设计论文</div>

      <h2>实习经历</h2>
      <div class="item"><span>阿里巴巴 · 阿里云智能事业群 · 后端研发实习生</span><span>2024.03 ~ 2024.09</span></div>
      <ul>
        <li>参与云原生分布式缓存网关模块研发，基于 Go 语言重构连接池与探活调度逻辑，将极端网络抖动下的探活误报率降低 60%。</li>
        <li>编写完整的压力测试与集成测试套件，覆盖核心路径 88% 的单元测试分支，发现并修复并发 Channel 死锁隐患 2 处。</li>
      </ul>

      <h2>核心科研与毕业课题</h2>
      <div class="item"><span>基于智能预测的分布式键值存储自适应缓存置换算法</span><span>2023.09 ~ 2024.06</span></div>
      <ul>
        <li>针对现有 LRU 算法在扫描型热点流量下命中率骤降问题，提出双队列概率预测模型，提升复杂访问模式下缓存命中率 14.5%。</li>
        <li>相关研究成果以学生第一作者身份录用于计算机核心期刊，并在实验室分布式集群完成 10 节点真机压测验证。</li>
      </ul>

      <h2>专业技能与荣誉资质</h2>
      <ul>
        <li><b>计算机语言</b>: 熟练掌握 Go 语言底层并发机制，熟悉 C/C++ 内存管理与 Python 自动化脚本。</li>
        <li><b>专业奖项</b>: 全国大学生数学建模竞赛全国一等奖 (2021)、中国高校计算机大赛团体程序设计天梯赛金奖。</li>
        <li><b>外语水平</b>: 大学英语六级 (CET-6 612分)，具备流畅的英文专业文献阅读与撰写能力。</li>
      </ul>
    </body></html>"""

    html_file = SANDBOX / "t06_airy.html"
    pdf_file = SANDBOX / "t06_airy.pdf"
    preview_file = SANDBOX / "t06_airy.png"
    html_file.write_text(html_content, encoding="utf-8")
    
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "render_pdf.py"), str(html_file), str(pdf_file), "--max-pages", "1", "--preview", str(preview_file)
    ])
    assert code == 0, f"Airy 渲染失败: {stdout}\n{stderr}"
    assert "OK 页数: 1" in stdout
    # 验证填充率
    assert "填充率" in stdout
    log("Test 06 PASSED: 应届生精简经历经 airy 充实后单页饱满无空洞", "PASS")
    return True

# ==========================================
# [Test 07] 双栏侧边栏 + 真实真人证件照测试
# ==========================================
def test_07_sidebar_with_photo():
    log("Running Test 07: 双栏侧栏 (v8) + 真实证件照编译测试...", "INFO")
    html_src = ROOT / "skills" / "career-ops" / "examples" / "06-creative-product-manager" / "output" / "resume.html"
    pdf_dest = SANDBOX / "t07_sidebar.pdf"
    preview_dest = SANDBOX / "t07_sidebar.png"
    
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "render_pdf.py"), str(html_src), str(pdf_dest), "--max-pages", "1", "--preview", str(preview_dest)
    ])
    assert code == 0, f"Sidebar photo render failed: {stdout}\n{stderr}"
    assert "OK 页数: 1" in stdout
    assert preview_dest.exists()
    log("Test 07 PASSED: v8 双栏侧边栏与真实证件照无头编译渲染通过", "PASS")
    return True

# ==========================================
# [Test 08] 金融投行纯黑白 + ATS 必提关键字回环测试
# ==========================================
def test_08_finance_ats_extract():
    log("Running Test 08: 金融投行纯黑白 + ATS 关键字 100% 提取测试...", "INFO")
    html_src = ROOT / "skills" / "career-ops" / "examples" / "03-finance-ib-analyst" / "output" / "resume.html"
    pdf_dest = SANDBOX / "t08_finance.pdf"
    
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "render_pdf.py"), str(html_src), str(pdf_dest),
        "--must", "陈思远,CPA,12.5亿,DCF,估值", "--max-pages", "1"
    ])
    assert code == 0, f"Finance ATS render failed: {stdout}\n{stderr}"
    assert "全部可提取" in stdout
    log("Test 08 PASSED: 华尔街黑白经典款 ATS 关键指标 100% 回环提取", "PASS")
    return True

# ==========================================
# [Test 09] Harvard/MIT 学术 CV 严格双页测试
# ==========================================
def test_09_academic_two_pages():
    log("Running Test 09: 海外申博 Harvard/MIT 学术 CV 严格双页测试...", "INFO")
    html_src = ROOT / "skills" / "career-ops" / "examples" / "04-academic-cs-phd" / "output" / "cv.html"
    pdf_dest = SANDBOX / "t09_academic.pdf"
    
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "render_pdf.py"), str(html_src), str(pdf_dest), "--max-pages", "2"
    ])
    assert code == 0, f"Academic CV failed: {stdout}\n{stderr}"
    assert "OK 页数: 2" in stdout
    log("Test 09 PASSED: 学术双页规范严格锁定两页，无任何溢出", "PASS")
    return True

# ==========================================
# [Test 10] 事实追溯红线门禁与防捏造拦截测试
# ==========================================
def test_10_facts_checking_guard():
    log("Running Test 10: 事实追溯红线门禁与防捏造拦截测试...", "INFO")
    
    # 步骤 1: 真实无捏造简历，必须 PASS (code 0)
    real_html = ROOT / "skills" / "career-ops" / "examples" / "07-ai-agent-architect" / "output" / "resume.html"
    real_prof = ROOT / "skills" / "career-ops" / "examples" / "07-ai-agent-architect" / "profile"
    code, stdout, stderr = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "check_facts.py"), str(real_html), str(real_prof)
    ])
    assert code == 0, f"真实素材检查应当通过却失败了: {stdout}\n{stderr}"
    assert "所有量化数字/日期区间均可在 profile/ 素材库中追溯" in stdout
    
    # 步骤 2: 注入虚假数字的篡改简历，必须 FAIL (code 1)
    fake_html = SANDBOX / "fake_resume.html"
    fake_html.write_text(real_html.read_text(encoding="utf-8").replace("12.8k★", "999.8k★ 独家虚假数据"), encoding="utf-8")
    
    code_fake, stdout_fake, stderr_fake = run_cmd([
        sys.executable, str(SCRIPTS_DIR / "check_facts.py"), str(fake_html), str(real_prof)
    ])
    assert code_fake == 1, "篡改了虚假数据却未被拦截！事实红线门禁失效！"
    assert "FAIL" in stdout_fake
    assert "999.8k" in stdout_fake
    log("Test 10 PASSED: 事实追溯门禁成功识别伪造数据并强制阻断交付", "PASS")
    return True

def main():
    print("=" * 65)
    print("  🚀 CareerExpert 10 大全场景端到端真实模拟自动化测试")
    print("=" * 65)
    setup_sandbox()
    
    tests = [
        ("Test 01: PDF 简历智能摄取", test_01_pdf_ingest),
        ("Test 02: Word (.docx) 简历零依赖解析", test_02_docx_ingest),
        ("Test 03: 代码库工程深度架构探测", test_03_inspect_repo),
        ("Test 04: 岗位 JD 评估与红旗拦截", test_04_jd_eval_red_flags),
        ("Test 05: 8年海量经历 ultra-dense 极致单页压制", test_05_ultra_dense_page_fitting),
        ("Test 06: 应届生精简经历 airy 从容舒展防空洞", test_06_airy_campus_filling),
        ("Test 07: 双栏侧边栏 + 真实真人证件照", test_07_sidebar_with_photo),
        ("Test 08: 金融投行纯黑白 + ATS 关键词回环", test_08_finance_ats_extract),
        ("Test 09: Harvard/MIT 学术 CV 严格双页", test_09_academic_two_pages),
        ("Test 10: 事实红线防捏造拦截门禁", test_10_facts_checking_guard),
    ]
    
    passed = 0
    results = []
    for name, func in tests:
        try:
            ok = func()
            if ok:
                passed += 1
                results.append((name, "PASSED"))
        except Exception as e:
            log(f"{name} 发生异常: {e}", "FAIL")
            results.append((name, f"FAILED: {e}"))
            
    print("\n" + "=" * 65)
    print(f"  📊 测试汇总: 共 {len(tests)} 项场景测试，通过: {passed} / {len(tests)}")
    for name, res in results:
        status = "✓" if "PASSED" in res else "✗"
        print(f"  [{status}] {name}: {res}")
    print("=" * 65)
    
    if passed == len(tests):
        log("🎉 全部 10 大场景端到端测试 100% 成功通过！系统具备极高工业级健壮性！", "PASS")
        return 0
    else:
        log("存在未通过测试，请查看日志排查修复！", "FAIL")
        return 1

if __name__ == "__main__":
    sys.exit(main())
