# 官方基准实操案例 01：FastFlow 高并发流式引擎与统一网关 (字节跳动中间件专家方向)

> **场景**：社招资深架构师李昂在简历中补充了开源流式计算引擎 FastFlow（18.5万 QPS、零拷贝、1.2k★）。  
> **痛点**：高硬核指标极易在面试中招致考官连环拷打（“怎么测的？Payload 多大？Cache 伪共享怎么解决？自研 ROI 怎么算？”）。  
> **方案**：运行 `/career-coach` 生成本专属掌握手册，并在浏览器中自动打开供求职者系统性复习。

---

## 交付文件清单
1. `data.json`：包含经历排雷、底层原理清单、STAR-T 思考模型与连环追问解析的结构化数据；
2. `output/fastflow-mastery-guide.html`：自包含纯静态高质感 Web 手册（支持浏览器直接打开、支持打印导出）；
3. `output/fastflow-mastery-guide.md`：结构化 Markdown 文档，支持离线纯文本速查与 Git 审计。

## 复现命令
```bash
python skills/career-coach/scripts/render_guide.py \
  skills/career-coach/examples/01-fastflow-middleware-guide/data.json \
  --out skills/career-coach/examples/01-fastflow-middleware-guide/output/fastflow-mastery-guide.html \
  --open
```
