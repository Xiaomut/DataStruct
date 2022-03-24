#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   number_join.py
@Time    :   2021/10/08 19:51:59
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

from functools import cmp_to_key


def number_join(numbers):
    nums = list(map(str, numbers))
    nums.sort(key=cmp_to_key(cmp))
    print(f'nums: {nums}')
    s = ''.join(nums)
    s2 = ''.join(nums[::-1])
    print(f's: {s}')
    print(f's2: {s2}')
    return min(s, s2)


def cmp(a, b):
    if a+b < b+a:
        return 1
    elif a > b:
        return -1
    else:
        return 0


if __name__ == "__main__":
    a = '32123'
    b = '323'
    nums = [3, 323, 32123]
    print(cmp(a, b))
    print(number_join(nums))