#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   searchInsert.py
@Time    :   2020/11/19 20:08:57
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''


def searchInsert(nums, target):
    if target > nums[-1]:
        return len(nums)
    elif target <= nums[0]:
        return 0
    else:
        num = binary_search(nums, target)
        if nums[num] > target:
            return num
        else:
            return num + 1


def binary_search(nums, target):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (right + left) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        else:
            return mid
    return mid


print(searchInsert(nums=[1, 3, 5, 6], target=2))
"""
Runtime: 52 ms, faster than 27.96% of Python3 online submissions for Search Insert Position.
Memory Usage: 14.6 MB, less than 78.08% of Python3 online submissions for Search Insert Position.
"""