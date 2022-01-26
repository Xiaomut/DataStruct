#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   89. grayCode.py
@Time    :   2022/01/05 16:08:00
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2021-2022, WangShuai
'''

def grayCode(n: int):
    res, head = [0], 1
    for i in range(n):
        for j in range(len(res) - 1, -1, -1):
            res.append(head + res[j])
        head <<= 1
    return res


if __name__ == "__main__":
    res = grayCode(4)
    print(res)

