#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   33.  search.py
@Time    :   2022/01/07 19:28:49
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2021-2022, WangShuai
'''


def search(nums, target: int) -> int:

    def mid_search(a, target):
        l, r = 0, len(a)-1
        while l <= r:
            mid = (l + r) // 2
            num = a[mid]
            if num < target:
                l = mid + 1
            elif num > target:
                r = mid - 1
            else:
                return mid
        return None
    
    n = len(nums)
    if n == 1:
        if target == nums[0]:
            return 0
        return -1
    index = 0
    for i in range(1, n):
        if nums[i] < nums[i-1]:
            index = i
    
    l_res = mid_search(nums[:index], target)
    r_res = mid_search(nums[index:], target)
    if l_res is not None:
        return l_res
    if r_res is not None:
        return r_res + index
    return -1


if __name__ == "__main__":
    nums = [4,5,6,7,0,1,2]
    target = 0
    res = search(nums, target)