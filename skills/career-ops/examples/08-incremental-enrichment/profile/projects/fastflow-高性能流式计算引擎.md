# FastFlow 高性能流式计算引擎

- **角色**: 独立设计者与核心作者
- **时间**: 2024.03 ~ 至今
- **项目/仓库链接**: https://github.com/leon-tech/fastflow
- **演示/在线体验**: https://fastflow.dev/demo

## 核心技术战果 (STAR / Google XYZ)
- 主导基于 Go 语言研发轻量级低延迟流式计算中间件
- 设计无锁环形队列 (Lock-Free RingBuffer) 与零拷贝通道
- 单节点压测极限吞吐达 18.5万 QPS
- 端到端传输延迟由 45ms 降至 4.2ms
- 相比传统流式框架内存降低 42%
- 单机支持 8000+ 虚拟流通道
- 开源收获 1.2k★ 与 140+ Forks
