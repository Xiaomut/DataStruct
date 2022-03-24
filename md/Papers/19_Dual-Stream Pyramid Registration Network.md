## Dual-Stream Pyramid Registration Network


> 这篇论文结构图很清晰了，就是根据Unet构造整的，有个小小疑惑的地方就是文中说权值是共享的，但是看这图又是分开输入的（个人认为图只是这样画了，不影响原文的表述），有机会了试试写一下代码

### 1. 介绍

- 设计了一种双流编解码器网络，能够从一对输入量单独计算两个卷积特征金字塔，从而获得更强的深度表示来估计多级变形。
- 提出一个金字塔配准模块，直接从卷积特征估计配准域，得到一组分层的配准域，通过顺序扭曲卷积特征编码多层次的上下文信息。这使得模型能够处理显著的变形。


### 2. Dual-Stream Pyramid Registration Network

- 用于计算特征金字塔的双流编解码器网络
- 在解码过程中估计分层配准域的金字塔配准模块


<p align="center"><img src="https://img-blog.csdnimg.cn/5dcf738ab0b64bec9e8c3fa0b689098a.png" 
width="60%"\></p>

#### 2.1 Preliminaries

以 `VoxelMorph` 为例做了个介绍，略

#### 2.2 Dual-Stream Architecture

- 双流编解码器参数共享
- 编码器结构采用 [VoxResNet](https://github.com/bo-10000/pytorch_3d_segmentation)。编码器包含四个下采样卷积块。每个块有一个步长为2的3D下采样卷积层。因此，编码器将输入体积的空间分辨率总共降低了16倍。除第一个块外，下采样卷积层后面是两个resblock，每个resblock包含两个卷积层，其中有一个残差连接，类似于ResNet。采用BN和ReLU操作。
- 在解码阶段，我们在编码和解码过程中对相应的卷积映射应用跳层连接。通过使用1×1×1卷积层，将低分辨率卷积地图上采样并添加到高分辨率地图中，使用Refine Unit将这些特征融合在一起。最后，分别从浮动图像和参考图像得到两个具有多分辨率卷积特征的特征金字塔。


#### 2.3 Pyramid Registration Module

在解码过程中，`VoxelMorph` 从最后上采样层的卷积特征计算单个变形场，限制了其处理大规模变形的能力。我们的金字塔配准模块能够预测不同分辨率的多个变形场，并生成金字塔变形场。每个解码层利用一对卷积特征计算出一个变形场，因此可以得到多个变形场（网络包含4个）


第一层解码器输出得到第一个形变场 ($Φ_1$) ，随后采用双线性插值对形变场进行2倍上采样，记为 $u(Φ_1)$，下一层的浮动图像经过其变形得到配准图像，再与参考图像stack后进行卷积，得到下一个形变场...不断重复，最后得到的形变场即为最终的形变场

#### 3. 实验结果与比较

Datasets: LPBA40
Experimental Settings: 160×192×160

比较就说好，放个图和数据完事...


#### 4. 论文
[1] Hu X ,  Kang M ,  Huang W , et al. Dual-Stream Pyramid Registration Network[J]. Springer, Cham, 2019.

#### To Be Continued...