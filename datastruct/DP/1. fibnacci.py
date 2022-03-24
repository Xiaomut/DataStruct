#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   1. fibnacci.py
@Time    :   2021/10/08 17:18:12
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

from functools import lru_cache
# 递归
@lru_cache(30)
def fibnacci(n):
    if n== 1 or n == 2:
        return 1
    else:
        return fibnacci(n-1) + fibnacci(n-2)


# 非递归
def fibnacci_no_recurision(n):
    f = [0, 1, 1]
    if n > 2:
        for i in range(n-2):
            num = f[-1] + f[-2]
            f.append(num)
    return f[n]


if __name__ == "__main__":
    print(fibnacci(100))
    # print(fibnacci_no_recurision(100))