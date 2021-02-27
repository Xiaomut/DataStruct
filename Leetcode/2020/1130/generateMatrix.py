#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   generateMatrix.py
@Time    :   2020/11/30 17:23:50
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

# 59. Spiral Matrix II


def generateMatrix(n):
    matrix = [[0] * n for _ in range(n)]

    # matrix[0] = list(range(n))
    flag = -1
    num = 1
    left2right, up2down, right2left, down2up = 0, n - 1, n - 1, 0
    value = n
    time = 0

    while value > 0:
        if flag == -1:
            for index, i in enumerate(list(range(num, num + value))):
                matrix[left2right][index + down2up] = i
            flag -= 1
            left2right += 1
        elif flag == -2:
            for index, i in enumerate(list(range(num, num + value))):
                matrix[index + left2right][up2down] = i
            flag -= 1
            up2down -= 1
        elif flag == -3:
            for index, i in enumerate(list(range(num, num + value))[::-1]):
                matrix[right2left][index + down2up] = i
            flag -= 1
            right2left -= 1
        else:
            for index, i in enumerate(list(range(num, num + value))[::-1]):
                matrix[index + left2right][down2up] = i
            flag = -1
            down2up += 1

        time += 1
        num += value
        if value == n:
            value -= 1
            time = 0
        elif time % 2 == 0:
            value -= 1

        # print('-----------------------------')
        # for i in matrix:
        #     print(i)

    return matrix


n = 5
# print(generateMatrix(n))
for i in generateMatrix(n):
    print(i)