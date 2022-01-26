#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   78. subset.py
@Time    :   2021/12/29 19:12:24
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

import itertools

def subsets1(nums):
    res = [[]]
    for i in nums:
        res = res + [[i] + num for num in res]
        print(res)
    return res


def subsets2(nums):
    res = []
    for i in range(len(nums)+1):
        for tmp in itertools.combinations(nums, i):
            res.append(tmp)
    return res


def subsets3(nums):
    res = []
    n = len(nums)

    def helper(i, tmp):
        res.append(tmp)
        for j in range(i, n):
            helper(j + 1, tmp + [nums[j]])
    helper(0, [])

    return res


if __name__ == "__main__":
    nums = [1,2,3]
    # res = subsets1(nums)
    res = subsets3(nums)