#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   12. pivotIndex.py
@Time    :   2021/12/08 17:33:16
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""
给你一个整数数组 nums ，请计算数组的 中心下标 。
数组 中心下标 是数组的一个下标，其左侧所有元素相加的和等于右侧所有元素相加的和。
如果中心下标位于数组最左端，那么左侧数之和视为 0 ，因为在下标的左侧不存在元素。这一点对于中心下标位于数组最右端同样适用。
如果数组有多个中心下标，应该返回 最靠近左边 的那一个。如果数组不存在中心下标，返回 -1 。
"""

def pivotIndex(nums) -> int:
    length = len(nums)
    idx = length // 2
    while 0 <= idx <= length-1:
        if sum(nums[:idx]) == sum([idx+1:])


if __name__ == "__main__":
    res = pivotIndex()
    print(res)
