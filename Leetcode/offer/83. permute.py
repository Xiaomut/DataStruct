#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   83. permute.py
@Time    :   2021/12/10 16:39:28
@Author  :   SmallMu 
@Contact :   hunt_hak@outlook.com
@License :   (C)Copyright 2020-2021, WangShuai
'''

"""给定一个不含重复数字的整数数组 nums ，返回其 所有可能的全排列 。可以 按任意顺序 返回答案。"""
from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    def dfs(first=0):
        # 所有数都填完了
        if first == n:  
            res.append(nums[:])
        for i in range(first, n):
            # 动态维护数组
            nums[first], nums[i] = nums[i], nums[first]
            # 继续递归填下一个数
            dfs(first + 1)
            # 撤销操作
            nums[first], nums[i] = nums[i], nums[first]
    
    res = []
    dfs()
    return res


if __name__ == "__main__":
    res = permute([1,2,3])
    print(res)