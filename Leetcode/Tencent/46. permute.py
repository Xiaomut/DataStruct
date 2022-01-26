#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   46. permute.py
@Time    :   2022/01/08 09:17:15
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2021-2022, WangShuai
'''


def permute(nums):
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """
    def backtrack(first = 0):
        # 所有数都填完了
        if first == n:  
            res.append(nums[:])
        for i in range(first, n):
            # 动态维护数组
            nums[first], nums[i] = nums[i], nums[first]
            # 继续递归填下一个数
            backtrack(first + 1)
            # 撤销操作
            nums[first], nums[i] = nums[i], nums[first]
    
    n = len(nums)
    res = []
    backtrack()
    return res



if __name__ == "__main__":
    nums = [1,2,3]
    res = permute(nums)
    print(nums)