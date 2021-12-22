#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   91. minCost.py
@Time    :   2021/12/21 16:36:54
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''


def minCost(costs) -> int:
    dp = [[0] * len(costs[0]) for _ in range(len(costs))]

    dp[0] = costs[0]
    for i in range(1, len(costs)):
        for j in range(3):
            if j == 0:
                dp[i][0] = costs[i][0] + min(dp[i-1][1], dp[i-1][2])
            elif j == 1:
                dp[i][1] = costs[i][1] + min(dp[i-1][0], dp[i-1][2])
            else:
                dp[i][2] = costs[i][2] + min(dp[i-1][0], dp[i-1][1])
    return min(dp[-1])


if __name__ == "__main__":
    costs = [[17,2,17]]
    res = minCost(costs)
    print(res)