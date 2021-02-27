#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   maxSubArray.py
@Time    :   2020/11/23 17:49:34
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


# 53. Maximum Subarray
def maxSubArray(nums):
    maxSub, curSum = nums[0], 0

    for n in nums:
        if curSum < 0:
            curSum = 0
        curSum += n
        maxSub = max(maxSub, curSum)
    return maxSub


maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
