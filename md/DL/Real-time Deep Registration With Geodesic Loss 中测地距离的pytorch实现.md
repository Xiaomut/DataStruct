## Real-time Deep Registration With Geodesic Loss 中 Loss 的 pytorch 实现

#### 1. pytorch实现
Paper: Real-time Deep Pose Estimation with Geodesic Loss for Image-to-Template Rigid Registration

该论文采用网络回归刚性配准的参数，主要借鉴其loss函数。[源码链接](https://github.com/SadeghMSalehi/DeepRegistration)


<div align="center"><img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fblog.pluskid.org%2Fwp-content%2Fuploads%2F2010%2F05%2Fisomap-graph.png&refer=http%3A%2F%2Fblog.pluskid.org&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1628077554&t=cd17ac457469c3d0c5f60f2b27e81f91
" width="50%" alt=""></div>

在流形中，由上图可以直观的看出测地距离与欧式距离的区别，该论文就摒弃了大多论文中的 `MSE误差` ，采用角度差异的误差来进行优化。

原论文的建模过程中有两个简化，核心的式子为
$$R = I_3 + sin(\theta)[v]_× + (1-cos\theta)[v]_×^2$$$$tr(R) = 1 + 2cos(\theta)$$$$Loss_{Geodesic} = d(R_s ,R_{GT}) = cos^{-1}[\frac{tr(R_s^TR_{GT}) - 1}{2}] $$

最终求得的是变换的角度

`Code:`
```py
class GeodesicLoss(nn.Module):
    def __init__(self):
        super(GeodesicLoss, self).__init__()

    def my_R(self, x):
        R1 = torch.eye(3) + torch.sin(
            x[2]) * x[0] + (1.0 - torch.cos(x[2])) * (x[0] @ x[0])
        R2 = torch.eye(3) + torch.sin(
            x[3]) * x[1] + (1.0 - torch.cos(x[3])) * (x[1] @ x[1])

        return R1.transpose(0, 1) @ R2

    def get_theta(self, x):

        clamp_res = torch.clamp(0.5 * (x[0, 0] + x[1, 1] + x[2, 2] - 1.0),
                                -1.0 + 1e-7, 1.0 - 1e-7)
        acos_res = torch.acos(clamp_res)
        abs_res = torch.abs(acos_res)

        return abs_res

    def forward(self, y_true, y_pred):
        # skew_true: (3, 3, 3)
        # skew_pred: (3, 3, 3)
        # angle_true: (3,)    
        # angle_pred: (3,)
        # R shape: (3, 3, 3)
        angle_true = torch.sqrt(torch.sum(torch.pow(y_true, 2), axis=1))
        angle_pred = torch.sqrt(torch.sum(torch.pow(y_pred, 2), axis=1))

        # compute axes
        axis_true = F.normalize(y_true, p=2, dim=-1).view(3, 3)
        axis_pred = F.normalize(y_pred, p=2, dim=-1).view(3, 3)

        proj = torch.FloatTensor([[0, 0, 0, 0, 0, -1, 0, 1, 0],
                                  [0, 0, 1, 0, 0, 0, -1, 0, 0],
                                  [0, -1, 0, 1, 0, 0, 0, 0, 0]])

        skew_true = (axis_true @ proj).view(3, 3, 3)
        skew_pred = (axis_pred @ proj).view(3, 3, 3)

        r1 = self.my_R((skew_true[0, ...], skew_pred[0, ...], angle_true[0], angle_pred[0]))
        r2 = self.my_R((skew_true[1, ...], skew_pred[1, ...], angle_true[1], angle_pred[1]))
        r3 = self.my_R((skew_true[2, ...], skew_pred[2, ...], angle_true[2], angle_pred[2]))
        R = torch.stack([r1, r2, r3], dim=0)

        theta1 = self.get_theta(R[0, ...])
        theta2 = self.get_theta(R[1, ...])
        theta3 = self.get_theta(R[2, ...])
        theta = torch.stack([theta1, theta2, theta3], dim=0)
        return torch.mean(theta)
```

#### 2. `tf.map_fn()`
顺便记录一下 `tf.map_fn()` 函数，通过官方文档以及查资料明白其就是一个遍历迭代最后stack的过程，但是复现过程中总是遇到了问题，这时候注意把源码中的元组的每个元素都看作为迭代器，分开计算结果就正确了。

```py
R = tf.map_fn(my_R, (skew_true, skew_pred, angle_true, angle_pred), dtype=tf.float32)
```