from itertools import accumulate


def min_dist(weights):
    m, n = len(weights), len(weights[0])
    # 构造路径表
    tables = [[0] * n for _ in range(m)]

    # 初始化第一列和第一行路径的值
    tables[0] = list(accumulate(weights[0]))
    for i, v in enumerate(accumulate(row[0] for row in (weights))):
        tables[i][0] = v

    # 不断取局部最优，得到最终最优解
    for i in range(1, m):
        for j in range(1, n):
            tables[i][j] = weights[i][j] + min(tables[i - 1][j],
                                               tables[i][j - 1])

    # print(tables)
    return tables[-1][-1]


if __name__ == "__main__":

    weights = [
        [1, 3, 5, 9],
        [2, 1, 3, 4],
        [5, 2, 6, 7],
        [6, 8, 4, 3],
    ]
    min_d = min_dist(weights)
    print(min_d)