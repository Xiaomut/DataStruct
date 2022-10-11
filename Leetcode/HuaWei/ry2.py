"""
一个矩阵, 5*5, 取相邻(二个成员有一个边是相同的)的6个, 输入一个6个成员列表, 判断是否满足？

矩阵成员如下: 

[[1,2,3,4,5],

[11,12,13,14,15],

[21,22,23,24,25],

[31,32,33,34,35],

[41,42,43,44,45]].

 

输入描述: 

包含6个矩阵成员数组, 如: 1, 2, 3, 4, 5, 11以一个空格分隔, 支持多行

1, 2, 3, 4, 5, 11

1, 2, 11, 14, 25, 15
"""

# 利用并查集实现。设定一个长度为6的数组, 其中每个成员单独成组,
# 接下来判断两两是否相邻, 若相邻则合并为一组。最后判断是否存在孤立的组,
# 若有则输出0, 否则输出1


def find(x):
    if tree[x] == -1:
        return x
    tmp = find(tree[x])
    tree[x] = tmp
    return tmp


# while True:
# nums = list(map(int, sys.stdin.readline().strip().split()))
# nums = [1, 2, 3, 4, 5, 11]
nums = [1, 2, 11, 14, 25, 15]
# if not nums:
#     break
tree = [-1] * 6
for i in range(6):
    for j in range(i + 1, 6):
        x, y = max(nums[i], nums[j]), min(nums[i], nums[j])
        if x - y == 1 or x - y == 10:
            a = find(i)
            b = find(j)
            if a != b:
                tree[a] = b
        print(f"tree: {tree}")
print(f"final: {tree}")
if tree.count(-1) == 1:
    print(1)
else:
    print(0)
