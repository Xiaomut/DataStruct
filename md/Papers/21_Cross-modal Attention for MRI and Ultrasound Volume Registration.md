## Cross-modal Attention for MRI and Ultrasound Volume Registration 论文

- [https://github.com/DIAL-RPI/Attention-Reg](https://github.com/DIAL-RPI/Attention-Reg) 非完整代码，里面有很多细节并未展现

### 1. 介绍

提出了一种新的跨模态注意机制，明确地使用空间对应来提高神经网络的图像配准性能。将非局部注意机制扩展到两幅图像之间的注意操作。注意块能够有效地捕捉局部特征和它们的全局对应关系。如图1所示，将该跨模态注意块嵌入到图像配准网络中，改进了基于深度学习的多模态图像配准，实现了特征学习和对应关系的明确协同建立。

<div align="center"><img src="assets/cross_model attention block.png" width="70%"></div>

通过添加跨模态特征对应，图像配准网络可以以更简单的结构实现更好的配准性能。据我们所知，这是第一个将非局部注意嵌入到深度神经网络中进行图像配准的工作。在我们的实验中，我们展示了所提出的方法在三维核磁共振图像融合任务，这是一个非常具有挑战性的交叉模态图像配准问题。该网络在650个MRI和TRUS体积对数据集上进行训练和测试。结果表明，该网络能将配准误差从10.17±5.75mm降低到3.71±1.99mm。该方法的性能也优于目前最先进的方法，参数数仅为竞争对手的1/10到1/5，并且显著缩短了运行时间。

### 2. 方法

<div align="center"><img src="assets/cross model structure.png" width="70%"></div>

- 配准网络
    - 特征提取网络(卷积和最大池化)
    - 注意块
    - 全连接层

That inspired us to re-place the MRI volume with the prostate segmentation label volume in our work. The network remains the same and we only need to set the fixed image input as either MRI volume or segmentation label. 

该方法以两篇论文为基准，均使用Adam优化器，300个epoch训练网络
- MSReg
    - lr: 5e-5, decays to 0.9 every 5 epochs
    - batch size: 16
- DVNet
    - lr: 1e-3
- Attention Reg
    - batch size: 8

### 3. 结果

<div align="center"><img src="assets/att-reg res.png" width="70%"></div>

在本研究中，我们使用了528例MRI-TRUS容量对进行训练，66例进行验证，68例进行测试。每个病例包含一个t2加权MRI容积和一个3D超声容积。每个MRI体积具有512×512×26体素，各方向分辨率为0.3mm。超声重建从电磁跟踪徒手二维扫描前列腺。每个训练历元重新生成训练集，以提高模型的鲁棒性。相反，验证集由每个情况的5个预先生成的初始化矩阵组成，总共有330个样本。没有在每个epoch都重新生成新的验证集的原因是为了以更稳定的方式监控epoch到epoch的性能。为了测试，我们为每种情况生成了40个随机初始化矩阵。所有的实验都使用相同的测试集。

利用 `表面配准误差(SRE)` 测量图像配准性能。为了准确地生成一个已知SRE的数据集进行训练和验证，我们在5mm平移或6度旋转范围内随机扰动每个ground truth变换参数，然后将扰动缩放到所需范围内的随机SRE。

为了证明交叉模态注意块的作用，我们在没有注意块的情况下训练我们的attention - reg网络，即，直接连接特征提取模块的输出，并将其反馈给深度配准模块。结果显示在表2的下半部分，这证明了所提出的交叉模态注意块的重要性。在没有注意模块的情况下，两种设置下的配准性能均显著降低(p <0.001，配对t检验)。此外，需要注意的是，在没有注意块的情况下，使用分割标签作为固定图像不再比MRI体积有优势。我们推测这也是由于注意力阻滞的缺失造成的，这在MRI分割和超声体积之间建立了一种合理的空间相关性，如图4所示。


