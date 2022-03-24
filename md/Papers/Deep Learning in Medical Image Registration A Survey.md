##  配准综述


### 1. INTRODUCTION

&emsp;&emsp;图像配准是将不同的图像数据集转换成具有匹配图像内容的一个坐标系统的过程，可以是不同时间图像的配准，可以是多模态配准，可以是不同空间的配准。这些图像之间的空间关系可能是刚性变换（平移和旋转）与非刚性变换（包含仿射和缩放）。在医学领域有着重要的应用，如图像融合、器官图谱创建、肿瘤生长监测等临床任务。当分析一对从不同角度、不同时间或不同模态的图像时，配准可能是必要的。配准是一个非常具有挑战性的问题。

&emsp;&emsp;总之，深度学习的发展很快，大多数研究都是基于深度学习


### 2. Deep Iterative Registration

两种方法:
- `2.1` 介绍早期基于相似度的配准
- `2.2` 介绍基于强化学习的配准

```py
# 基于强度的配准框架的直接扩展（个人计划大致阅读的paper）
[1] Simonovsky M , B Gutiérrez-Becker,  Mateus D , et al. A Deep Metric for Multimodal Registration[C]// International Conference on Medical Image Computing and Computer-Assisted Intervention. Springer, Cham, 2016.
[2] Wu G ,  Kim M ,  Qian W , et al. Scalable High-Performance Image Registration Framework by Unsupervised Deep Feature Representations Learning[J]. Deep Learning for Medical Image Analysis, 2016, 63(7):245-269.
```

#### 2.1 Deep Similarity based Registration
<div align="center"><img src="https://img-blog.csdnimg.cn/0d5ae757cfd148b7891ef68015e02e5b.png
" width="60%" alt=""></div>

`Scalable High-Performance Image Registration Framework by Unsupervised Deep Feature Representations Learning` 基于`diffomorphic demons` 和 `HAMMER` 的配准技术

    `Demons` 就是一种著名的非参数化可形变配准方法。它最早来自于光流算法 (optical flow)，光流是用来估计视频图像中相邻的两帧图像目标的位移，也就是目标移动的速度。配准的能量函数包括相似性测度和对位移场的平滑化限制 （来源于[图像可形变配准的Demons方法](https://blog.csdn.net/taigw/article/details/53373400)）


`Combining mrf-based deformable
registration and deep binary 3d-cnn descriptors for large lung motion estimation
in copd patients.` 表明在单模态配准情况下，深度学习可能并不优于手工方法。但是，它可以用来获得互补的信息。

将深度学习应用于基于强度的配准的优势在多模态情况下更加明显，在这种情况下，人工制作的相似度度量几乎没有成功。

```py
[1] Cheng X ,  Zhang L ,  Zheng Y . Deep similarity learning for multimodal medical images[J]. Computer methods in biomechanics and biomedical engineering. Imaging & visualization, 2018.
```


最近的工作证实了神经网络在多模态医学图像配准中评估图像相似度的能力。本节描述的方法所取得的结果表明，深度学习可以成功地应用于具有挑战性的注册任务。然而，`Combining ……` 的研究结果表明，在单模态情况下，学习的图像相似性度量可能最适合补充现有的相似性度量。此外，这些迭代技术很难用于实时配准。

#### 2.2 Reinforcement Learning based Registration

略

### 3. Supervised Transformation Estimation

尽管前面描述的方法在早期取得了成功，但这些方法中的变换估计是迭代的，这可能导致配准慢的问题。[36]。在解空间为高维[59]的可变形配准情况下尤其如此。这激发了网络的发展，它可以一步估计出与最优相似度相对应的变换。



两种方法:
- `3.1` 全监督
- `3.2` 双监督/弱监督

#### 3.1 Fully Supervised Transformation Estimation

Miao，AirNet（这篇咨询了原论文作者一些问题，主要还是数据的差异吧），Loss采用测地距离（已复现pytorch的代码）……

<div align="center"><img src="https://img-blog.csdnimg.cn/8d0eab536f8b43e3b2bb2241dfb136ab.png
" width="60%" alt=""></div>

```py
[1] Sloan J M ,  Goatman K A ,  Sie Be Rt J P . Learning Rigid Image Registration - Utilizing Convolutional Neural Networks for Medical Image Registration[C]// International Conference on Bioimaging. 2018.
```

**确保模拟数据与临床数据足够相似**

#### 3.2 Dual/Weakly Supervised Transformation Estimation

`Dual supervision` 是指利用真实标签和一些量化图像相似度的度量来训练模型。`weak supervision` 是指利用相应解剖结构的节段重叠来设计损失功能。

<div align="center"><img src="https://img-blog.csdnimg.cn/bdf5456ec4f843d4b000da52fdc7f72b.png
" width="60%" alt=""></div>


### 4. Unsupervised Transformation Estimation


获得可靠的GT仍然是一个重大的挑战，这促使无监督的方法的探索和发展。使用STN来执行与其配准应用相关的变形

#### 4.1 Similarity Metric based Unsupervised Transformation Estimation

<div align="center"><img src="https://img-blog.csdnimg.cn/011c05e290a34cbfa66b7973e5543563.png
" width="60%" alt=""></div>

大多是 `FCN/Unet`，损失函数大多是 `MSE` 或 `NCC+正则损失`，后来 `GAN` 网络也开始疯狂卷了，看的几篇论文中应该是 `cycleGAN` 更牛b一些。

基于图像相似度的无监督图像配准最近受到了研究界的广泛关注，因为它不需要GroundTruth。这意味着模型的性能将不依赖于专业知识。此外，对基于相似度的原始方法进行了扩展，引入了更复杂的相似度度量(例如GAN的判别器)和正则化策略等。然而，在多模态配准应用中，图像相似度的量化仍然是一个难题。因此，基于图像相似度的无监督作品的范围很大程度上局限于单模态情况。鉴于在许多临床应用中经常需要多模态配准，我们希望在不久的将来看到更多的论文来解决这个具有挑战性的问题。


#### 4.2 Feature based Unsupervised Transformation Estimation

使用学习到的特征表示来训练神经网络的方法。

<div align="center"><img src="https://img-blog.csdnimg.cn/6dc68ec7a87f4fafb24b1b4259dd351b.png
" width="60%" alt=""></div>


### 5. Research Trends and Future Directions

对于深度学习在医学图像分析中的普遍应用，基于深度学习的医学图像配准似乎遵循了观察到的趋势（深度学习越来越可）。其次，无监督变换估计方法最近受到了学术界的更多关注。此外，基于深度学习的方法始终优于传统的基于优化的技术

#### 5.1 Deep Adversarial Image Registration

我们进一步推测 `GAN` 将在未来几年更频繁地用于基于深度学习的图像配准。如上所述，`GAN` 在基于深度学习的医学图像配准中可以满足几个不同的目的: <u>使用判别器作为学习的相似性度量，确保预测的变换是真实的，并使用 `GAN` 执行图像平移，将多模态配准问题转化为单模态配准问题</u>。

尽管训练形式借鉴了无监督训练策略，但判别器需要预先对齐的图像对。因此，它在多模态或具有挑战性的单模态应用中取得的成功有限，因为这些应用很难配准图像。因为判别器可能被训练的分配所有的错位图像对为相同的标签（尝试过，确实是判别器一眼就瞄出你是猫猫里的哈士奇，直接干碎生成器）。

不受约束的形变场预测可能导致扭曲的运动图像与不切实际的器官外观。一种常见的方法是<u>将预测变形场的L2范数、梯度或拉普拉斯算子添加到损失函数中</u>。然而，使用这种正则化术语可能会限制神经网络能够预测的变形的大小。因此，Hu等人探索了使用 `GAN` 框架来产生真实的变形。<u>使用判别器约束变形预测的结果优于在该工作中使用L2范数正则化</u>。

#### 5.2 Reinforcement Learning based Registration（不是我的关注点...）

我们还预计，强化学习在未来几年也将更普遍地用于医学图像注册，因为它非常直观，可以模仿医生进行配准的方式。需要指出的是，基于深度学习的医学图像配准存在一些独特的挑战: 包括变形配准案例中动作空间的维数。然而，我们认为这些限制是可以克服的，因为已经有一种提出的方法使用基于强化学习的配准与变形变换模型。

#### 5.3 Raw Imaging Domain Registration

本文主要研究利用重建图像进行配准的测量方法。然而，我们推测，将重建纳入基于深度学习的端到端配准是可能的。2016年，Wang[107]假设可以使用深度神经网络进行图像重建。此外，一些研究[85,98,115,120]最近展示了深度学习将原始数据域的数据点映射到重建图像域的能力。因此，有理由期待以原始数据作为输入和输出配准、重建图像的配准框架在未来几年内能够发展起来。