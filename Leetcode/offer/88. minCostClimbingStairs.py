#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   88. minCostClimbingStairs.py
@Time    :   2021/12/08 16:52:42
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""
数组的每个下标作为一个阶梯，第 i 个阶梯对应着一个非负数的体力花费值 cost[i]（下标从 0 开始）。
每当爬上一个阶梯都要花费对应的体力值，一旦支付了相应的体力值，就可以选择向上爬一个阶梯或者爬两个阶梯。
请找出达到楼层顶部的最低花费。在开始时，你可以选择从下标为 0 或 1 的元素作为初始阶梯。
"""
from typing import List


def minCostClimbingStairs(cost: List[int]) -> int:
    length = len(cost)
    if length == 2:
        return min(cost)

    dp = [0] * (length)
    dp[0] = cost[0]
    dp[1] = cost[1]

    for idx in range(2, length):
        dp[idx] = min(dp[idx-1]+cost[idx], dp[idx-2]+cost[idx])

    return min(dp[-1], dp[-2])


if __name__ == "__main__":
    res = minCostClimbingStairs(cost=[1, 100, 1, 1, 1, 100, 1, 1, 100, 1])
    print(res)