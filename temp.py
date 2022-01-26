import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# 生成随机数
alpha = [1, 1, 1] # 三维平狄利克雷分布
N = 1000; L = len(alpha) # 样本数N=1000
gamma_rnd = np.zeros([L, N]); dirichlet_rnd = np.zeros([L, N])
for n in range(N):
    for i in range(L):
        gamma_rnd[i, n]=np.random.gamma(alpha[i], 1)
    # 逐样本归一化（对维度归一化）
    Z_d = np.sum(gamma_rnd[:, n])
    dirichlet_rnd[:, n] = gamma_rnd[:, n]/Z_d
# 绘制散点图
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(dirichlet_rnd[0, :], dirichlet_rnd[1, :], dirichlet_rnd[2, :])
ax.view_init(30, 60)

plt.show()