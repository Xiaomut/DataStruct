#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   107. updateMatrix.py
@Time    :   2021/12/15 17:41:03
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

from typing import List
from collections import deque


class Solution:
    def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        m, n = len(matrix), len(matrix[0])
        dist = [[0] * n for _ in range(m)]
        zeroes_pos = [(i, j) for i in range(m) for j in range(n) if matrix[i][j] == 0]
        # 将所有的 0 添加进初始队列中
        q = deque(zeroes_pos)
        seen = set(zeroes_pos)

        # 广度优先搜索
        while q:
            i, j = q.popleft()
            for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 <= ni < m and 0 <= nj < n and (ni, nj) not in seen:
                    dist[ni][nj] = dist[i][j] + 1
                    q.append((ni, nj))
                    seen.add((ni, nj))
        
        return dist

    def updateMatrix2(self, mat: List[List[int]]) -> List[List[int]]:
        m = len(mat)
        n = len(mat[0])
        inf = m + n
        if m + n < 4:
            return mat
        dist = [[inf if mat[r][c] else 0 for c in range(n)] for r in range(m)]

        # 从右下向左上更新
        for r in range(m - 1, -1, -1):
            for c in range(n-1, -1, -1):
                if dist[r][c]:
                    dist[r][c] = min(dist[r][c], dist[r+1][c] + 1 if r+1 < m else inf, dist[r][c+1] + 1 if c+1 < n else inf)

        # 左上朝右下更新
        for r in range(m):
            for c in range(n):
                if dist[r][c]:
                    dist[r][c] = min(dist[r][c], dist[r - 1][c] + 1 if 0 <= r - 1 else inf, dist[r][c - 1] + 1 if 0 <= c - 1 else inf)
        return dist


if __name__ == "__main__":
    solution = Solution()
    res = solution.updateMatrix([[0,0,0],[0,1,0],[0,0,0]])
    print(res)