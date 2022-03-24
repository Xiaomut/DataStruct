# STN

- [STN](https://zhuanlan.zhihu.com/p/358928845)

## 1. 介绍


&emsp;&emsp;平移不变性，对于CNN来说，如果移动一张图片中的物体，那应该是不太一样的。假设物体在图像的左上角，我们做卷积，采样都不会改变特征的位置，糟糕的事情在我们把特征平滑后接入了全连接层，而全连接层本身并不具备 平移不变性 的特征。但是 CNN 有一个采样层，假设某个物体移动了很小的范围，经过采样后，它的输出可能和没有移动的时候是一样的，这是 CNN 可以有小范围的平移不变性的原因。

<div align="center"><img src="https://pic2.zhimg.com/v2-a9b90fe03d8b5fa57ba52fb1657c49d9_r.jpg
" width="60%" alt=""></div>

|||
|:--------:|:--------:|
|参数预测：|Localisation net|
|坐标映射：|Grid generator|
|像素点采集：|Sampler|

<!-- <div><tbody><tr><td>参数预测：</td><td>Localisation net</td></tr><tr><td>坐标映射：</td><td>Grid generator</td></tr><tr><td>像素点采集：</td><td>Sampler</td></tr></tbody></div> -->



## 2. Localisation Net 如何实现参数的选取

### 2.1 平移
### 2.2 缩放
### 2.3 旋转
### 2.4 剪切

## 3. Grid generator 实现像素点坐标的对应关系

### 3.1 坐标的问题

经过变换 $T_\theta(G)$ , $\theta$ 是上一个部分（Localisation net）生成的参数，生成了图片 $V\in ^{H'xW'xC}R$ ，它的像素相当于被贴在了图片的固定位置上，用 $G=G_i$ 表示，像素点的位置可以表示为 $G_i = \{x_i^t, y_i^t\}$ 这就是我们在这一阶段要确定的坐标。

### 3.2 仿射变换关系

坐标的映射关系是从目标图片映射到输入图片上的。坐标映射的作用，其实是让目标图片在原图片上采样，每次从原图片的不同坐标上采集像素到目标图片上，而且要把目标图片贴满，每次目标图片的坐标都要遍历一遍，是固定的，而采集的原图片的坐标是不固定的，因此用这样的映射。

## 4. Sampler实现坐标求解的可微性

### 4.1 小数坐标问题的提出


假如权值是小数，拿得到的值也一定是小数，1.6,2.4，但是没有元素的下标索引是小数呀。如果取最近的话不能用梯度下降法求解。

梯度下降是一步一步调整的，而且调整的数值都比较小，哪怕权值参数有小范围的变化，虽然最后的输出也会有小范围的变化，比如一步迭代后，结果有：$1.6→1.64 2.4→2.38$。但是即便这样，结果依然是：$a_{22}^{l-1} \rightarrow a_{22}^l$  的对应关系没有一点变化，所以output依然没有变，我们没有办法微分了，也就是梯度依然为0呀，梯度为0就没有可学习的空间呀。所以我们需要做一个小小的调整。

计算一下输出的结果与他们的下标的距离

<div align="center"><img src="https://img-blog.csdnimg.cn/84a2bcf551184e52b41f594193c15e46.jpg
" width="40%" alt=""></div>

<div align="center"><img src="https://img-blog.csdnimg.cn/bc3dd8c69ef54e538b32e61eb5d5e93d.png
" width="40%" alt=""></div>

他们对应的权值都是与结果对应的距离相关的，如果目标图片发生了小范围的变化，这个式子也是可以捕捉到这样的变化的，这样就能用梯度下降法来优化了。

### 4.2 Sample的数学原理

每次变换相当于从 $(x_i^s, y_i^s)$ 中，经过仿射变换，确定目标图片的像素坐标 $(x_i^t, y_i^t)$ 的过程，这个过程可以用公式表示为：

<div align="center"><img src="https://img-blog.csdnimg.cn/5cf6f09f891746a1bd5e167fde9b8053.png
" width="60%" alt=""></div>

如果利用双线性插值，可以有：

<div align="center"><img src="https://img-blog.csdnimg.cn/83c8acfde5e344ddae7a92a9d91a1de3.png
" width="60%" alt=""></div>

公式含义：在图像中双线性插值一般都在矩阵形状的相邻四个点，对于双线性插值函数：
<div align="center"><img src="https://img-blog.csdnimg.cn/2ce692d0c5f147afaea52055355f432f.png
" width="50%" alt=""></div>

可以化简到上式 $max(0, 1 - |x_i^s - m|)$ 主要是为了限制在值在 $[0, 1]$ ，即限制在边长为1的像素矩阵中。

为了允许反向传播，回传损失，对该函数求导：

<div align="center"><img src="https://img-blog.csdnimg.cn/99a60063333e430ba43a4604cd7b07f4.png
" width="50%" alt=""></div>

$Localisation Net \leftarrow  Grid generator \leftarrow Sampler$ 的梯度就可以走通了

## 5.  Spatial Transformer Network

这个Spatial Transformer就可以添加到神经网络的任意位置，这种逆向计算需要的算力也比较小。显性的完成网络的各种旋转放缩变换。