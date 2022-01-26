#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   231.isPowerOfTwo.py
@Time    :   2021/12/28 17:38:42
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

def isPowerOfTwo(n):
    while n:
        n = n >> 1
        print(n)


if __name__ == "__main__":
    isPowerOfTwo(4)