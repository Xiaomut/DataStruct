#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   6. twoSum.py
@Time    :   2021/12/08 16:45:25
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""
给定一个已按照 升序排列  的整数数组 numbers ，请你从数组中找出两个数满足相加之和等于目标数 target 。
函数应该以长度为 2 的整数数组的形式返回这两个数的下标值。numbers 的下标 从 0 开始计数 ，所以答案数组应当满足 0 <= answer[0] < answer[1] < numbers.length 。
假设数组中存在且只存在一对符合条件的数字，同时一个数字不能使用两次。
"""
from typing import List


def twoSum(numbers: List[int], target: int) -> List[int]:
    l, r = 0, len(numbers)-1
    while l < r:
        tmp = numbers[l] + numbers[r]
        if tmp == target:
            return [l, r]
        elif tmp < target:
            l += 1
        else:
            r -= 1


if __name__ == "__main__":
    res = twoSum(numbers = [1,2,4,6,10], target = 8)
    print(res)