#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   2. addBinary.py
@Time    :   2021/12/08 16:38:17
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""
给定两个 01 字符串 a 和 b ，请计算它们的和，并以二进制字符串的形式输出。
输入为 非空 字符串且只包含数字 1 和 0。
"""


def addBinary(a, b) -> str:
    x, y = int(a, 2), int(b, 2)
    while y:
        answer = x ^ y
        carry = (x & y) << 1
        x, y = answer, carry
    return bin(x)[2:]


if __name__ == "__main__":
    res = addBinary(a="11", b="10")
    print(res)
