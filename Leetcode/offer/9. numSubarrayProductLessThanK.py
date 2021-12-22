#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   9. numSubarrayProductLessThanK.py
@Time    :   2021/12/17 11:31:52
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

from typing import List

def numSubarrayProductLessThanK(nums: List[int], k: int) -> int:
    def prod(nums):
        res = 1
        for i in nums:
            res *= i
        return res

    n = len(nums)
    res = 0
    l, r = 0, 1
    while r <= n:
        tmp = prod(nums[l:r])
        if tmp >= k:
            tmp_l = r - l - 1
            res += tmp_l * (tmp_l + 1) // 2
            l += 1
        else:
            tmp_l = r - l
            res += tmp_l * (tmp_l + 1) // 2
            r += 1
    return res // 2

if __name__ == "__main__":
    res = numSubarrayProductLessThanK(nums = [1,2,3], k = 0)
    print(res)