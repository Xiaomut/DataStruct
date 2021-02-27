#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   rotate.py
@Time    :   2020/11/23 16:22:24
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

# 这个能得到结果但是不对，必须是原列表发生变化
# def rotate(matrix):
#     n = len(matrix)
#     # print(f'matrix: {matrix}')
#     image = [[0] * n for i in range(n)]
#     for i in range(n):
#         for j in range(n):
#             image[j][n - i - 1] = matrix[i][j]
#     matrix = image
#     return matrix


def rotate(matrix):
    n = len(matrix)

    for i in range(n):
        for j in range(i):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    for i in range(n):
        for j in range(n // 2):
            matrix[i][j], matrix[i][n - j - 1] = matrix[i][n - j -
                                                           1], matrix[i][j]
    return matrix


print(rotate(matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
