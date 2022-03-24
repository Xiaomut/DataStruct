## Recursive Cascaded Networks for Unsupervised Medical Image Registration 论文


- 这是一篇19年的配准论文
- [官方源码链接 tf版](https://github.com/microsoft/Recursive-Cascaded-Networks) 
- [非官方源码链接 pytorch版](https://github.com/ivan-jgr/recursive-cascaded-networks) 

论文也很容易理解，看了代码就完全明白了，很清晰易懂。

pytorch版本的改动适用于 `2D` 和 `3D` 图像，但是中间的图像显示仅适用于 `2D` 图像，自行去掉就好。源码无法直接运行，跟着报错稍作改动。本人主要添加了加载模型的问题，如果想从某个epoch训练或验证的时候如何加载网络。



```py
class RecursiveCascadeNetwork(nn.Module):
    """For Training"""
    def __init__(self, n_cascades, im_size, device, state_dict=None, testing=False):
        super(RecursiveCascadeNetwork, self).__init__()

        self.stems = []
        # See note in base_networks.py about the assumption in the image shape
        init_model = VTNAffineStem(dim=len(im_size), im_size=im_size[0]).to(device)
        self.stems.append(init_model)
        for i in range(n_cascades):
            model = VTN(dim=len(im_size), flow_multiplier=1.0 / n_cascades).to(device)
            self.stems.append(model)

        self.reconstruction = SpatialTransform(im_size).to(device)

        # 如果有模型，则加载已有模型
        if state_dict:
            for i, m in enumerate(self.stems):
                m.load_state_dict(state_dict[f'cascade {i}'])

        if testing:
            for m in self.stems:
                m.eval()
            self.reconstruction.eval()

    def forward(self, fixed, moving):
        flows = []
        stem_results = []
        # Affine registration
        flow = self.stems[0](fixed, moving)
        stem_results.append(self.reconstruction(moving, flow))
        flows.append(flow)
        for model in self.stems[1:]: # cascades
            # registration between the fixed and the warped from last cascade
            flow = model(fixed, stem_results[-1])
            stem_results.append(self.reconstruction(stem_results[-1], flow))
            flows.append(flow)

        return stem_results, flows

checkpoint = 'ckp/model_wts/epoch_120.pth'
state_dict = torch.load(checkpoint)
```

<div align="center"><img src="https://img-blog.csdnimg.cn/d3bfd9deb1614c7785043da4ffd2fb2d.png
" width="60%" alt=""></div>

如果从中间开始训练，引入 `state_dict` 即可，如果测试，将 `testing` 改为 `True`

具体的结果还在改一些细节，总是有点小问题，目前还没有确定，待确定就有结果了，迫不及待。