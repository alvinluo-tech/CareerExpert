# 学术项目卡：SparseSplat 稀疏视角高保真三维神经辐射场渲染引擎

- 时间：2023.03 ~ 2024.04
- 角色：第一作者 / 核心算法设计与 CUDA 算子实现
- 依托成果：CVPR 2024 Oral 顶会论文
- 代码仓库与开源路径：
  - 公开 GitHub 仓库：`https://github.com/guowei-research/sparse-splat-core` (650+ Stars, Fork 110+)
  - 本地研究代码：`E:/research/sparse-splat-core`
  - 真实性与归属声明：核心深度可微前向与反向传播 CUDA Kernel、自适应视锥剔除与球谐函数重构代码全部由本人独立编写，支持学术面试白板推导公式与推演梯度。

## 核心科学问题与学术突破
- **挑战**：传统 3D Gaussian Splatting (3DGS) 高度依赖数十张密集视角照片，当输入图像减少至 3~5 张稀疏视角时，由于缺乏足够几何几何约束，重建结果会产生极严重的结构坍塌与伪影。
- **创新点与突破**：
  1. 提出首个几何先验自监督流场约束（Geometry-guided Flow Prior），将稀疏多视角外极线几何投影显式引入高斯体素优化过程；
  2. 手写定制化 CUDA 反向传播算子，对各向异性三维高斯协方差矩阵求导进行了紧凑矩阵化重构，GPU 显存占用下降 52%，训练收敛提速 3.8 倍；
  3. 在 Synthetic NeRF 与 Tanks&Temples 标准基准数据集上，稀疏 3 视角渲染质量达到 28.6 dB PSNR，以绝对优势刷新 SOTA。

## 关键词
`3D Computer Vision` `Neural Rendering` `Gaussian Splatting` `CUDA` `CVPR Oral`
