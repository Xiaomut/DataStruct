#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   99. minPathSum.py
@Time    :   2021/12/14 17:04:41
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

def minPathSum(grid) -> int:
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]

    for i in range(1, rows):
        dp[i][0] = dp[i-1][0] + grid[i][0]

    for j in range(1, cols):
        dp[0][j] = dp[0][j-1] + grid[0][j]

    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    
    return dp[-1][-1]


if __name__ == "__main__":
    res = minPathSum(grid=[[1,2],[1,1]])
    print(res)