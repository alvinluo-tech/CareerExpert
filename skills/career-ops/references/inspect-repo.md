# 代码库工程深度探测 (inspect-repo)

> 本文件是 `job-finding` 技能在**深度解析用户代码项目**时的核心参考文档，由 `SKILL.md` 按需加载；路径均相对仓库根目录。

---

## 核心目标与现实痛点解决

**痛点**：以往求职工具在处理候选人项目时，往往只读一个 README，停留在“一句话简介”或“使用说明”的皮毛，无法真正识别候选人在代码层面的核心架构能力与底层技术功底。

**解决方案**：
本工作流提供**代码工程深度探测与亮点提炼（Deep Codebase Inspection）**：
1. **真实依赖全景扫描**：解析 `go.mod`、`package.json`、`Cargo.toml`、`requirements.txt`、`pom.xml`，提取真实的生产级技术栈与中间件依赖；
2. **代码规模与拓扑度量**：计算代码行数（LOC）、主导语言分布、测试代码占比（Test Coverage Ratio）；
3. **架构与底层并发模式挖掘**：基于代码 AST 与模式检索，探查协程池、Channel 通信、分布式锁、数据库显式事务、限流算法、缓存预刷盘等高价值工程实现；
4. **输出《代码工程深度审计报告》**：自动沉淀至 `profile/projects/<项目名>.md`，生成具有**代码级真实证据支撑**的 Google XYZ 简历 Bullet。

---

## 一、 执行流水线

```mermaid
graph LR
    A[用户输入项目路径\n本地目录 或 GitHub URL] --> B[运行 inspect_repo.py 扫描依赖/代码/并发]
    B --> C[生成《代码工程技术深度审计报告》]
    C --> D[提炼代码级 Google XYZ 成果 Bullet]
    D --> E[沉淀至 profile/projects/<项目名>.md]
```

### 步骤 1：探测代码库
- **本地项目**：
  ```bash
  python .agents/skills/job-finding/scripts/inspect_repo.py "<本地项目绝对或相对路径>" --out profile/projects/<项目名>.md
  ```
- **远程 GitHub 项目**：
  若用户提供 GitHub 链接（如 `https://github.com/username/my-repo`），AI 可通过 Git 浅克隆至临时目录后运行探测：
  ```bash
  git clone --depth 1 https://github.com/username/my-repo .tmp_repo
  python .agents/skills/job-finding/scripts/inspect_repo.py .tmp_repo --out profile/projects/<项目名>.md
  rm -rf .tmp_repo
  ```

---

## 二、 提炼代码级简历 Bullet 标准 (Code Evidence to XYZ)

AI 依据探测报告，将代码特征转化为高冲击力简历语句：

| 探测到的底层代码证据 | 传统平庸写法 (❌ 严禁) | 基于代码证据的 Google XYZ (✅ 标准) |
|---|---|---|
| `go.mod` 含有 `FastHTTP`，代码包含 `sync.Pool` 内存对象池 | “使用 Go 语言重写了网关” | **基于 Go 语言从零自研高性能反向代理网关 [Z]**，引入 `sync.Pool` 内存对象复用与 FastHTTP 零内存拷贝解析 [Z]，**将系统 P99 延迟由 45ms 压缩至 18ms，平稳承载单机 6.5 万 QPS 峰值流量 [X+Y]**。 |
| 检测到 `sarama.NewConsumerGroup` 与 Redis 缓存 | “负责消息队列和缓存开发” | **设计双层缓存与异步解耦消费架构 [Z]**，运用 Kafka 消费组批量拉取与 Redis 预热机制 [Z]，**削减数据库峰值负载 70%，消息处理吞吐提升 3 倍 [X+Y]**。 |
| 测试代码占比 > 25%，检测到混沌故障注入代码 | “编写了单元测试” | **主导编写端到端混沌故障注入测试套件 [Z]**，模拟网络分区、磁盘静默损坏等 8 类极端异常场景 [Z]，**测试代码占比逾 30%，保障核心集群在 100+ 次极限故障注入中数据零丢失 [X+Y]**。 |

---

## 三、 防翻车与归属自查提醒

每次审计完成后，必须在项目卡顶部明确标注：
- 代码仓库可公开访问的 GitHub 地址或本地路径；
- 提示用户确认：**该代码确为本人独立编写或主导的核心成果**，严禁使用他人开源代码充数，避免技术面试被要求现场打开 GitHub 或白板撕底层函数时被当场揭穿。
