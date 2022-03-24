#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   5. cut_tod.py
@Time    :   2021/10/14 15:35:38
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''


# p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 21, 23, 24, 26, 27, 27, 28, 30, 33, 36, 39, 40]
p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


def cut_rod_recursion_1(p, n):
    if n == 0:
        return 0
    res = p[n]
    for i in range(1, n // 2):
        res = max(res, cut_rod_recursion_1(p, i) + cut_rod_recursion_1(p, n-i))
    return res


def cut_rod_recursion_2(p, n):
    if n == 0:
        return 0
    res = 0
    for i in range(1, n+1):
        res = max(res, p[i] + cut_rod_recursion_2(p, n-i))
    return res


def cut_rod_dp(p, n):
    r = [0]
    for i in range(1, 1+n):
        res = 0
        for j in range(1, 1+i):
            res = max(res, p[j] + r[i-j])
        r.append(res)
    return r[n]


if __name__ == "__main__":
    print(cut_rod_recursion_1(p, 9))
    print(cut_rod_recursion_2(p, 9))