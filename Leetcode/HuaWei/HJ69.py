x = int(input())
y = int(input())
z = int(input())
A = []
B = []
for i in range(x):
    A.append(list(map(int,input().split()))) 
for j in range(y):
    B.append(list(map(int,input().split())))
#输入录入后，开始计算，先初始化一个二维数组，初始值为0
R=[[0 for k in range(z)] for i in range(x)]
for i in range(x):
    for k in range(z):
        for j in range(y): #计算每个输出单元格的数据，A行与B列的乘积，长度为y
            R[i][k] += A[i][j] * B[j][k]
#按行输出
for i in range(x):
    for k in range(z):
        print(R[i][k], end = ' ')
    print('')