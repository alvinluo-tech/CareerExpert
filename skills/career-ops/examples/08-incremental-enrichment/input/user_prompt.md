# 场景设定：用户交互指令 (User Refinement Prompt)

> 用户在对话中发送了以下消息，并上传了原简历 `input/base_resume.pdf` 与目标 JD：

```markdown
你好，这是我之前生成的简历 PDF（已上传）。
最近我在业余主导开发了一个高性能流式数据引擎开源项目叫 **FastFlow**：
- GitHub 仓库：`https://github.com/leon-tech/fastflow`
- 在线演示 Demo：`https://fastflow.dev/demo`
- 个人技术专栏：`https://leon.tech/posts/fastflow-internals`
- 核心指标与事实：
  - 基于 Go 语言原生实现零拷贝环形缓冲区 (RingBuffer)，单节点压测吞吐量达 18.5万 QPS，P99 延迟由 45ms 骤降至 4.2ms；
  - 内存开销较主流流式框架降低 42%，单机支撑 8,000+ 虚拟流通道；
  - 获得 GitHub 1,200+ Stars (1.2k★) 与 140+ 社区 Forks。

现在我想投递【字节跳动 — 基础架构部 · 高并发流媒体与分布式中间件专家】岗位（JD 见 input/target_jd.md）。
要求：
1. 帮我把 FastFlow 项目和上述链接增量补充进简历，突出高并发、流式处理和零拷贝性能优化；
2. 链接在 PDF 里要能正常点击，排版不要丑陋生硬；
3. 严格控制为 A4 单页纸，保持黄金呼吸感，绝不能溢出到第二页；
4. 给我一份 Before vs After 的优化对比报告，告诉我修改点和理由。
```
