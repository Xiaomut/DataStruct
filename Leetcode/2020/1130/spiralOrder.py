#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spiralOrder.py
@Time    :   2020/12/01 08:32:02
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

# 54. Spiral Matrix


def spiralOrder(matrix):

    height, width = len(matrix), len(matrix[0])

    res = []
    num = 1
    flag = -1
    rownum = width
    colnum = height

    left2right, up2down, right2left, down2up = 0, width - 1, height - 1, 0
    while rownum > 0 and colnum > 0:
        if flag == -1:
            for index in range(rownum):
                res.append(matrix[left2right][index + down2up])
            flag -= 1
            left2right += 1
        elif flag == -2:
            for index in range(colnum):
                res.append(matrix[index + left2right][up2down])
            flag -= 1
            up2down -= 1
        elif flag == -3:
            for index in range(rownum - 1, -1, -1):
                res.append(matrix[right2left][index + down2up])
            flag -= 1
            right2left -= 1
        else:
            for index in range(colnum - 1, -1, -1):
                res.append(matrix[index + left2right][down2up])
            flag = -1
            down2up += 1

        if flag == -1 or flag == -3:
            num += rownum
            rownum -= 1
        else:
            num += colnum
            colnum -= 1

    return res


matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
for i in matrix:
    print(i)
print('------------------------------------')
print(spiralOrder(matrix))
"""
Runtime: 28 ms, faster than 79.52% of Python3 online submissions for Spiral Matrix.
Memory Usage: 14.4 MB, less than 5.88% of Python3 online submissions for Spiral Matrix.
"""