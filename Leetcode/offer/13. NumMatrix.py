#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   13. NumMatrix.py
@Time    :   2021/12/14 10:18:26
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

from typing import List


class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        self.sums = [[0] * len(matrix[0]) for _ in range(len(matrix))]
        
        self.sums[0][0] = matrix[0][0]
        for i in range(1, len(matrix)):
            self.sums[i][0] = self.sums[i-1][0] + self.matrix[i][0]
        for j in range(len(matrix[0])):
            self.sums[0][j] = sum(matrix[0][:j+1])

        for i in range(1, len(matrix)):
            for j in range(1, len(matrix[0])):
                self.sums[i][j] = self.sums[i-1][j] + self.sums[i][j-1] - self.sums[i-1][j-1] + matrix[i][j]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        if row1 == 0 and col1 == 0:
            return self.sums[row2][col2]
        elif row1 == 0:
            return self.sums[row2][col2] - self.sums[row2][col1-1]
        elif col1 == 0:
            return self.sums[row2][col2] - self.sums[row1-1][col2]
        else:
            return self.sums[row2][col2] - self.sums[row2][col1-1] - self.sums[row1-1][col2] + self.sums[row1-1][col1-1]

# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)


if __name__ == "__main__":
    matrix = [[-4, -5]]
    obj = NumMatrix(matrix)
    row1, col1, row2, col2 = [0, 1, 0, 1]
    param_1 = obj.sumRegion(row1, col1, row2, col2)
    print(param_1)