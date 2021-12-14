#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   72. mySqrt.py
@Time    :   2021/12/09 15:42:21
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

def mySqrt(x: int) -> int:
    if x == 0:
        return 0
    if x <= 3:
        return 1
    if x == 4:
        return 2

    num = 0
    tmp = x
    while tmp > 0:
        tmp >>= 1
        num += 1
    for i in range(num-1, x // num):
        if i**2 == x:
            return i
        elif i**2 < x:
            continue
        else:
            return i-1 
    return num - 1

if __name__ == "__main__":
    # for i in range(0, 66):
    #     res = mySqrt(i)
    #     print(f'res {i}: {res}')
    