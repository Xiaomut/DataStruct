import torch
import numpy as np
from torch import nn
w = torch.randn(1, 6)
print(w)
r = torch.clamp(w[:, :3], -np.pi, np.pi)
t = torch.clamp(w[:, 3:], -0.9, 0.9)
w = torch.cat([r, t], dim=1)
print(w)
# nn.init.xavier_uniform_(w, gain=1)
# print(w)